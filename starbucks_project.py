from bs4 import BeautifulSoup
import requests
import re
import csv
import time
import random
import json


#for city, state in zip(cities, states)

#f'https://www.yelp.com/search?find_desc=starbucks&find_loc={city}%2C+{state}'
session = requests.Session()
request_headers = {
    'authority': 'www.yelp.com',
    'method': 'GET',
    'path': '/search?find_desc=starbucks&find_loc=Montgomery%2C+AL',
    'scheme': 'https',
    'Content-Type': 'text/html; charset=UTF-8',
    'Referer': 'https://www.yelp.com/',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Sec-Ch-Device-Memory': '8',
    'Sec-Ch-Ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    'Sec-Ch-Ua-Platform': "Linux",
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
  }

url = 'https://www.yelp.com/search?find_desc=starbucks&find_loc=Tallahassee%2C+FL'
apikey = 'a1e4a7b9f59af93437b837ce98072413fb9ed6e1'
params = {
    'url': url,
    'apikey': apikey,
	'js_render': 'true',
	'premium_proxy': 'true',
	'autoparse': 'true',
}
response = session.get('https://api.zenrows.com/v1/', params=params, headers=request_headers)
print(json.dumps(dict(response.headers), sort_keys=True, indent=4))
if response:
    print("Success!")
else:
    raise Exception(f"Non-success status code: {response.status_code}")

text = BeautifulSoup(response.text, 'html.parser')
print(text)
links = text.find_all(href=re.compile('biz'))
print(links)
