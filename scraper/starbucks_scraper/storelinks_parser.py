from bs4 import BeautifulSoup
import re
# simple program to format raw abtracted store links into a format suited to my needs
with open('./links_2.txt', 'r') as file:
    text = file.read()
soup = BeautifulSoup(text, 'html.parser')

def uniq_links(tag):
    return tag.has_attr('name') and re.search('/biz/', tag['href'])

links = soup.find_all(uniq_links)

with open('abstracted_links_2.txt', 'a') as file:
    for link in links:
        link = str(link)
        link = re.search('href\=\".*?\"', link).group(0)
        file.write("%s\n" % re.search('/.*?\=starbucks', link).group(0))