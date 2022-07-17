import json
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape, Template
from livereload import Server
from more_itertools import chunked


def get_books_catalog(path: str) -> list[dict]:
    json_path = Path(path)
    json_path.mkdir(parents=True, exist_ok=True)
    file_path = json_path.joinpath('books_catalog.json')
    with open(file_path, 'r', encoding='utf8') as file:
        json_str = file.read()
        return json.loads(json_str)


def render_pages(paged_catalog: list[list[list[dict]]],
                 pages_links: dict[int, str], template: Template,
                 pages_num: int, pages_path: Path):
    for number, page in enumerate(paged_catalog, 1):
        previous_page = pages_links[number - 1] if number > 1 else None
        next_page = pages_links[number + 1] if number < pages_num else None
        page_title = f'Собрание НФ-худлита, страница {number}'
        rendered_page = template.render(
            current_page_num=number,
            catalog=page,
            page_title=page_title,
            pages_links=pages_links,
            previous_page=previous_page,
            next_page=next_page
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
    pages_num = len(paged_catalog)
    pages_links: dict[int, str] = {
        number: f'./index{number}.html'
        for number in range(1, pages_num + 1)
    }
    render_pages(paged_catalog, pages_links, template, pages_num, pages_path)


def main():
    on_reload()
    server = Server()
    server.watch('template.html', on_reload)
    server.serve(root='pages', default_filename='index1.html')


if __name__ == "__main__":
    main()
