# Importing libraries
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Opening Google Chrome (WebDrive)
driver = webdriver.Chrome()
driver.get("https://www.iasp.ws/our-members/directory")
time.sleep(5)

# Accepting Cookies Policy
# Note: Update the Xpath if it's not working
submit_button = driver.find_element(by=By.XPATH, value='//*[@id="layout_1200087sub1mergefield_5"]/div/input')
submit_button.click()
time.sleep(5)

# Scrolling the page
for _ in range(25):
  driver.find_element(by=By.TAG_NAME, value='body').send_keys(Keys.PAGE_DOWN)
  time.sleep(2)

# Scraping TechParks IASP URLs
urls = []
techpark_card = driver.find_elements(by=By.CLASS_NAME, value='member-item')

for index, techpark in enumerate(techpark_card):
  url = techpark.get_attribute(name="href")    
  urls.append(url)

# Scraping data about each TechPark
# Important: we use 'try' and 'except' because of missing values in some of the TechParks
names = []
descriptions = []
locations = []
website_urls = []
twitter_urls = []
linkedin_urls = []
main_tech_sectors = []
parks_types = []
members_category = []

for url in urls:
    
  driver.get(url)
  time.sleep(2)  # Wait for the page to load
  
  try:
    name = driver.find_element(by=By.XPATH, value='//*[@id="layout500sub1mergefield293"]/div/div').text
  except:
    name = "None"
  names.append(name)
  
  try:
    description = driver.find_element(by=By.XPATH, value='//*[@id="layout500sub1mergefield301"]/div/div').text
  except:
    description = "None"
  descriptions.append(description)
  
  try:
    location = driver.find_element(by=By.XPATH, value='//*[@id="layout500sub1mergefield2645"]/div').text
  except:
    location = "None"
  locations.append(location)
  
  try:
    website_url = driver.find_element(by=By.XPATH, value='//*[@id="layout500sub1mergefield299"]/div/span/a').get_attribute(name="href")
  except:
    website_url = "None"
  website_urls.append(website_url)
    
  try:
    twitter_url = driver.find_element(by=By.XPATH, value='//*[@id="layout500sub1mergefield2058"]/div/div/a').get_attribute(name="href")
  except:
    twitter_url = "None"
  twitter_urls.append(twitter_url)
    
  try:
    linkedin_url = driver.find_element(by=By.XPATH, value='//*[@id="layout500sub1mergefield2057"]/div/div/a').get_attribute(name="href")
  except:
    linkedin_url = "None"
  linkedin_urls.append(linkedin_url)
    
  try:
    main_tech_sector = driver.find_element(by=By.XPATH, value='//*[@id="layout500sub1mergefield359"]').text
  except:
    main_tech_sector = "None"
  main_tech_sectors.append(main_tech_sector)
    
  try:
    park_type = driver.find_element(by=By.XPATH, value='//*[@id="layout500sub1mergefield352"]/div').text
  except:
    park_type = "None"
  parks_types.append(park_type)
    
  try:
    member_category = driver.find_element(by=By.XPATH, value='//*[@id="layout500sub1mergefield422"]/div').text
  except:
    member_category = "None"
  members_category.append(member_category)

driver.quit()

# Creating a Pandas Dataframe
df_techparks = pd.DataFrame()
df_techparks['name'] = names
df_techparks['decription'] = descriptions
df_techparks['location'] = locations
df_techparks['website_url'] = website_urls
df_techparks['twitter_url'] = twitter_urls
df_techparks['linkedin_url'] = linkedin_urls
df_techparks['main_tech_sector'] = main_tech_sectors
df_techparks['park_type'] = parks_types
df_techparks['member_category'] = members_category

# Transforming in a csv file
df_techparks.to_csv('techparks_iasp.csv', index=False)
