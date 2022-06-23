from pathlib import Path

import requests


def check_for_redirect(response: requests.Response):
    redirect = response.history and '?' not in response.url
    if redirect:
        raise requests.HTTPError


def main():
    books_path = 'books'
    books_dir = Path(books_path)
    books_dir.mkdir(parents=True, exist_ok=True)

    for number in range(10):
        file_number = number + 1
        payload = {'id': file_number}
        url = 'https://tululu.org/txt.php'
        response = requests.get(url, params=payload)
        try:
            response.raise_for_status()
            check_for_redirect(response)
        except requests.HTTPError:
            pass
        else:
            file_name = f'id{file_number}.txt'
            file_path = books_dir.joinpath(file_name)
            with open(file_path, 'w') as file:
                file.write(response.text)


if __name__ == '__main__':
    main()
