from selenium.webdriver.common.by import By
from os import environ
from selenium.webdriver import Remote, ChromeOptions as Options
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection as Connection
from selenium.common.exceptions import NoSuchElementException, WebDriverException

from bs4 import BeautifulSoup
import re
import csv
import sys

AUTH = environ.get('AUTH', default='brd-customer-hl_3e287db4-zone-scraping_browser2:oe7yaonn04qa')
stores = []
with open('./abstracted_links.txt', 'r') as file:
    for store in file:
        store = store.rstrip('\n')
        stores.append(f'https://www.yelp.com{store}')


def scrape(store):
    if AUTH == 'USER:PASS':
        raise Exception('Provide Scraping Browsers credentials in AUTH ' +
                        'environment variable or update the script.')
    print('Connecting to Browser...')
    server_addr = f'https://{AUTH}@brd.superproxy.io:9515'
    connection = Connection(server_addr, 'goog', 'chrome')
    driver = Remote(connection, options=Options())
    try:
        print(f'Connected! Navigating to {store}...')
        status = 'solve_failed'
        while status == 'solve_failed':
            try:
                print(f'Connected! Navigating to {store}...')
                driver.get(store)
                print('Navigated! Waiting captcha to detect and solve...')
                result = driver.execute('executeCdpCommand', {
                    'cmd': 'Captcha.waitForSolve',
                    'params': {'detectTimeout': 10 * 1000},
                })
                status = result['value']['status']
                print(f'Captcha status: {status}')
            except WebDriverException:
                print("server error, trying again")
                driver.implicitly_wait(10)
                driver.get(store)
                print('Navigated! Waiting captcha to detect and solve...')
                result = driver.execute('executeCdpCommand', {
                    'cmd': 'Captcha.waitForSolve',
                    'params': {'detectTimeout': 10 * 1000},
                })
                status = result['value']['status']
                print(f'Captcha status: {status}')
        while True:
            print('pulling review information')
            driver.implicitly_wait(3)
            content = driver.find_element(By.ID, 'main-content').get_attribute('innerHTML')
            soup = BeautifulSoup(content, 'html.parser')
            address = soup.find('address').find_all('span')[-1:]
            address = address[0].string
            review_ratings = soup.find_all('div', class_='y-css-dnttlc')
            review_dates = soup.find_all('span', class_="y-css-1d8mpv1")
            reviews = soup.find_all('p', class_=re.compile('comment__'))
            with open('review_info.csv', mode='a') as csv_file:
                csv_writer = csv.writer(csv_file, delimiter='~', quoting=csv.QUOTE_NONE, escapechar='`')
                for rating, date, review in zip(review_ratings, review_dates, reviews):
                    string = str(review.span).replace('<br/><br/>', '')
                    rating = rating['aria-label'].rstrip(' star rating')
                    date = date.string
                    review = re.sub('\<.*?\>', '', string)
                    csv_writer.writerow([address, rating, date, review])
            print('review infromation written to file')
            try:
                print('searching for "next" page')
                next_button = driver.find_element(By.CLASS_NAME, 'next-link')
            except NoSuchElementException:
                print("No Such Element or End of Review list")
                break

            next_button = next_button.get_attribute("href")
            print(f'Navigating to {next_button}...')
            try:
                status = 'solve_failed'
                while status == 'solve_failed':
                    driver.get(next_button)
                    print('Navigated! Waiting captcha to detect and solve...')
                    result = driver.execute('executeCdpCommand', {
                        'cmd': 'Captcha.waitForSolve',
                        'params': {'detectTimeout': 10 * 1000},
                    })
                    status = result['value']['status']
                    print(f'Captcha status: {status}')
            except WebDriverException:
                print("server error, trying again")
                driver.implicitly_wait(10)
                status = 'solve_failed'
                while status == 'solve_failed':
                    driver.get(next_button)
                    print('Navigated! Waiting captcha to detect and solve...')
                    result = driver.execute('executeCdpCommand', {
                        'cmd': 'Captcha.waitForSolve',
                        'params': {'detectTimeout': 10 * 1000},
                    })
                    status = result['value']['status']
                    print(f'Captcha status: {status}')
    finally:
        driver.quit()


if __name__ == '__main__':
    if len(sys.argv) < 3:
        sys.exit()
    scrape(sys.argv[1])
    for store in stores[int(sys.argv[2]):]:
        scrape(store)