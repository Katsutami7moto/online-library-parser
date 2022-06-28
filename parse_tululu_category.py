import argparse
import json
from pathlib import Path
from time import sleep
from urllib.parse import urljoin, urlsplit, unquote

import requests
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename


def save_pretty_json(info: list):
    with open('books_info.json', 'w') as file:
        file.write(json.dumps(info, sort_keys=False,
                              indent=4, ensure_ascii=True))


def main():
    base_url = 'https://tululu.org/l55/'
    for page in range(1, 11):
        page_url = f'https://tululu.org/l55/{page}/'
        response = requests.get(page_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'lxml')
        for link in soup.find('body').find_all('table', class_='d_book'):
            print(urljoin(base_url, link.find('a')['href']))


if __name__ == '__main__':
    main()
