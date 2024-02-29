import time
from time import sleep
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import itertools
import os
from selenium.webdriver.chrome.options import Options
import random
from selenium.common.exceptions import NoSuchElementException


def mkdir(folder_name):
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)


def login_facebook():
    url = 'https://www.facebook.com/login/'
    driver.get(url)

    # [(i, e) for i,e in enumerate(inputs) if e.get_attribute('name') == 'pass']

    inputs = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'input')))
    username = inputs[13]
    username.send_keys("fatimamarsad@gmail.com")
    # username.send_keys(Keys.ENTER)

    password = inputs[14]
    password.send_keys("fatimamarsad2023")
    password.send_keys(Keys.ENTER)


def scrape_search_bar_posts(link):
    all_links = []
    all_posts = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,
                                                                                        'span.x4k7w5x.x1h91t0o.x1h9r5lt.x1jfb8zj.xv2umb2.x1beo9mf.xaigb6o.x12ejxvf.x3igimt.xarpa2k.xedcshv.x1lytzrv.x1t2pt76.x7ja8zs.x1qrby5j a.x1i10hfl.xjbqb8w.x6umtig.x1b1mbwd.xaqea5y.xav7gou.x9f619.x1ypdohk.xt0psk2.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x16tdsg8.x1hl2dhg.xggy1nq.x1a2a7pz.x1heor9g.xt0b8zv.xo1l8bm')))

    for p in all_posts:
        try:
            all_links.append(p.get_attribute('href'))
        except:
            continue

    return all_links


def apply_scraping_feed_searchbar(link, max_count):
    ''' function that scrolls over and extracts all comments for a certain youtube video and returns dataframe of comments '''

    SCROLL_PAUSE_TIME = 2  # I'll use this variable for code sleeping time
    delay = 30  # delay time for WebDriver (in seconds)
    scrolling = True  # boolean value -> TRUE means that we're still scrolling, FALSE means we're not scrolling anymore
    last_height = driver.execute_script("return document.documentElement.scrollHeight")  # this is our last/current position on the page
    scrolling_attempt = 5  # we'll have 5 attempts before turning scrolling boolean to False

    driver.get(link)

    all_links = []
    while scrolling == True:
        htmlelement = driver.find_element_by_tag_name("body")  # locate html tag
        htmlelement.send_keys(Keys.END)

        try:
            last_20_links = scrape_search_bar_posts(link)  # calling function to scrape last 20 comments
            all_links.extend(last_20_links)
            print(len(set(all_links)))
        except:
            print("error while trying to load comments")

        if len(set(all_links)) >= max_count:
            return all_links

        new_height = driver.execute_script("return document.documentElement.scrollHeight")  # calculate current position
        time.sleep(SCROLL_PAUSE_TIME)  # make pause because scrolling will take 0.5/1 seconds
        driver.implicitly_wait(30)  # make longer pause if loading new comments takes longer

        if new_height == last_height:  # if current position  is the same as last position, it means we've reached bottom of the page, so we'll break the loop
            scrolling_attempt -= 1
            print(f"scrolling attempt {scrolling_attempt}")
            if (scrolling_attempt == 0):
                scrolling = False  # this will break while loop
        last_height = new_height  # if current position is not the same as last one, we'll set last position as new height

    return all_links


if __name__ == '__main__':
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome('C:\Program Files\chromedriver-win32-119\chromedriver.exe')
    delay = 10

    search_query = input('Please enter your search query of interest: ')
    search_query_mod = '%20'.join(search_query.split(' '))
    max_count = int(input('In case there are many posts, what is the maximum count of posts you are considering to scrape: '))
    login_facebook()
    time.sleep(3)
    all_links = apply_scraping_feed_searchbar(link='https://www.facebook.com/search/top?q={}'.format(search_query_mod),
                                              max_count=max_count)

    all_links = list(set(all_links))

    with open('facebook_search_bar.txt', 'w') as f:
        for link in all_links:
            f.write(link + '\n')
    f.close()

