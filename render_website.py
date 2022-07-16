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
    paged_catalog = list(chunked(chunked(get_books_catalog('media'), 2), 6))
    pages_links = {number: f'./index{number}.html'
                   for number in range(1, len(paged_catalog) + 1)}
    for number, page in enumerate(paged_catalog, 1):
        previous_page = f'./index{number - 1}.html' if number > 1 else None
        next_page = (f'./index{number + 1}.html'
                     if number < len(paged_catalog) else None)
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


def main():
    on_reload()
    server = Server()
    server.watch('template.html', on_reload)
    server.serve(root='.', default_filename='pages/index1.html')


if __name__ == "__main__":
    main()
