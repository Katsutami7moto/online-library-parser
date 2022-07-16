import argparse
from itertools import chain
import json
from pathlib import Path

import requests
from bs4 import BeautifulSoup

from parse_tululu import download_books_and_images, handle_errors


def check_for_page_redirect(response: requests.Response, page):
    if response.history:
        err_msg = f'There is no page {page}'
        raise requests.HTTPError(err_msg)


def save_pretty_json(data, path: str):
    json_path = Path(path)
    json_path.mkdir(parents=True, exist_ok=True)
    file_path = json_path.joinpath('books_catalog.json')
    with open(file_path, 'w', encoding='utf8') as file:
        file.write(json.dumps(data, indent=4, ensure_ascii=False))


def get_final_page(genre_url: str) -> int:
    response = requests.get(genre_url)
    response.raise_for_status()
    genre_soup = BeautifulSoup(response.text, 'lxml')
    final_page = genre_soup.select_one(
        'body p.center a.npage:last-of-type'
    ).text
    return int(final_page)


def get_one_page_book_ids(genre_url: str, page: int) -> list:
    page_url = f'{genre_url}{page}/'
    response = requests.get(page_url)
    response.raise_for_status()
    check_for_page_redirect(response, page)
    soup = BeautifulSoup(response.text, 'lxml')
    return [book.select_one('a')['href'].strip('/b')
            for book in soup.select('body .d_book')]


def get_book_ids(genre_url: str, pages: tuple) -> list:
    book_ids = []
    for page in range(*pages):
        book_ids.append(
            handle_errors(
                get_one_page_book_ids,
                genre_url,
                page
            )
        )
    return list(chain(*book_ids))


def download_genre_books(args: argparse.Namespace, genre_url: str):
    pages = args.start_page, args.end_page + 1
    book_ids = get_book_ids(genre_url, pages)
    downloaded_books_catalog = download_books_and_images(
        book_ids, args.skip_txt, args.skip_img, args.dest_folder
    )
    save_pretty_json(downloaded_books_catalog, args.json_path)


def main():
    sci_fi_url = 'https://tululu.org/l55/'
    final_page = get_final_page(sci_fi_url)

    parser = argparse.ArgumentParser()
    parser.add_argument('--start_page', type=int, default=1)
    parser.add_argument('--end_page', type=int, default=final_page)
    parser.add_argument('--dest_folder', default='media')
    parser.add_argument('--skip_txt', action='store_true')
    parser.add_argument('--skip_img', action='store_true')
    parser.add_argument('--json_path', default='media')

    args = parser.parse_args()
    download_genre_books(args, sci_fi_url)


if __name__ == '__main__':
    main()
