import argparse
import json
from pathlib import Path
from time import sleep
from urllib.parse import urljoin, urlsplit, unquote

import requests
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename

from parse_tululu import download_books_and_images


def save_pretty_json(data):
    with open('downloaded_books.json', 'w', encoding='utf8') as file:
        file.write(json.dumps(data, indent=4, ensure_ascii=False))


def get_book_ids(genre_url: str, start_page: int, end_page: int) -> list:
    book_ids = []
    for page in range(start_page, end_page + 1):
        page_url = f'{genre_url}{page}/'
        response = requests.get(page_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'lxml')
        for book in soup.select('body .d_book'):
            book_id = book.select_one('a')['href'].strip('/b')
            book_ids.append(book_id)
    return book_ids


def main():
    sci_fi_url = 'https://tululu.org/l55/'
    book_ids = get_book_ids(sci_fi_url, 1, 2)  # 45 книг
    downloaded_books_catalog = download_books_and_images(book_ids)
    save_pretty_json(downloaded_books_catalog)


if __name__ == '__main__':
    main()
