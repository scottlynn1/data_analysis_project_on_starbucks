from selenium.webdriver.common.by import By
from os import environ
from selenium.webdriver import Remote, ChromeOptions as Options
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection as Connection
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup


AUTH = environ.get('AUTH', default='USER:PASS')
#initialize and fill list of capitals and states of U.S.
capitals_list = []
with open('./state_and_capitals.txt', 'r') as file:
  for line in file:
    capitals_list.append(line)
#define main scraper function
def scrape(url):
  #uses bright data credentials to initiate proxy server connection
  if AUTH == 'USER:PASS':
    raise Exception('Provide Scraping Browsers credentials in AUTH ' +
                    'environment variable or update the script.')
  print('Connecting to Browser...')
  server_addr = f'https://{AUTH}@brd.superproxy.io:9515'
  connection = Connection(server_addr, 'goog', 'chrome')
  driver = Remote(connection, options=Options())
  #connection established
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
    # while loop until next page link is not found
    while True:
      print('finding link elements')
      #wait for page load
      driver.implicitly_wait(10)
      content = driver.find_element(By.ID, 'main-content').get_attribute('innerHTML')
      soup = BeautifulSoup(content, 'html.parser')
      ulitem = soup.find_all('ul')[0]
      listitems = ulitem.find_all('li', recursive=False)
      listitems = listitems[12:17]
      # storing store links into file
      with open('related_store_links.txt', 'a') as file:
        for item in listitems:
          link = item.find('a')
          file.write("%s\n" % link)
      print('link elements written to file')
      # this section grabs next next page element and directs to next page 
      # otherwise breaks loop if no next page is found
      try:
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
        # end captha solving loop
      except NoSuchElementException:
        print("No Such Element")
        break
      
  finally:
    driver.quit()

# scraper function is executed and loops through entire of state capitals
if __name__ == '__main__':
    for line in capitals_list:
        state, city = line.split(',')
        city = city.replace(' ', '+')
        city = city.replace('\n', '')
        TARGET_URL = environ.get('TARGET_URL', default=f'https://www.yelp.com/search?find_desc=starbucks&find_loc={city}%2C+{state}%2C+United+States')
        print(f'scraping {TARGET_URL}')
        scrape(TARGET_URL)
