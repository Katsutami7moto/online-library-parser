import json
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape, Template
from livereload import Server
from more_itertools import chunked


def get_books_catalog(path: str) -> list:
    json_path = Path(path)
    json_path.mkdir(parents=True, exist_ok=True)
    file_path = json_path.joinpath('books_catalog.json')
    with open(file_path, 'r', encoding='utf8') as file:
        return json.load(file)


def render_pages(paged_catalog: list, template: Template, pages_path: Path):
    pages_links: dict = {
        number: f'./index{number}.html'
        for number in range(1, len(paged_catalog) + 1)
    }
    for number, page in enumerate(paged_catalog, 1):
        rendered_page = template.render(
            current_page_num=number,
            catalog=page,
            pages_links=pages_links
        )
        file_path = pages_path.joinpath(f'index{number}.html')
        with open(file_path, 'w', encoding="utf8") as file:
            file.write(rendered_page)


def on_reload():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    pages_path = Path('pages')
    pages_path.mkdir(parents=True, exist_ok=True)
    template = env.get_template('template.html')
    book_cards_in_row = 2
    rows_in_page = 6
    paged_catalog = list(
        chunked(
            chunked(
                get_books_catalog('media'),
                book_cards_in_row
            ),
            rows_in_page
        )
    )
    render_pages(paged_catalog, template, pages_path)


def main():
    on_reload()
    server = Server()
    server.watch('template.html', on_reload)
    server.serve(root='pages', default_filename='index1.html')


if __name__ == "__main__":
    main()
