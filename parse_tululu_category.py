import argparse
from pathlib import Path
from time import sleep
from urllib.parse import urljoin, urlsplit, unquote

import requests
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename


def main():
    base_url = 'https://tululu.org/l55/'
    response = requests.get(base_url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    for link in soup.find('body').find_all('table', class_='d_book'):
        print(urljoin(base_url, link.find('a')['href']))


if __name__ == '__main__':
    main()
