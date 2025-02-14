from selenium.webdriver.common.by import By
from os import environ
from selenium.webdriver import Remote, ChromeOptions as Options
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection as Connection
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import re
import csv
# this file abstracts all links to starbucks stores in every state capital across the U.S.
capitals_list = []
AUTH = environ.get('AUTH', default='API_key')
with open('./state_and_capitals.txt', 'r') as file:
        for line in file:
            capitals_list.append(line)
# main scraper function for starbucks storelinks
def scrape(url):
    # initiate connection with bright data proxy server
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
        print(f'Connected! Navigating to {url}...')
        status = 'solve_failed'
        while status == 'solve_failed':
            print(f'Connected! Navigating to {url}...')
            driver.get(url)
            print('Navigated! Waiting captcha to detect and solve...')
            result = driver.execute('executeCdpCommand', {
                'cmd': 'Captcha.waitForSolve',
                'params': {'detectTimeout': 10 * 1000},
            })
            status = result['value']['status']
            print(f'Captcha status: {status}')
        # end captcha solving loop
        # begin loop until next page button is not found
        while True:
            print('finding link elements')
            links = driver.find_elements(By.NAME, 'Starbucks')
            # saving abstracted store links from page to file
            with open('links.txt', 'a') as file:
                for link in links:
                    file.write("%s\n" % link.get_attribute("outerHTML"))
            print('link elements written to file')
            try:
                # attempt to find next page element and direct to next page for more links
                # otherwise break loop and exit function
                print('searching for "next" page')
                next_button = driver.find_element(By.CLASS_NAME, 'next-link')
                next_button = next_button.get_attribute("href")
                # captcha solving loop
                status = 'solve_failed'
                while status == 'solve_failed':
                    print(f'Connected! Navigating to {next_button}...')
                    driver.get(next_button)
                    print('Navigated! Waiting captcha to detect and solve...')
                    result = driver.execute('executeCdpCommand', {
                        'cmd': 'Captcha.waitForSolve',
                        'params': {'detectTimeout': 10 * 1000},
                    })
                    status = result['value']['status']
                    print(f'Captcha status: {status}')
                # end captcha solving loop
            except NoSuchElementException:
                print("No Such Element")
                break
    finally:
        driver.quit()

# scraper function is set to loop through all state capitals to abstract links for stores in all capitals
if __name__ == '__main__':
    for line in capitals_list:
        state, city = line.split(',')
        city = city.replace(' ', '+')
        city = city.replace('\n', '')
        TARGET_URL = environ.get('TARGET_URL', default=f'https://www.yelp.com/search?choq=1&find_desc=starbucks&find_loc={city}%2C+{state}%2C+United+States')
        print(f'scraping {TARGET_URL}')
        scrape(TARGET_URL)
