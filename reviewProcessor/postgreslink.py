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

# This program initaites a connection to the postgres instance in which all the review data was stores and analyze review data with NLP tools
# the query parameter can be used to filter which reviews are inluded in the analysis
# this can be by date, date, or rating, or any combination of the three
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
      # this inserts the ngrams and there associated counts into any table of your choosing
      # this programm was used several times using different query parameters (filter context) to create several different tables titled based on the filter context
      # for example this last run was used to make a table of ngrams for all reviews of 1 star ratings dating before 2014
      cur.execute("INSERT INTO negative_words_before_2014 (words, occurrences) VALUES (%s, %s);", (words, count))
    

  finally:
    cur.close()
    conn.commit()

    conn.close()
  print("\nsuccess")


# the command line argument is the sql query string to search the main review table based on any filter context you see fit
if __name__ == "__main__":
  get_reviews(sys.argv[1])