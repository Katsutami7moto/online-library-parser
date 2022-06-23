from pathlib import Path

import requests
from bs4 import BeautifulSoup


def check_for_redirect(response: requests.Response):
    redirect = response.history and '?' not in response.url
    if redirect:
        err_msg = 'There is no book with such ID.'
        raise requests.HTTPError(err_msg)


def download_books():
    books_path = 'books'
    books_dir = Path(books_path)
    books_dir.mkdir(parents=True, exist_ok=True)

    for number in range(10):
        file_number = number + 1
        payload = {'id': file_number}
        url = 'https://tululu.org/txt.php'
        response = requests.get(url, params=payload)
        response.raise_for_status()
        check_for_redirect(response)
        file_name = f'id{file_number}.txt'
        file_path = books_dir.joinpath(file_name)
        with open(file_path, 'w') as file:
            file.write(response.text)


def get_books_title(book_id: int) -> str:
    url = f'https://tululu.org/b{book_id}'
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    title_soup_text = soup.find('html').find('head').find('title').text
    title, author = title_soup_text.split('-')
    title: str = title.strip()
    author: str = author.split(',')[0].strip()
    return f"""Заголовок: {title}
Автор: {author}"""


def main():
    try:
        print(get_books_title(55555))
    except requests.HTTPError as err:
        print(err)


if __name__ == '__main__':
    main()
