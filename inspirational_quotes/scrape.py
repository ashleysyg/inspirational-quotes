import time
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
driver = webdriver.Chrome("/usr/local/bin/chromedriver", options=options)

# load all quotes
view_more_button = "IQButtonDefaultOutlined"
driver.get('https://www.inspiringquotes.com/inspirations')
while True:
  try:
    WebDriverWait(driver, 10).until(expected_conditions.visibility_of_element_located((By.CLASS_NAME, view_more_button)))
    elem = driver.find_element_by_class_name(view_more_button)
    driver.execute_script("arguments[0].scrollIntoView(true);", elem)
    driver.find_element_by_class_name(view_more_button).click()
  except Exception as e:
    print(e)
    break
print("completed loading more quotes")

# get quote URLs
quote_elems = driver.find_elements_by_xpath("//div[@class='IQInspirationListFeed__imageContainer IQQuoteImage']/div/a")
quote_urls = [quote.get_attribute('href') for quote in quote_elems]

driver.quit()

# scrape quotes and authors
quotes = []
authors = []
for url in quote_urls:
  req = requests.get(url)
  soup = BeautifulSoup(req.content, 'html.parser')
  quotes.append(soup.find("span", class_='IQDailyInspiration__quote').get_text())
  authors.append(soup.find("div", class_='IQDailyInspiration__author').get_text())

# convert to dataframe and write to CSV file
quotes_df = pd.DataFrame(list(zip(quotes, authors)), columns=['quote', 'author'])
quotes_df.to_csv('./data/quotes.csv', index=False)
  

