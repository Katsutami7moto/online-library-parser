import json
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked


def get_books_catalog(path: str) -> list[dict]:
    json_path = Path(path)
    json_path.mkdir(parents=True, exist_ok=True)
    file_path = json_path.joinpath('books_catalog.json')
    with open(file_path, 'r', encoding='utf8') as file:
        json_str = file.read()
        return json.loads(json_str)


def on_reload():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    pages_path = Path('pages')
    pages_path.mkdir(parents=True, exist_ok=True)
    template = env.get_template('template.html')
    catalog = list(chunked(get_books_catalog('media'), 2))
    paged_catalog = list(chunked(catalog, 6))
    for number, page in enumerate(paged_catalog, 1):
        rendered_page = template.render(
            catalog=page,
            page_title=f'Собрание НФ-худлита, страница {number}'
        )
        file_name = f'index{number if number != 1 else ""}.html'
        file_path = pages_path.joinpath(file_name)
        with open(file_path, 'w', encoding="utf8") as file:
            file.write(rendered_page)


def main():
    on_reload()
    server = Server()
    server.watch('template.html', on_reload)
    server.serve(root='.', default_filename='pages/index.html')


if __name__ == "__main__":
    main()
