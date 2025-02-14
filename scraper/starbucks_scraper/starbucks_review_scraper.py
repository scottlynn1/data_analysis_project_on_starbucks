from selenium.webdriver.common.by import By
from os import environ
from selenium.webdriver import Remote, ChromeOptions as Options
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection as Connection
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import re
import csv
import sys
# this file scrapes a list of provided stores for every review at each store
# inluding rating, date, city and state, and review content
AUTH = environ.get('AUTH', default='USER:PASS')
# initiate list and full with links to every store abstracted from starbucks_storelinks_scraper.py
stores = []
last_store = ''
with open('./abstracted_links.txt', 'r') as file:
    for store in file:
        store = store.rstrip('\n')
        stores.append(f'https://www.yelp.com{store}')

# main scraper function
def scrape(store):
    global last_store
    # initiate connection to bright data proxy server
    if AUTH == 'USER:PASS':
        raise Exception('Provide Scraping Browsers credentials in AUTH ' +
                        'environment variable or update the script.')
    print('Connecting to Browser...')
    server_addr = f'https://{AUTH}@brd.superproxy.io:9515'
    connection = Connection(server_addr, 'goog', 'chrome')
    driver = Remote(connection, options=Options())
    # connection initiated
    try:
        # captcha solving loop
        print(f'Connected! Navigating to {store}...')
        status = 'solve_failed'
        while (status == 'solve_failed' or status == 'invalid'):
            print(f'Connected! Navigating to {store}...')
            driver.get(store)
            print('Navigated! Waiting captcha to detect and solve...')
            result = driver.execute('executeCdpCommand', {
                'cmd': 'Captcha.waitForSolve',
                'params': {'detectTimeout': 10 * 1000},
            })
            status = result['value']['status']
            print(f'Captcha status: {status}')
        # end captcha solving loop
        # while loop to loop through every page on current store provided as argument until next page element is not found
        while True:
            print('pulling review information')
            # wait for page elements to load
            driver.implicitly_wait(10)
            # try two different element tags to scrape with BeautifulSoup
            try:
                content = driver.find_element(By.ID, 'main-content').get_attribute('innerHTML')
            except NoSuchElementException:
                print('could not find main tag, searching parent')
                driver.implicitly_wait(3)
                content = driver.find_element(By.CLASS_NAME, 'y-css-13kng0r').get_attribute('innerHTML')
            # grab each element that contains date, location, rating, and review
            soup = BeautifulSoup(content, 'html.parser')
            address = soup.find('address').find_all('span')[-1:]
            address = address[0].string
            review_ratings = soup.find_all('div', class_='y-css-dnttlc')
            review_dates = soup.find_all('span', class_="y-css-1d8mpv1")
            reviews = soup.find_all('p', class_=re.compile('comment__'))
            last_store = store
            # write data to file
            print(f'writing from current store {last_store}')
            with open('review_info.csv', mode='a') as csv_file:
                csv_writer = csv.writer(csv_file, delimiter='~', quoting=csv.QUOTE_NONE, escapechar='`')
                for rating, date, review in zip(review_ratings, review_dates, reviews):
                    string = str(review.span).replace('<br/><br/>', '')
                    rating = rating['aria-label'].rstrip(' star rating')
                    date = date.string
                    review = re.sub('\<.*?\>', '', string)
                    csv_writer.writerow([address, rating, date, review])
            print(f'review infromation written to file from store {last_store}')
            # close file
            # attempt to find next page element
            # otherwise break loop and exit function
            try:
                print('searching for "next" page')
                next_button = driver.find_element(By.CLASS_NAME, 'next-link')
                store = next_button.get_attribute("href")
                driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
                driver.implicitly_wait(3)
                next_button.click()
            except NoSuchElementException:
                print("No Such Element or End of Review list")
                break
            # captcha solving loop
            print(f'Navigating to {last_store}...')
            status = 'solve_failed'
            while (status == 'solve_failed' or status == 'invalid'):
                print('Navigated! Waiting captcha to detect and solve...')
                result = driver.execute('executeCdpCommand', {
                    'cmd': 'Captcha.waitForSolve',
                    'params': {'detectTimeout': 10 * 1000},
                })
                status = result['value']['status']
                print(f'Captcha status: {status}')
            # end captcha solving loop
            
    finally:
        driver.quit()

# this function was defined due to several errors on bright data's side that were out of my control and would exit my program
# this function catches a general error given by bright data and then calls itself recursively from the "last_store"
# I did this to reduce the amount of times I had to restart the program
# Maybe not the best fix because it may lead to other issues such as stack overflows but it allowed for less interuptions in the scraping process
def exception_loop(number):
    global stores
    global last_store
    stores = stores[int(number):]
    print(len(stores))
    last_store = stores[0]
    print(f"record: {last_store}")
    try:
        for i, store in enumerate(stores):
            number = i
            scrape(store)
    except WebDriverException:
        print(f"server failed, restarting from: {last_store}")
        scrape(last_store)
        print("restarting exception loop")
        exception_loop(number+1)

# the scraper would still exit so this function allows me to restart where I left off by provoding command line arguments
#argv[1] being the line in my "abstracted_store_links" file that the last run left off on
#argv[2] being the actual link to that store
if __name__ == '__main__':
  if len(sys.argv) < 3:
      sys.exit()
  scrape(sys.argv[1])
  exception_loop(sys.argv[2])