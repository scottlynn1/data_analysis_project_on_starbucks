import psycopg2
from psycopg2 import sql
import csv

conn = psycopg2.connect(database = "starbucksproject", 
                        user = "scott", 
                        host = 'localhost',
                        password = "Atlas234^",
                        port = 5432)

cur = conn.cursor()
try:
  cur.execute("SELECT COUNT(rating) FROM reviews WHERE address = 'WY';")
  for row in cur:
    print(row)
finally:
  cur.close()
  conn.close()
print("success")