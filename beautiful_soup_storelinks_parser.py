from bs4 import BeautifulSoup
import re

with open('./links.txt', 'r') as file:
    text = file.read()
soup = BeautifulSoup(text, 'html.parser')

def uniq_links(tag):
    return tag.has_attr('name') and re.search('/biz/', tag['href'])

links = soup.find_all(uniq_links)

with open('abstracted_links.txt', 'a') as file:
    for link in links:
        link = str(link)
        link = re.search('href\=\".*?\"', link).group(0)
        file.write("%s\n" % re.search('/.*?\=starbucks', link).group(0))