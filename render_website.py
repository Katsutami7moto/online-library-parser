import json
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape


def get_books_catalog(path: str) -> list[dict]:
    json_path = Path(path)
    json_path.mkdir(parents=True, exist_ok=True)
    file_path = json_path.joinpath('books_catalog.json')
    with open(file_path, 'r', encoding='utf8') as file:
        json_str = file.read()
        return json.loads(json_str)


def main():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('template.html')

    catalog = get_books_catalog('media')

    rendered_page = template.render(
        catalog=catalog
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == "__main__":
    main()
