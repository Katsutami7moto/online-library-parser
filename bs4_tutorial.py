import requests
from bs4 import BeautifulSoup


url = 'https://www.franksonnenbergonline.com/blog/are-you-grateful/'
response = requests.get(url)
response.raise_for_status()

soup = BeautifulSoup(response.text, 'lxml')
post_title_tag = soup.find('main').find('header').find('h1')
post_title_text = post_title_tag.text
print(post_title_text)
post_img_src = soup.find('img', class_='attachment-post-image')['src']
print(post_img_src)
post_text = soup.find('div', class_='entry-content').text
print(post_text)
