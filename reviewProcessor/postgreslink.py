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
import sys

def get_reviews(query):
  conn = psycopg2.connect(database = "starbucksproject", 
                          user = "avnadmin", 
                          host = 'first-project-starbucksproject.h.aivencloud.com',
                          password = environ.get('PASSWORD'),
                          port = 11273
                        )

  cur = conn.cursor()
  try:
    cur.execute(query)
    text = ''
    for row in cur:
      text = text + ' ' + row[0]

    
    tokens = word_tokenize(text.lower())
    filtered_tokens = [token for token in tokens if token not in stopwords.words('english') and token.isalpha()]
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in filtered_tokens]

    
    finder = nltk.collocations.TrigramCollocationFinder.from_words(lemmatized_tokens)
    grams = finder.ngram_fd.most_common(100)
    for gram in grams:
      count = gram[1]
      print(count)
      words = str(gram[0]).replace("'", '').lstrip('(').rstrip(')')
      print(words)
      cur.execute("INSERT INTO negative_words_before_2014 (words, occurrences) VALUES (%s, %s);", (words, count))
    

  finally:
    cur.close()
    conn.commit()

    conn.close()
  print("\nsuccess")



if __name__ == "__main__":
  get_reviews(sys.argv[1])