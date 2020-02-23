from bs4 import BeautifulSoup
from selenium import webdriver

from datetime import date
import requests
import time
import csv


# Open the CSV file to write output to
today = str(date.today())
csv_title = './stats/bc_notable_' + today + '.csv'
csv_file = open(csv_title, 'w')
csv_writer = csv.writer(csv_file)
csv_writer.writerow([
    'Title', 
    'Artist', 
    'Genre', 
    'Link', 
    'Date', 
    'Location', 
    'Amount',
    'Currency',
    'Has Label',
    'Label'
])

# Navigate to page with Selenium in order for async content to load
driver = webdriver.Firefox(executable_path='/usr/local/bin/geckodriver')
driver.get('https://bandcamp.com/')
time.sleep(2)
driver.execute_script("window.scrollTo(0, 1750)")
time.sleep(2)
notable = driver.find_element_by_xpath('/html/body/div[3]/div/div[2]/div[1]/div[2]/div[5]/div[2]')

# Sample source (so that the browser doesn't need to open every time during devolpment)
# with open('source_sample.txt', 'r') as source_file:
#     source = source_file.read()

# load the content of .result-notable div into source
source = notable.get_attribute('innerHTML')
soup = BeautifulSoup(source, 'lxml')

def get_album_info(driver, url):
    # Retrieve the artist's hometown, label info, and price of the digital album
    driver.get(url)
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

    album_info = {
        'location': location,
        'amount': amount,
        'currency': currency,
        'has_label': has_label,
        'label': label
    }

    return album_info


def get_notables_info(item):
    # Retrieve info on notable item
    artist_raw = item.find('span', attrs={"data-bind": "text: artist"}).text
    artist = artist_raw.strip()

    link_raw = item.find('h4', class_="item-title").a['href']
    link = link_raw.split('?')[0]

    try:
        genre_raw = item.find('p', attrs={"data-bind": "text: genre"}).text
        genre = genre_raw.strip()
        if not genre:
            genre = None
    except AttributeError as e:
        genre = None

    notables_info = {
        'artist': artist,
        'link': link,
        'genre': genre
    }

    return notables_info

# drill down to get the artist name, album title, genre, link
items = soup.find_all('div', class_='notable-item')

# Create a list of titles to check against in order to prevent duplicating entries
titles = []

for item in items:
    title_raw = item.find('span', attrs={"data-bind": "text: title"}).text
    title = title_raw.strip()

    if not title in titles:
        notables = get_notables_info(item)

        # Get info for album from the album's page
        album = get_album_info(driver, notables['link'])
        date = today

        csv_writer.writerow([
            title, 
            notables['artist'], 
            notables['genre'], 
            notables['link'], 
            date, 
            album['location'],
            album['amount'],
            album['currency'],
            album['has_label'],
            album['label']
        ])

        titles.append(title)

# close the browser and file
csv_file.close()
driver.close()