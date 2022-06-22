import os
from pathlib import Path

import requests

books_path = 'books'
books_dir = Path(books_path)
books_dir.mkdir(parents=True, exist_ok=True)

start_number = 32168
books = []
while len(books) < 10:
    file_number = len(books) + 1
    book_number = start_number + file_number
    url = f'https://tululu.org/txt.php?id={book_number}'
    response = requests.get(url)
    try:
        response.raise_for_status()
        file_name = f'id{file_number}.txt'
        file_path = books_dir.joinpath(file_name)
        with open(file_path, 'w') as file:
            file.write(response.text)
    except Exception as e:
        print(e)
    books = tuple(os.walk(books_path))[0][2]
