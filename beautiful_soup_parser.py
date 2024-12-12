from bs4 import BeautifulSoup
import re

with open('./links.txt', 'r') as file:
    text = file.read()
print(text)
soup = BeautifulSoup(text, 'html.parser')

def uniq_links(tag):
    return tag.has_attr('name') and re.search('/biz/', tag['href'])
links = soup.find_all(uniq_links)
for link in links:
    link = str(link)
    print(re.search('href\=\".*?\"', link).group(0))