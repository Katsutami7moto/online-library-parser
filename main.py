from pathlib import Path
from urllib.parse import urljoin, urlsplit, unquote

import requests
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename


def check_for_redirect(response: requests.Response, number: int):
    redirect = response.history
    if redirect:
        err_msg = f'There is no book with ID {number}.'
        raise requests.HTTPError(err_msg)


def get_file_name_from_url(url: str) -> str:
    return Path(unquote(urlsplit(url).path)).name


def get_books_title(book_id: int) -> tuple:
    base_url = 'https://tululu.org'
    book_url = urljoin(base_url, f'b{book_id}')
    response = requests.get(book_url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    title_soup_text = soup.find('html').find('head').find('title').text
    if ' - ' not in title_soup_text:
        return '', ''
    title, author = title_soup_text.split(' - ')
    title: str = title.strip()
    # author: str = author.split(',')[0].strip()
    image_soup = soup.find('body').find('div', class_='bookimage').find('img')
    image_url = urljoin(base_url, image_soup.attrs['src'])
    requests.get(image_url).raise_for_status()
    return title, image_url


def download_txt(books_dir: Path, file_number: int) -> str:
    url = 'https://tululu.org/txt.php'
    payload = {'id': file_number}
    response = requests.get(url, params=payload)
    response.raise_for_status()
    check_for_redirect(response, file_number)
    book_title: str = get_books_title(file_number)[0]
    file_name = f'{file_number}. {sanitize_filename(book_title)}.txt'
    file_path = books_dir.joinpath(file_name)
    with open(file_path, 'w') as file:
        file.write(response.text)
    return str(file_path)


def download_image(images_dir: Path, url: str):
    response = requests.get(url)
    response.raise_for_status()
    file_path = images_dir.joinpath(get_file_name_from_url(url))
    with open(file_path, 'wb') as file:
        file.write(response.content)


def download_books_with_titles():
    books_dir = Path('books')
    books_dir.mkdir(parents=True, exist_ok=True)
    images_dir = Path('images')
    images_dir.mkdir(parents=True, exist_ok=True)
    for number in range(10):
        file_number = number + 1
        try:
            # download_txt(url, books_dir, file_number)
            title, img_url = get_books_title(file_number)
            if img_url:
                download_image(images_dir, img_url)
        except requests.HTTPError as err:
            print(err)


def main():
    download_books_with_titles()


if __name__ == '__main__':
    main()
