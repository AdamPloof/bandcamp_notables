from bs4 import BeautifulSoup
from selenium import webdriver

from datetime import date
import requests
import time
import csv


# Navigate to page with Selenium in order for async content to load
driver = webdriver.Firefox(executable_path='/usr/local/bin/geckodriver')
driver.get('https://peggysue.bandcamp.com/album/vices')
time.sleep(2)

source = driver.page_source

soup = BeautifulSoup(source, 'lxml')

bio = soup.find('div', id='bio-container')
location = bio.find('span', class_='location').text

buy_item = soup.find('li', class_='buyItem digital')
amount = buy_item.find('span', class_='base-text-color').text
currency = buy_item.find('span', class_='buyItemExtra secondaryText').text

try:
    label_link = soup.find('a', class_='back-to-label-link')
    has_label = True
    label_raw = label_link.find('span', class_='back-link-text').text
    label = label_raw.strip('more from')
except Exception as e:
    has_label = False
    label = None

print(location)
print(amount)
print(currency)
print(has_label)
print(label)
driver.close()