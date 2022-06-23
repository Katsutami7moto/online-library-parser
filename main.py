from pathlib import Path

import requests
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename


def check_for_redirect(response: requests.Response, number: int):
    redirect = response.history and '?' not in response.url
    if redirect:
        err_msg = f'There is no book with ID {number}.'
        raise requests.HTTPError(err_msg)


def get_books_title(book_id: int) -> tuple:
    url = f'https://tululu.org/b{book_id}'
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    title_soup_text = soup.find('html').find('head').find('title').text
    title, author = title_soup_text.split(' - ')
    title: str = title.strip()
    author: str = author.split(',')[0].strip()
    return title, author


def download_txt(url: str, books_dir: Path, file_number: int) -> str:
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


def download_books_with_titles(folder: str = 'books'):
    books_dir = Path(folder)
    books_dir.mkdir(parents=True, exist_ok=True)
    for number in range(10):
        file_number = number + 1
        url = 'https://tululu.org/txt.php'
        try:
            download_txt(url, books_dir, file_number)
        except requests.HTTPError as err:
            print(err)
        finally:
            continue


def main():
    download_books_with_titles()


if __name__ == '__main__':
    main()
