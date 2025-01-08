import psycopg2
from psycopg2 import sql
import csv
import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.probability import FreqDist
from os import environ


conn = psycopg2.connect(database = "starbucksproject", 
                        user = "avnadmin", 
                        host = 'first-project-starbucksproject.h.aivencloud.com',
                        password = environ.get('PASSWORD'),
                        port = 11273
                      )

cur = conn.cursor()
try:
  cur.execute("SELECT review FROM starbucks_reviews WHERE rating = '1' AND review LIKE '%drive-thru%';")
  text = ''
  for row in cur:
    text = text + ' ' + row[0]
  print(text)
  tokens = word_tokenize(text.lower())
  filtered_tokens = [token for token in tokens if token not in stopwords.words('english') and token.isalpha()]
  lemmatizer = WordNetLemmatizer()
  lemmatized_tokens = [lemmatizer.lemmatize(token) for token in filtered_tokens]

  """
  finder = nltk.collocations.TrigramCollocationFinder.from_words(lemmatized_tokens)
  grams = finder.ngram_fd.most_common(100)
  for gram in grams:
    count = gram[1]
    print(count)
    words = str(gram[0]).replace("'", '').lstrip('(').rstrip(')')
    print(words)
    cur.execute("INSERT INTO common_negative_words (words, occurrences) VALUES (%s, %s);", (words, count))
"""

finally:
  conn.commit()
  cur.close()
  conn.close()
print("\nsuccess")