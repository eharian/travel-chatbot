import os
import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.agents import ZeroShotAgent, Tool, AgentExecutor
from langchain.utilities import SearchApiAPIWrapper
from langchain import LLMChain
from langchain.callbacks import StreamlitCallbackHandler
from ImageSearch import ImageSearchTool
import re
import base64
from pathlib import Path
from dotenv import load_dotenv
from streamlit_mic_recorder import mic_recorder,speech_to_text

load_dotenv('.env')
searchapi_api_key = os.environ.get("SEARCH_KEY")
openai_api_key = os.environ.get("OPENAI_KEY")

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text


def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=500,
        chunk_overlap=100,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks


def get_vectorstore(text_chunks):
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore


def get_conversation_chain(vectorstore):
    llm = ChatOpenAI(openai_api_key=openai_api_key,
                    temperature=0,
                    model="gpt-4-1106-preview")
    memory = ConversationBufferMemory(
        memory_key='chat_history', return_messages=True)
    qa = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(
            search_type="similarity", search_kwargs={"k": 4}),
        memory=memory,
    )
    tools = [
    Tool(
        name = "Travel QA System",
        func = qa.run,
        description = "useful for when you need to answer questions about the uploaded document. Input should be a fully formed question or a request."
    ),
    ImageSearchTool(),
    Tool(
        name = "Additional Answer",
        func = SearchApiAPIWrapper(searchapi_api_key=searchapi_api_key).run,
        description = "useful for when the answer cannot be found in the given documents, then use this to search"
    )
    ]

    prefix = """You are an expert at anything travel related as well as planning, answer the questions as best as you can.
    If the action is image_search then reply with the source image.
    You have access to the following tools:"""
    suffix = """Begin!
        {chat_history}
        Question: {input} No need to add Action
        {agent_scratchpad}
    """

    prompt = ZeroShotAgent.create_prompt(
        tools,
        prefix=prefix,
        suffix=suffix,
        input_variables=["input", "chat_history", "agent_scratchpad"]
    )
    
    llm_chain = LLMChain(llm=llm, prompt=prompt)
    agent = ZeroShotAgent(llm_chain=llm_chain, tools=tools, verbose=True)
    agent_chain = AgentExecutor.from_agent_and_tools(agent=agent, tools=tools, verbose=True, memory=memory, handle_parsing_errors=True)

    return agent_chain

def is_image(s):
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp']
    return any(ext in str.lower(s) for ext in image_extensions)


def img_to_bytes(img_path):
    try:
        img_bytes = Path(img_path).read_bytes()
        encoded = base64.b64encode(img_bytes).decode()
        return encoded
    except:
        return ''

def img_to_html(img_path):
    img_html = "<img src='data:image/png;base64,{}' class='img-fluid'>".format(
      img_to_bytes(img_path)
    )
    return img_html


def handle_userinput(prompt):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        st_callback = StreamlitCallbackHandler(st.container())
        response = st.session_state.conversation.run(prompt, callbacks=[st_callback])
        
        pattern = r'!\[.*?\]\(.*?\.jpg\)'
        replacement_texts = re.findall(pattern, response)
        for replacement in replacement_texts:
            image_file_pattern = r"\/Images/[^]]+\.jpg"
            src_file = f'.{re.findall(image_file_pattern, replacement)[0]}'
            src_file = src_file.replace('%20', ' ')
            response = response.replace(replacement, img_to_html(src_file))
        # check if response is an image
        st.markdown(response, unsafe_allow_html=True)
        st.session_state.messages.append({"role": "assistant", "content": response})
            
        



def main():
    load_dotenv()
    st.set_page_config(page_title="Travel Genie",
                       page_icon="🧞")
    st.header("Travel Genie 🧞")
    
    with st.sidebar:
        st.subheader("Your documents")
        pdf_docs = st.file_uploader(
            "Upload your PDFs here and click on 'Process'", accept_multiple_files=True)
        if st.button("Process"):
            with st.spinner("Processing"):
                # get pdf text
                raw_text = get_pdf_text(pdf_docs)

                # get the text chunks
                text_chunks = get_text_chunks(raw_text)

                # create vector store
                vectorstore = get_vectorstore(text_chunks)

                # create conversation chain
                st.session_state.conversation = get_conversation_chain(
                    vectorstore)
                
        st.divider()

        stt = speech_to_text(language='en',use_container_width=True,just_once=True,key='STT')



    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "How may I help you?"}]

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"], unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None

    if stt:
        handle_userinput(stt)

    if prompt := st.chat_input("Ask questions here"):
        handle_userinput(prompt)

if __name__ == '__main__':
    main()
