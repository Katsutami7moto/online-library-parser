import argparse
from pathlib import Path
from time import sleep
from urllib.parse import urljoin, urlsplit, unquote

import requests
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename


def create_book_path(books_dir: Path, book_title: str) -> Path:
    file_name = f'{sanitize_filename(book_title).strip(".")}.txt'
    return books_dir.joinpath(file_name)


def create_image_path(images_dir: Path, image_url: str) -> Path:
    file_name = sanitize_filename(get_file_name_from_url(image_url))
    return images_dir.joinpath(file_name)


def check_for_redirect(response: requests.Response, book_id):
    if response.history:
        err_msg = f'There is no book with ID {book_id}'
        raise requests.HTTPError(err_msg)


def get_file_name_from_url(url: str) -> str:
    return Path(unquote(urlsplit(url).path)).name


def get_book_soup(book_id) -> BeautifulSoup:
    base_url = 'https://tululu.org'

    # book_url has to end with '/', or else check_for_redirect() won't work
    book_url = urljoin(base_url, f'b{book_id}/')
    response = requests.get(book_url)
    response.raise_for_status()
    check_for_redirect(response, book_id)
    return BeautifulSoup(response.text, 'lxml')


def get_image_url(book_soup: BeautifulSoup) -> str:
    book_url = book_soup.select_one('.bookimage a')['href']
    base_url = urljoin('https://tululu.org', book_url)
    image_src = book_soup.select_one('.bookimage a img')['src']
    return urljoin(base_url, image_src)


def get_book_title_and_author(book_soup: BeautifulSoup) -> tuple:
    title_soup = book_soup.select_one('html head title')
    *title, author = title_soup.text.split(' - ')
    title: str = ' '.join(title).strip()
    author: str = author.split(',')[0].strip()
    return title, author


def get_book_comments(book_soup: BeautifulSoup) -> list:
    comments_soup = book_soup.select('body .texts')
    return [comment.contents[-1].text for comment in comments_soup]


def get_book_genres(book_soup: BeautifulSoup) -> list:
    genres_soup = book_soup.select('body span.d_book a')
    return [genre.text for genre in genres_soup]


def parse_book_page(book_soup: BeautifulSoup) -> dict:
    title, author = get_book_title_and_author(book_soup)
    genres = get_book_genres(book_soup)
    comments = get_book_comments(book_soup)
    parsed_book = {
        'title': title,
        'author': author,
        'image_path': '',
        'book_path': '',
        'genres': genres,
        'comments': comments,
    }
    return parsed_book


def download_txt(book_path: Path, book_id):
    base_url = 'https://tululu.org/txt.php'
    payload = {'id': book_id}
    response = requests.get(base_url, params=payload)
    response.raise_for_status()
    check_for_redirect(response, book_id)
    with open(book_path, 'w') as file:
        file.write(response.text)


def download_image(image_path: Path, url: str):
    response = requests.get(url)
    response.raise_for_status()
    with open(image_path, 'wb') as file:
        file.write(response.content)


def download_books_and_images(book_ids) -> list:
    books_dir = Path('books')
    books_dir.mkdir(parents=True, exist_ok=True)
    images_dir = Path('images')
    images_dir.mkdir(parents=True, exist_ok=True)
    parsed_books = []
    for book_id in book_ids:
        first_reconnection = True
        while True:
            try:
                book_soup = get_book_soup(book_id)
                parsed_book = parse_book_page(book_soup)
                book_path = create_book_path(books_dir, parsed_book['title'])
                image_url = get_image_url(book_soup)
                image_path = create_image_path(images_dir, image_url)

                download_txt(book_path, book_id)
                download_image(image_path, image_url)

                parsed_book['book_path'] = str(book_path)
                parsed_book['image_path'] = str(image_path)
                parsed_books.append(parsed_book)
                break
            except requests.exceptions.ConnectionError as connect_err:
                print(f'Connection failure: {connect_err};')
                print(f'book ID: {book_id}')
                if first_reconnection:
                    print('Retry in 5 seconds')
                    sleep(5)
                    first_reconnection = False
                else:
                    print('Retry in 15 seconds')
                    sleep(15)
            except requests.HTTPError as err:
                print(err)
                break
    return parsed_books


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--start_id', type=int, default=1)
    parser.add_argument('-e', '--end_id', type=int, default=10)
    args = parser.parse_args()
    book_ids = range(args.start_id, args.end_id + 1)
    download_books_and_images(book_ids)


if __name__ == '__main__':
    main()
