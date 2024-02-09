from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import re


option = webdriver.ChromeOptions()
option.add_argument('--headless')
browser = webdriver.Chrome(options=option)


browser.get('https://www.tripadvisor.com/Attractions')


try:
    # Use CSS Selector to locate the search field with multiple attributes
    search_input = WebDriverWait(browser, 60).until(
        EC.presence_of_element_located((By.CSS_SELECTOR,
                                        "input[type='search'][role='searchbox'][placeholder='Search a destination, attraction, or activity'][title='Search'][aria-autocomplete='list']"))
    )
    search_input.clear()  # Clear the field if needed
    search_value = "las vegas"  # The value I want to write into the input
    search_input.send_keys(search_value)  # Write the value into the input field
    #print(f"Value set in search input: {search_input.get_attribute('value')}")  # Print out the value to ensure it's set

    # To mimic pressing Enter after input
    search_input.send_keys(Keys.RETURN)

except TimeoutException:
    print("Search input field was not found within the given time.")

previous_url = browser.current_url

try:
    search_button = WebDriverWait(browser, 60).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "button[type='submit'][title='Search'][aria-label='Search']"))
    )
    browser.execute_script("arguments[0].click();", search_button)
except TimeoutException:
    print("Search button was not found within the given time.")

new_url = browser.current_url
browser.get(new_url)

# Assume browser is a webdriver instance
activities = []
ratings_activity = []
addresses_activity = []
images_activity = []
links_activity = []

# After the page has loaded, find the elements
activity_elements = browser.find_elements(By.CSS_SELECTOR, 'div.result-title > span')

try:
    # Wait for the rating elements to be present in the DOM
    rating_elements = WebDriverWait(browser, 60).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "span.ui_bubble_rating"))
    )
    # Retrieve the ratings for the first 10 elements found
    for rating_element in rating_elements:  # Only process the first 10 elements
        rating_text = rating_element.get_attribute('alt')
        ratings_activity.append(rating_text)
except TimeoutException:
    print("Rating elements were not found within the given time.")

address_elements = browser.find_elements(By.CSS_SELECTOR, 'div.address-text')

image_elements = browser.find_elements(By.CSS_SELECTOR, 'div.inner')

link_elements = browser.find_elements(By.CSS_SELECTOR, 'div.result-title')

# Loop through the found elements and get the text
for activity_element in activity_elements:
    activities.append(activity_element.text)

for address_element in address_elements:
    addresses_activity.append(address_element.text)

for image_element in image_elements:
    image_url = image_element.get_attribute('style')
    images_activity.append(image_url)

for link_element in link_elements:
    link_url = link_element.get_attribute('onclick')
    links_activity.append(link_url)

image_urls = []

# Iterate through each string in the list and apply the regex to find URLs
for string in images_activity:
    image_urls.extend(re.findall(r'https?://[^\s"]+\.jpg', string))

def get_filename_from_url(url):
    return url.rsplit('/', 1)[-1]

image_urls_unique_activity = {}

for url in image_urls:
    filename = get_filename_from_url(url)
    if filename not in image_urls_unique_activity:
        image_urls_unique_activity[filename] = url

pattern = r"/Attraction_Review-g\d+-d\d+-Reviews-[^']+"

links_activity_final = []
for link in links_activity:
    # Use the `search` method to find the match in the HTML snippet
    match = re.search(pattern, link)
    # Extract the matched part
    extracted_part = match.group(0) if match else None
    full_link = 'https://www.tripadvisor.com' + extracted_part
    links_activity_final.append(full_link)


################################################### HOTEL ####################################################
browser.get('https://www.tripadvisor.com/Attractions')

try:
    # Use CSS Selector to locate the search field with multiple attributes
    search_input = WebDriverWait(browser, 60).until(
        EC.presence_of_element_located((By.CSS_SELECTOR,
                                        "input[type='search'][role='searchbox'][placeholder='Hotel name or destination'][title='Search'][aria-autocomplete='list']"))
    )
    search_input.clear()  # Clear the field if needed
    search_value = "las vegas"  # The value you want to write into the input
    search_input.send_keys(search_value)  # Write the value into the input field
    #print(f"Value set in search input: {search_input.get_attribute('value')}")  # Print out the value to ensure it's set

    # To mimic pressing Enter after input
    search_input.send_keys(Keys.RETURN)

except TimeoutException:
    print("Search input field was not found within the given time.")

previous_url = browser.current_url

try:
    search_button = WebDriverWait(browser, 60).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "button[type='submit'][title='Search'][aria-label='Search']"))
    )
    browser.execute_script("arguments[0].click();", search_button)
except TimeoutException:
    print("Search button was not found within the given time.")

new_url = browser.current_url
browser.get(new_url)

# Assume browser is a webdriver instance
hotels = []
addresses_hotel = []
ratings_hotel = []
images_hotel = []
links_hotel = []

# After the page has loaded, find the elements
# title_elements = browser.find_elements_by_css_selector('div.result-title > span')
hotel_elements = browser.find_elements(By.CSS_SELECTOR, 'div.result-title > span')

try:
    # Wait for the rating elements to be present in the DOM
    rating_elements = WebDriverWait(browser, 60).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "span.ui_bubble_rating"))
    )
    # Retrieve the ratings for the first 10 elements found
    for rating_element in rating_elements:  # Only process the first 10 elements
        rating_text = rating_element.get_attribute('alt')
        ratings_hotel.append(rating_text)
except TimeoutException:
    print("Rating elements were not found within the given time.")

address_elements = browser.find_elements(By.CSS_SELECTOR, 'div.address-text')

image_elements = browser.find_elements(By.CSS_SELECTOR, 'div.inner')

link_elements = browser.find_elements(By.CSS_SELECTOR, 'div.result-title')

# Loop through the found elements and get the text
for hotel_element in hotel_elements:
    hotels.append(hotel_element.text)

for address_element in address_elements:
    addresses_hotel.append(address_element.text)

for image_element in image_elements:
    image_url = image_element.get_attribute('style')
    images_hotel.append(image_url)

for link_element in link_elements:
    link_url = link_element.get_attribute('onclick')
    links_hotel.append(link_url)

image_urls = []

# Iterate through each string in the list and apply the regex to find URLs
for string in images_hotel:
    image_urls.extend(re.findall(r'https?://[^\s"]+\.jpg', string))


def get_filename_from_url(url):
    return url.rsplit('/', 1)[-1]


image_urls_unique_hotel = {}

for url in image_urls:
    filename = get_filename_from_url(url)
    if filename not in image_urls_unique_hotel:
        image_urls_unique_hotel[filename] = url

pattern = r"/Hotel_Review-g\d+-d\d+-Reviews-[^']+"

links_hotel_final = []
for link in links_hotel:
    # Use the `search` method to find the match in the HTML snippet
    match = re.search(pattern, link)
    # Extract the matched part
    extracted_part = match.group(0) if match else None
    full_link = 'https://www.tripadvisor.com' + extracted_part
    links_hotel_final.append(full_link)


browser.get('https://www.airbnb.com')

wait = WebDriverWait(browser, 60)
button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Anywhere')]")))

# Click the button
button.click()

search_input = WebDriverWait(browser, 60).until(
    EC.presence_of_element_located((By.CSS_SELECTOR,
                                    "input[placeholder='Search destinations'][data-testid='structured-search-input-field-query'][name='query']")))

# search_input.clear()  # Clear the field if needed

search_value = "las vegas"  # The value you want to write into the input
search_input.send_keys(search_value)  # Write the value into the input field

# To mimic pressing Enter after input
search_input.send_keys(Keys.RETURN)

# press search button
search_button = WebDriverWait(browser, 20).until(
    EC.presence_of_element_located(
        (By.CSS_SELECTOR, "button[type='button'][data-testid='structured-search-input-search-button']"))
)
browser.execute_script("arguments[0].click();", search_button)

airbnbs = []
subtitles_airbnbs = []
images_airbnbs = []
links_airbnbs = []

airbnb_elements = WebDriverWait(browser, 30).until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[data-testid='listing-card-title']"))
)

# Extract the text from each listing
for element in airbnb_elements:
    if element.text is not None:
        airbnbs.append(element.text)

subtitle_elements = WebDriverWait(browser, 30).until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[data-testid='listing-card-subtitle']"))
)
for element in subtitle_elements:
    if element.text is not None:
        subtitles_airbnbs.append(element.text)
subtitles_airbnbs = [item for i, item in enumerate(subtitles_airbnbs) if (i + 1) % 3 != 0]

# links_airbnb_elements = browser.find_elements(By.CSS_SELECTOR, 'div.a')
link_elements = browser.find_elements(By.CSS_SELECTOR, "div[data-testid='card-container'] > a")
for link_element in link_elements:
    link_url = link_element.get_attribute('href')
    links_airbnbs.append(link_url)

image_elements = WebDriverWait(browser, 20).until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[data-testid='card-container'] img"))
)

# Iterate over the image elements found and print their 'src' or 'data-src' attributes
for element in image_elements:
    # First, try to get the 'src' attribute
    image_src = element.get_attribute('src')
    # If 'src' is None, try to get the 'data-src' attribute or any other relevant attribute
    images_airbnbs.append(image_src)

subtitles_airbnbs = [' | '.join(subtitles_airbnbs[i:i + 2]) for i in range(0, len(subtitles_airbnbs), 2)]

title_airbnbs = [f"{a}:{b}" for a, b in zip(airbnbs, subtitles_airbnbs)]

image_dict_airbnbs = {}
for title, img in zip(title_airbnbs, images_airbnbs):
    image_dict_airbnbs[title] = img

#################################################### RESTAURANT ####################################################

browser.get('https://www.tripadvisor.com/Restaurants')

try:
    # Use CSS Selector to locate the search field with multiple attributes
    search_input = WebDriverWait(browser, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR,
                                        "input[type='search'][role='searchbox'][placeholder='City or restaurant name'][title='Search'][aria-autocomplete='list']"))
    )
    search_input.clear()  # Clear the field if needed
    search_value = "las vegas"  # The value you want to write into the input
    search_input.send_keys(search_value)  # Write the value into the input field
    #print(f"Value set in search input: {search_input.get_attribute('value')}")  # Print out the value to ensure it's set

    # To mimic pressing Enter after input
    search_input.send_keys(Keys.RETURN)

except TimeoutException:
    print("Search input field was not found within the given time.")

previous_url = browser.current_url

try:
    search_button = WebDriverWait(browser, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "button[type='submit'][title='Search'][aria-label='Search']"))
    )
    browser.execute_script("arguments[0].click();", search_button)
except TimeoutException:
    print("Search button was not found within the given time.")

new_url = browser.current_url
browser.get(new_url)

# Assume browser is a webdriver instance
restaurants = []
ratings_restaurant = []
addresses_restaurant = []
images_restaurant = []
links_restaurant = []

# After the page has loaded, find the elements
# title_elements = browser.find_elements_by_css_selector('div.result-title > span')
restaurant_elements = browser.find_elements(By.CSS_SELECTOR, 'div.result-title > span')

try:
    # Wait for the rating elements to be present in the DOM
    rating_elements = WebDriverWait(browser, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "span.ui_bubble_rating"))
    )
    # Retrieve the ratings for the first 10 elements found
    for rating_element in rating_elements:  # Only process the first 10 elements
        rating_text = rating_element.get_attribute('alt')
        ratings_restaurant.append(rating_text)
except TimeoutException:
    print("Rating elements were not found within the given time.")

address_elements = browser.find_elements(By.CSS_SELECTOR, 'div.address-text')

image_elements = browser.find_elements(By.CSS_SELECTOR, 'div.inner')

link_elements = browser.find_elements(By.CSS_SELECTOR, 'div.result-title')

# Loop through the found elements and get the text
for restaurant_element in restaurant_elements:
    restaurants.append(restaurant_element.text)

for address_element in address_elements:
    addresses_restaurant.append(address_element.text)

for image_element in image_elements:
    image_url = image_element.get_attribute('style')
    images_restaurant.append(image_url)

for link_element in link_elements:
    link_url = link_element.get_attribute('onclick')
    links_restaurant.append(link_url)

image_urls = []

# Iterate through each string in the list and apply the regex to find URLs
for string in images_restaurant:
    image_urls.extend(re.findall(r'https?://[^\s"]+\.jpg', string))


def get_filename_from_url(url):
    return url.rsplit('/', 1)[-1]


image_urls_unique_restaurant = {}

for url in image_urls:
    filename = get_filename_from_url(url)
    if filename not in image_urls_unique_restaurant:
        image_urls_unique_restaurant[filename] = url

pattern = r"/Restaurant_Review-g\d+-d\d+-Reviews-[^']+"

links_restaurant_final = []
for link in links_restaurant:
    # Use the `search` method to find the match in the HTML snippet
    match = re.search(pattern, link)
    # Extract the matched part
    extracted_part = match.group(0) if match else None
    full_link = 'https://www.tripadvisor.com' + extracted_part
    links_restaurant_final.append(full_link)

browser.get('https://www.yelp.com/search?find_desc=Restaurants&find_loc=San+Francisco%2C+CA')

search_input = WebDriverWait(browser, 80).until(
    EC.presence_of_element_located((By.CSS_SELECTOR,
                                    "input[data-testid='realInput'][placeholder='address, neighborhood, city, state or zip']")))

search_input.send_keys(Keys.CONTROL + "a")
search_input.send_keys(Keys.DELETE)

search_value = "las vegas"  # The value you want to write into the input
search_input.send_keys(search_value)  # Write the value into the input field
#print(f"Value set in search input: {search_input.get_attribute('value')}")  # Print out the value to ensure it's set

# press search button
search_button = WebDriverWait(browser, 20).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "button[aria-label='Search'][type='submit']"))
)
browser.execute_script("arguments[0].click();", search_button)
#print(browser.current_url)
# WebDriverWait(browser, 30).until(EC.url_contains(search_value))

new_url = browser.current_url
browser.get(new_url)

yelps = []
images_yelps = []
links_yelps = []

yelp_elements = WebDriverWait(browser, 60).until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[data-testid='serp-ia-card'] h3 > span > a"))
)

# Extract the text from each listing
for element in yelp_elements:
    yelps.append(element.get_attribute('name'))

image_elements = WebDriverWait(browser, 60).until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[data-testid='serp-ia-card'] div > a > img"))
)

# Iterate over the image elements found and print their 'src' or 'data-src' attributes
for element in image_elements:
    image_src = element.get_attribute('src')
    images_yelps.append(image_src)

#print(images_yelps)

link_elements = WebDriverWait(browser, 60).until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[data-testid='serp-ia-card'] div > a"))
)

for element in link_elements:
    link = element.get_attribute('href')
    links_yelps.append(link)

browser.quit()

###################################################################################################################

activity_full2 = []
for i in range(0,len(activities)):
    activity_full = activities[i] + ' ' +  ratings_activity[i] + ' ' + addresses_activity[i] + ' ' + links_activity_final[i]
    activity_full2.append(activity_full)

activity_full_string = ' '.join(map(str, activity_full2))

hotel_full2 = []
for i in range(0, len(hotels)):
    hotel_full = hotels[i] + ' ' +  ratings_hotel[i] + ' ' + addresses_hotel[i] + ' ' + links_hotel_final[i]
    hotel_full2.append(hotel_full)

airbnb_full2 = []
for i in range(0, len(airbnbs)):
    airbnb_full = title_airbnbs[i] + ' ' + links_airbnbs[i]
    airbnb_full2.append(airbnb_full)

placestostay_full = hotel_full2 + airbnb_full2

placestostay_full_string = ' '.join(map(str, placestostay_full))

restaurant_full2 = []
for i in range(0, len(restaurants)):
    restaurant_full = restaurants[i] + ' ' +  ratings_restaurant[i] + ' ' + addresses_restaurant[i] + ' ' + links_restaurant_final[i]
    restaurant_full2.append(restaurant_full)

yelp_full2 = []
for i in range(0, len(yelps)):
    yelp_full = yelps[i] + ' ' + links_yelps[i]
    yelp_full2.append(yelp_full)

plaecestoeat_full = restaurant_full2 + yelp_full2

placestoeat_full_string = ' '.join(map(str, plaecestoeat_full))

print(f"activity: {activity_full_string}")
print()
print(f"places to stay: {placestostay_full_string}")
print()
print(f'places to eat: {placestoeat_full_string}')