from bs4 import BeautifulSoup
import re
import csv


with open('./text.txt', 'r') as file:
    text = file.read()
soup = BeautifulSoup(text, 'html.parser')
review_ratings = soup.find_all('div', class_='y-css-dnttlc')
review_dates = soup.find_all('span', class_="y-css-1d8mpv1")
reviews = soup.find_all('p', class_=re.compile('comment__'))
with open('review_info.csv', mode='a') as csv_file:
    csv_writer = csv.writer(csv_file, delimiter='~', quoting=csv.QUOTE_NONE, escapechar='`')
    for rating, date, review in zip(review_ratings, review_dates, reviews):
        string = str(review.span).replace('<br/><br/>', '')
        rating = rating['aria-label']
        date = date.string
        review = re.sub('\<.*?\>', '', string)
        csv_writer.writerow([rating, date, review])
