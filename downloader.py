import requests
from bs4 import BeautifulSoup
import lxml
from latest_user_agents import get_random_user_agent
import os


search_for = input('Search for images:  ')

dir_name = f'{search_for}_images'
os.mkdir(dir_name)

url = f'https://www.gettyimages.com/search/2/image?family=creative&phrase={search_for}'

headers = {'User-Agent': get_random_user_agent()}

response = requests.get(url, headers=headers)

html_text = response.text

soup = BeautifulSoup(html_text, 'lxml')

element_before = soup.find('input', attrs={'data-testid': 'search-pagination-input'})

page_count = int(element_before.find_next_sibling().text)

for page_no in range(1, 2):
    url = f'https://www.gettyimages.com/photos/{search_for}?assettype=image&alloweduse=availableforalluses&family=creative&phrase={search_for}&sort=mostpopular&page={page_no}'

    headers = {'User-Agent': get_random_user_agent()}

    response = requests.get(url, headers=headers)

    html_text = response.text

    soup = BeautifulSoup(html_text, 'lxml')

    image_container = soup.find('div', attrs={'data-testid': 'gallery-items-container'})

    images = image_container.find_all('img')

    for image in images:
        image_url = image['src']

        image_response = requests.get(image_url)

        with open(f'{dir_name}/{image_url.split("/")[-1].split(".jpg")[0]}.jpg', 'wb') as image_file:
            image_file.write(image_response.content)


