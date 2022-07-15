import argparse
import json
from pathlib import Path
from time import sleep

import requests
from bs4 import BeautifulSoup

from parse_tululu import download_books_and_images


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


def get_book_ids(genre_url: str, pages: tuple) -> list:
    book_ids = []
    for page in range(*pages):
        first_reconnection = True
        while True:
            try:
                # page_url has to end with '/',
                # or else check_for_redirect() won't work
                page_url = f'{genre_url}{page}/'
                response = requests.get(page_url)
                response.raise_for_status()
                check_for_page_redirect(response, page)
                if not first_reconnection:
                    print('Connection is restored.')
            except requests.exceptions.ConnectionError as connect_err:
                print(f'Connection failure: {connect_err};')
                print(f'Page {page}')
                if first_reconnection:
                    print('Retry in 5 seconds')
                    sleep(5)
                    first_reconnection = False
                else:
                    print('Retry in 15 seconds')
                    sleep(15)
            except requests.HTTPError as err:
                print(err)
                continue
            else:
                soup = BeautifulSoup(response.text, 'lxml')
                for book in soup.select('body .d_book'):
                    book_id = book.select_one('a')['href'].strip('/b')
                    book_ids.append(book_id)
                break
    return book_ids


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
    parser.add_argument('--start_page', type=int, default=700)
    parser.add_argument('--end_page', type=int, default=final_page)
    parser.add_argument('--dest_folder', default='media')
    parser.add_argument('--skip_txt', action='store_true')
    parser.add_argument('--skip_img', action='store_true')
    parser.add_argument('--json_path', default='media')

    args = parser.parse_args()
    download_genre_books(args, sci_fi_url)


if __name__ == '__main__':
    main()
