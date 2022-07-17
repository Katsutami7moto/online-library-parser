# online-library-parser

A tool to parse and download books from [tululu.org](https://tululu.org/)

## How to install

Python3 should be already installed.
Download the [ZIP archive](https://github.com/Katsutami7moto/online-library-parser/archive/refs/heads/main.zip) of the code and unzip it.
Then open terminal form unzipped directory and use `pip` (or `pip3`, if there is a conflict with Python2) to install dependencies:
```commandline
pip install -r requirements.txt
```

## How to use

This projects contains two scripts: `parse_tululu.py` and 
`parse_tululu_category.py`.

Both scripts download book texts in *.txt format and book covers as pictures (usually in *.jpg format), if a book has a cover. Texts are store in 'books' directory, covers - in 'images' directory; both directories will be created automatically.

If the text file for a book is unavailable, the tool will continue downloading next books; the cover for this book will also not be downloaded, even if there is one.

The differences of these two scripts are described below.

### Parse and download books by ID

You can run the first script in two ways:

- without command line arguments, to download books by first 10 ids:
```commandline
python3 parse_tululu.py
```
- with two command line arguments, to download books from `start_id` to `end_id`, inclusively:
```commandline
python3 parse_tululu.py --start_id 20 --end_id 30
```
or in short notation:
```commandline
python3 parse_tululu.py -s 20 -e 30
```
`start_id` must be less than `end_id` and both arguments must be provided.

### Parse and download sci-fi books by pages

This script has several optional arguments:

- `--start_page` (default value is 1) and `--end_page` (default value is the automatically detected numer of the last page) define, what pages of sci-fi category books will be downloaded from, inclusively:
```commandline
python3 parse_tululu_category.py --start_page 238 --end_page 347
```
- `--dest_folder` (default value is the folder where the script is stored) defines where directories for book texts and covers will be created:
```commandline
python3 parse_tululu_category.py --start_page 238 --end_page 347 --dest_folder /home/username/grandpa_scifi_books/files
```
- `--json_path` (default value is the folder where the script is stored) defines where the `books_catalog.json` file with the information about those books will be created:
```commandline
python3 parse_tululu_category.py --start_page 238 --end_page 347 --dest_folder /home/username/grandpa_scifi_books/files --json_path /home/username/grandpa_scifi_books/metadata
```
- `--skip_txt` and `--skip_img`, if added, disable download of text files or pictures, respectively:
```commandline
python3 parse_tululu_category.py --start_page 238 --end_page 347 --json_path /home/username/grandpa_scifi_books/metadata --skip_txt --skip_img
```

### Create website

1. Download books from, e.g., first 5 pages with this command:
```commandline
python3 parse_tululu_category.py --end_page 5
```
2. Run this command to create pages of the website using information from `books_catalog.json` file:
```commandline
python3 render_website.py
```
You can open the website [here](http://127.0.0.1:5500/) while it's local, or stop the script and open pages from `pages` directory. Press `Читать` button to open text filr of a book.

## GitHub Pages website

An example of the webite is available [here](https://katsutami7moto.github.io/online-library-parser/pages/index1.html).

## Project Goals

The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/).
