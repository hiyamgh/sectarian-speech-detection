import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import itertools
import os
from selenium.webdriver.chrome.options import Options
import concurrent.futures as futures
import random
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import re
from openpyxl import load_workbook
import xlrd
from tqdm import tqdm
import re


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


def mkdir(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)


def login_tiktok():
    url = "https://www.tiktok.com/login/phone-or-email/email"
    driver.get(url)

    inputs = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'input')))
    print(inputs)
    print(len(inputs))

    if (len(inputs) == 2):
        username = inputs[0]
        username.send_keys("fatimamarsad2023")
        username.send_keys(Keys.ENTER)

        password = inputs[1]
        password.send_keys("fatimamarsad2023!")
        password.send_keys(Keys.ENTER)
    else:
        pass


def scrape_loaded_comments_tiktok(links_precomputed):
    all_data = {'Link': [], 'Day': [], 'Comments Volume': []}
    for link in links_precomputed:
        driver.get(link)
        time.sleep(random.randint(5, 10))

        num_comments = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'p.css-1xwyks2-PCommentTitle.e1a7v7ak1')))
        driver.execute_script("arguments[0].scrollIntoView();", num_comments)
        num_comments = num_comments.text
        print(f'Total number of comments: {num_comments}')

        print('Getting post time ....')
        try:
            info = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'span.css-5set0y-SpanOtherInfos.evv7pft3'))).text
            post_time = ''
            for t in info.split('.'):
                if '20' in t:
                    post_time = t
                    break
        except:
            post_time = ''
        print(f'\npost time {post_time}\n')

        try:
            all_data['Link'].append(link)
            all_data['Day'].append(post_time)
            all_data['Comments Volume'].append(num_comments)
        except:
            all_data['Link'].append('')
            all_data['Day'].append('')
            all_data['Comments Volume'].append('')

    return all_data


def apply_scraping_tiktok(links_precomputed):

    SCROLL_PAUSE_TIME = 2  # I'll use this variable for code sleeping time
    delay = 30  # delay time for WebDriver (in seconds)
    scrolling = True  # boolean value -> TRUE means that we're still scrolling, FALSE means we're not scrolling anymore
    last_height = driver.execute_script("return document.documentElement.scrollHeight")  # this is our last/current position on the page
    scrolling_attempt = 3  # we'll have 5 attempts before turning scrolling boolean to False

    all_data = {'Link': [], 'Day': [], 'Comments Volume': []}

    try:
        data = scrape_loaded_comments_tiktok(links_precomputed=links_precomputed)
        all_data['Link'].extend(data['Link'])
        all_data['Day'].extend(data['Day'])
        all_data['Comments Volume'].extend(data['Comments Volume'])
    except:
        pass

    df = pd.DataFrame(all_data)
    df = df.drop_duplicates()
    return df


def line_split(line):
    return re.findall(r'[^"\s]\S*|".+?"', line)


if __name__ == '__main__':

    category2english = {
        'فساد': 'corruption',
        'جندري': 'gender',
        'جنساني': 'sexuality',
        'ديني': 'religion',
        'سياسة وأمن': 'politics and security',
        'لجوء': 'refugee'
    }

    # category_en = input("Pick a category: ")
    months = input("Please enter the starting and ending month (inclusive) as MM-MM: ")
    months = months.strip().split("-")
    months_nb = []
    for m in months:
        if '0' in m and m[-1] != '0':
            months_nb.append(int(m[1]))
        else:
            months_nb.append(int(m))

    months_nb = list(range(months_nb[0], months_nb[1] + 1))

    driver = webdriver.Chrome('C:\Program Files\chromedriver-win32-119\chromedriver.exe')
    delay = 30

    login_tiktok()
    user_input = input('Please enter \'y\' when done logging in manually: ')

    for subdir, dirs, files in os.walk('Volume-TikTok/'):
        for file in files:
            if 'Accounts' not in file and 'Total-KD' in subdir and 'TikTok' in file and 'Comments' not in file:
                print(os.path.join(subdir, file))
                xls = xlrd.open_workbook(os.path.join(subdir, file), on_demand=True)
                sheets = xls.sheet_names()
                for sheet_name in tqdm(sheets):
                    if int(sheet_name[6:8]) in months_nb:
                        print('Processing sheet {} ====================================================='.format(sheet_name))
                        df = pd.read_excel(os.path.join(subdir, file), sheet_name)
                        print(os.path.join(subdir, file))
                        # category = subdir.split('\\')[0].split('/')[1]
                        category = subdir.split('\\')[0].split('/')[-1]

                        save_dir_volume = 'Volume-TikTok/{}/Total-KD/'.format(category)
                        comments_df = apply_scraping_tiktok(links_precomputed=list(set(df['link'])))
                        if not os.path.isfile(os.path.join(save_dir_volume, 'TikTok-Comments.xlsx')):
                            with pd.ExcelWriter(os.path.join(save_dir_volume, 'TikTok-Comments.xlsx')) as writer:
                                # df.to_excel(writer, sheet_name='E{}-{}'.format(str(time_after_dt)[:10], j), index=False)
                                comments_df.to_excel(writer, sheet_name=sheet_name, index=False)
                            writer.close()
                        else:
                            book = load_workbook(os.path.join(save_dir_volume, 'TikTok-Comments.xlsx'))
                            writer = pd.ExcelWriter(os.path.join(save_dir_volume, 'TikTok-Comments.xlsx'), engine='openpyxl')
                            writer.book = book

                            # df.to_excel(writer, sheet_name='E{}-{}'.format(str(time_after_dt)[:10], j), index=False)
                            comments_df.to_excel(writer, sheet_name=sheet_name, index=False)
                            writer.close()
