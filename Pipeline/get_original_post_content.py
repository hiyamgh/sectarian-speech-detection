from sys import platform

import pandas as pd
import time
import pandas as pd
from humanfriendly.testing import retry
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import itertools
import os
import re
from selenium.webdriver.chrome.options import Options
import concurrent.futures as futures
import random
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from openpyxl import load_workbook
from tqdm import tqdm
import shlex
import pickle
from accounts2credentials import acc2cred
from selenium.webdriver.chrome.service import Service
import argparse
import requests

def timeout(timelimit):
    def decorator(func):
        def decorated(*args, **kwargs):
            with futures.ThreadPoolExecutor(max_workers=1) as executor:
                future = executor.submit(func, *args, **kwargs)
                try:
                    result = future.result(timelimit)
                except futures.TimeoutError:
                    print('Timedout!')
                    raise TimeoutError from None
                else:
                    print(result)
                executor._threads.clear()
                futures.thread._threads_queues.clear()
                return result
        return decorated
    return decorator


def twitter_signin(driverG=None):
    if driverG is not None:
        driver = driverG

    delay=20
    url = "https://twitter.com/i/flow/login"
    driver.get(url)
    username = WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[autocomplete="username"]')))
    username.send_keys(acc2cred["Twitter"]["username"])
    username.send_keys(Keys.ENTER)

    done_selecting = input("When done selecting the images (CAPTCHA) please press any character and hit ENTER: ")
    return
    password = WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[name="password"]')))
    password.send_keys(acc2cred["Twitter"]["password"])
    password.send_keys(Keys.ENTER)
    # time.sleep(30)
    time.sleep(5)



def get_tweet_original_post(tweet_url):
    delay = 15
    driver.get(tweet_url.replace("\n", ""))
    time.sleep(5)
    try:
        post_content = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.css-175oi2r.r-eqz5dr.r-16y2uox.r-1wbh5a2')))
        print(post_content[0].text)
    except:
        return ""
    return post_content[0].text


def login_facebook():
    url = 'https://www.facebook.com/login/'
    driver.get(url)

    done = input("When you are done logging in MANUALLY, please press ENTER")
    return

def get_facebook_original_post(facebook_link):
    delay = 15
    driver.get(facebook_link.replace("\n", ""))
    time.sleep(5)
    if "story_fbid" in facebook_link or "pfbid" in facebook_link:
        try:
            post_content = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.html-div.xdj266r.x14z9mp.xat24cr.x1lziwak.xexx8yu.xyri2b.x18d9i69.x1c1uobl')))
            try:
                print(post_content[0].text)
            except:
                return ""
        except:
            return ""
    else:
        try:
            post_content = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.xf7dkkf.xv54qhq.xyamay9')))
            print(post_content[0].text)
        except:
            return ""
    return post_content[0].text


def extract_video_id(url):
    # Match standard and shortened YouTube URLs
    patterns = [
        r"v=([a-zA-Z0-9_-]{11})",  # youtube.com/watch?v=...
        r"youtu\.be/([a-zA-Z0-9_-]{11})"  # youtu.be/...
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None


def get_video_titles(video_ids):
    params = {
        "part": "snippet",
        "id": ",".join(video_ids),
        "key": API_KEY
    }
    response = requests.get(YOUTUBE_API_URL, params=params)
    data = response.json()

    titles = {}
    for item in data.get("items", []):
        vid = item["id"]
        title = item["snippet"]["title"]
        titles[vid] = title
    return titles



if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('--platform', type=str, default='YouTube', help='The platform to scrape for')
    args = argparser.parse_args()

    API_KEY = 'AIzaSyBmGp7Pc8MpPcwMavdqWBh0YPKxqYz1xOk'

    # urls = [
    #     "https://x.com/i/web/status/1713542383311192135",
    #     "https://x.com/i/web/status/1713479844414074998"
    # ]
    df = pd.read_excel("Dataset_updated.xlsx")
    urls = list(set(df["Link"]))

    chrome_driver_path = r"C:/Program Files/chromedriver-win64-138/chromedriver.exe"
    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service)

    links2content = {}
    if args.platform == "Facebook":
        login_facebook()
        urls_fb = [link for link in urls if "facebook" in link]
        for url in tqdm(urls_fb):
            fb_content = get_facebook_original_post(facebook_link=url)
            links2content[url] = fb_content
            print()
            with open(os.path.join(f'{args.platform}_links2content_.pickle'), 'wb') as handle:
                pickle.dump(links2content, handle, protocol=pickle.HIGHEST_PROTOCOL)
            print("=======================================")

    elif args.platform == "Twitter":
        twitter_signin(driverG=driver)
        urls_twitter = [link for link in urls if "twitter" in link or "x.com" in link]
        for url in tqdm(urls_twitter):
            twitter_content = get_tweet_original_post(tweet_url=url)
            links2content[url] = twitter_content
            with open(os.path.join(f'{args.platform}_links2content_.pickle'), 'wb') as handle:
                pickle.dump(links2content, handle, protocol=pickle.HIGHEST_PROTOCOL)
            print("=======================================")

    elif args.platform == "YouTube":
        YOUTUBE_API_URL = "https://www.googleapis.com/youtube/v3/videos"

        urls_youtube = [link.replace("\n", "") for link in urls if "youtube" in link]
        # Extract video IDs
        video_ids = list(filter(None, [extract_video_id(url) for url in urls_youtube]))
        titles = get_video_titles(video_ids)
        for url in urls_youtube:
            vid = extract_video_id(url)
            print(f"{url} → {titles.get(vid, 'Title not found')}")
            links2content[url] = titles.get(vid, 'Title not found')
            with open(os.path.join(f'{args.platform}_links2content_.pickle'), 'wb') as handle:
                pickle.dump(links2content, handle, protocol=pickle.HIGHEST_PROTOCOL)
            print("=======================================")
