# online-library-parser

A tool to parse and download books from [tululu.org](https://tululu.org/)

### How to install

Python3 should be already installed.
Download the [ZIP archive](https://github.com/Katsutami7moto/online-library-parser/archive/refs/heads/main.zip) of the code and unzip it.
Then open terminal form unzipped directory and use `pip` (or `pip3`, if there is a conflict with Python2) to install dependencies:
```commandline
pip install -r requirements.txt
```

### How to use

This script downloads book texts in *.txt format and book covers as pictures (usually in *.jpg format), if a book has a cover. Texts are store in 'books' directory, covers - in 'images' directory; both directories will be created automatically in the unzipped directory of this tool.
If the text file for a book is unavailable, the tool will continue downloading next books; the cover for this book will also not be downloaded, even if there is one.

You can run the tool in two ways:

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

### Project Goals

The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/).
