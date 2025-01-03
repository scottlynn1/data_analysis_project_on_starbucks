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

conn = psycopg2.connect(database = "starbucksproject", 
                        user = "scott", 
                        host = 'localhost',
                        password = "Atlas234^",
                        port = 5432)

cur = conn.cursor()
try:
  cur.execute("SELECT review FROM reviews WHERE address = 'FL' and rating = '5';")
  text = ''
  for row in cur:
    text = text + ' ' + row[0]
  print(text)
  tokens = word_tokenize(text.lower())
  filtered_tokens = [token for token in tokens if token not in stopwords.words('english') and token.isalpha()]
  lemmatizer = WordNetLemmatizer()
  lemmatized_tokens = [lemmatizer.lemmatize(token) for token in filtered_tokens]
  finder = nltk.collocations.TrigramCollocationFinder.from_words(lemmatized_tokens)
  print(finder.ngram_fd.most_common(100))
#  print(nltk.Text(tokens).concordance("white chocolate mocha", lines = 5))
#  processed_text = ' '.join(lemmatized_tokens)

#  fq=FreqDist(token for token in lemmatized_tokens)
#  print(fq.most_common(20)) 

    
finally:
  cur.close()
  conn.close()
print("\nsuccess")