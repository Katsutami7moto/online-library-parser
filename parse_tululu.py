import argparse
from pathlib import Path
from time import sleep
from urllib.parse import urljoin, urlsplit, unquote

import requests
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename


def check_for_redirect(response: requests.Response, number: int):
    if response.history:
        err_msg = f'There is no book with ID {number}'
        raise requests.HTTPError(err_msg)


def get_file_name_from_url(url: str) -> str:
    return Path(unquote(urlsplit(url).path)).name


def get_book_soup(book_id: int) -> BeautifulSoup:
    base_url = 'https://tululu.org'

    # book_url has to end with '/', or else check_for_redirect() won't work
    book_url = urljoin(base_url, f'b{book_id}/')
    response = requests.get(book_url)
    response.raise_for_status()
    check_for_redirect(response, book_id)
    return BeautifulSoup(response.text, 'lxml')


def get_image_url(book_soup: BeautifulSoup) -> str:
    bookimage_soup = book_soup.find('div', class_='bookimage')
    book_url = bookimage_soup.find('a')['href']
    base_url = urljoin('https://tululu.org', book_url)
    image_src = bookimage_soup.find('img')['src']
    return urljoin(base_url, image_src)


def get_book_title_and_author(book_soup: BeautifulSoup) -> tuple:
    title_soup = book_soup.find('html').find('head').find('title')
    *title, author = title_soup.text.split(' - ')
    title: str = ' '.join(title).strip()
    author: str = author.split(',')[0].strip()
    return title, author


def get_book_comments(book_soup: BeautifulSoup) -> list:
    comments_soup = book_soup.find('body').find_all('div', class_='texts')
    return [comment.contents[-1].text for comment in comments_soup]


def get_book_genres(book_soup: BeautifulSoup) -> list:
    genres_soup = book_soup.find('body').find('span', class_='d_book')
    return [genre.text for genre in genres_soup.find_all('a')]


def parse_book_page(book_soup: BeautifulSoup) -> dict:
    title, author = get_book_title_and_author(book_soup)
    image_url = get_image_url(book_soup)
    comments = get_book_comments(book_soup)
    genres = get_book_genres(book_soup)
    parsed_book = {
        'title': title,
        'author': author,
        'genres': genres,
        'image': image_url,
        'comments': comments,
    }
    return parsed_book


def download_txt(books_dir: Path, book_id: int, book_title: str):
    base_url = 'https://tululu.org/txt.php'
    payload = {'id': book_id}
    response = requests.get(base_url, params=payload)
    response.raise_for_status()
    check_for_redirect(response, book_id)
    file_name = f'{book_id}. {sanitize_filename(book_title)}.txt'
    file_path = books_dir.joinpath(file_name)
    with open(file_path, 'w') as file:
        file.write(response.text)


def download_image(images_dir: Path, url: str):
    response = requests.get(url)
    response.raise_for_status()
    file_name = sanitize_filename(get_file_name_from_url(url))
    file_path = images_dir.joinpath(file_name)
    with open(file_path, 'wb') as file:
        file.write(response.content)


def download_book_and_image(book_id: int, books_dir: Path, images_dir: Path):
    first_reconnection = True
    while True:
        try:
            book_soup = get_book_soup(book_id)
            parsed_book = parse_book_page(book_soup)
            download_txt(books_dir, book_id, parsed_book['title'])
            download_image(images_dir, parsed_book['image'])
            break
        except requests.exceptions.ConnectionError as connect_err:
            print(f'Connection failure: {connect_err}; book ID: {book_id}')
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


def download_books_and_images(start: int, end: int):
    books_dir = Path('books')
    books_dir.mkdir(parents=True, exist_ok=True)
    images_dir = Path('images')
    images_dir.mkdir(parents=True, exist_ok=True)
    any(
        download_book_and_image(book_id, books_dir, images_dir)
        for book_id in range(start, end + 1)
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--start_id', type=int, default=1)
    parser.add_argument('-e', '--end_id', type=int, default=10)
    args = parser.parse_args()
    download_books_and_images(args.start_id, args.end_id)


if __name__ == '__main__':
    main()
