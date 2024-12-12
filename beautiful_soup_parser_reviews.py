from bs4 import BeautifulSoup
import re

with open('./text.txt', 'r') as file:
    text = file.read()
soup = BeautifulSoup(text, 'html.parser')
review_ratings = soup.find_all('div', class_='y-css-dnttlc')
review_dates = soup.find_all('span', class_="y-css-1d8mpv1")
reviews = soup.find_all('p', class_=re.compile('comment__'))
for rating, date, review in zip(review_ratings, review_dates, reviews):
    string = str(review.span).replace('<br/><br/>', '')
    print(rating['aria-label'])
    print(date.string)
    print (re.sub('\<.*?\>', '', string))