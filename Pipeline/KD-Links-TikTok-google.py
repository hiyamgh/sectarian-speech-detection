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
from tqdm import tqdm


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


def scrape_query_search_results():
    all_articles = []
    try:
        links = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.RzdJxc')))
        all_articles.extend(links)
    except:
        pass
    try:
        links = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.yuRUbf')))
        all_articles.extend(links)
    except:
        pass

    try:
        links = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.MjjYud')))
        all_articles.extend(links)
    except:
        pass

    try:
        links = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.V5XKdd')))
        all_articles.extend(links)
    except:
        pass

    print(len(all_articles))

    all_titles = []
    all_links = []
    for a in all_articles:
        try:
            link = a.find_element_by_css_selector('a').get_attribute('href')
            title = a.find_element_by_css_selector('a').text
        except:
            print('did not find link')
            continue

        if 'www.google.com' in link:
            continue

        else:
            print(link)
            print(title)

            all_links.append(link)
            all_titles.append(title)

    for i in itertools.zip_longest(all_titles, all_links):
        print(i)
        print('===================================')

    return all_titles, all_links


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

    driver = webdriver.Chrome('C:\Program Files\chromedriver-win32-119\chromedriver.exe')
    delay = 15
    events_file = input("Please enter the name of the events file: ")
    df = pd.read_excel(events_file.strip())
    months = input("Please enter the starting and ending month (inclusive) as MM-MM: ")
    months = months.strip().split("-")
    months_nb = []
    for m in months:
        if '0' in m and m[-1] != '0':
            months_nb.append(int(m[1]))
        else:
            months_nb.append(int(m))

    months_nb = list(range(months_nb[0], months_nb[1] + 1))

    for i, row in tqdm(df.iterrows(), total=len(df)):

        # if i < 46:
        #     continue

        if i < 25:
            continue

        time_after = row['التاريخ']

        if '2023' not in str(time_after):  # restricting the years 2023
            continue

        time_after_dt = datetime.strptime(str(time_after)[:10], '%Y-%m-%d')
        month_curr = time_after_dt.month

        if month_curr not in months_nb:
            continue

        category = str(row['النوع'])
        category_en = category2english[category]  # get the english equivalent of the category

        window = str(row['Window of Date'])

        if window.strip() in ['', 'nan']:
            continue

        if 'week' in window:
            num = window.split(' ')[0]
            # time_before_dt = relativedelta(weeks=int(num)) + time_after_dt
        else:
            num = window.split(' ')[0]
            # time_before_dt = relativedelta(months=int(num)) + time_after_dt

        time_before_dt = relativedelta(weeks=2) + time_after_dt

        keywords_text = str(row['كلمات مفتاحية']).strip()
        keywords_text_facebook = str(row['كلمات مفتاحية']).strip()

        if keywords_text in ["", "nan"]:
            continue

        print('Keywords: {}'.format(keywords_text))
        print('start date: {}'.format(str(time_after_dt)))
        print('end date: {}'.format(str(time_before_dt)))

        keywords_text_new = line_split(keywords_text)

        j = 0
        for kt in keywords_text_new:
            ktnew = []
            if kt == '':
                continue

            kt = kt.replace('\'', '')
            kt = kt.replace('\"', '')
            kt = kt.strip()

            queries_tiktok = []

            query_tiktok = 'site:{} '.format('https://www.tiktok.com/')
            query_tiktok += kt
            query_tiktok += ' after:{} '.format(str(time_after_dt)[:10])
            query_tiktok += ' before:{} '.format(str(time_before_dt)[:10])
            queries_tiktok.append(query_tiktok)

            for i, k in enumerate(kt.split(" ")):
                if i == 0:
                    if len(kt.split(" ")) > 1:
                        knew = "\"" + k + "\" AND"
                    else:
                        knew = "\"" + k + "\""
                elif i == len(kt.split(" ")) - 1:
                    knew = "\"" + k + "\""
                else:
                    knew = "\"" + k + "\" AND"

                ktnew.append(knew)

            kt = " ".join(ktnew)

            # Query over facebook videos
            query_tiktok = 'site:{} '.format('https://www.tiktok.com/')
            query_tiktok += kt
            query_tiktok += ' after:{} '.format(str(time_after_dt)[:10])
            query_tiktok += ' before:{} '.format(str(time_before_dt)[:10])
            queries_tiktok.append(query_tiktok)

            save_dir_volume = 'Volume-TikTok/{}/Total-KD/'.format(category_en)
            save_dir_links = 'Events-TikTok/E{}-KD/'.format(str(time_after_dt)[:10])

            for qf in queries_tiktok:
                mkdir(save_dir_volume)
                mkdir(save_dir_links)

                articles = {'title': [], 'link': []}

                driver.get('http://www.google.com')
                search = driver.find_element_by_name('q')
                # search.send_keys(query_facebook)
                search.send_keys(qf)
                search.send_keys(Keys.RETURN)

                SCROLL_PAUSE_TIME = 2  # I'll use this variable for code sleeping time
                delay = 30  # delay time for WebDriver (in seconds)
                scrolling = True  # boolean value -> TRUE means that we're still scrolling, FALSE means we're not scrolling anymore
                last_height = driver.execute_script("return document.documentElement.scrollHeight")  # this is our last/current position on the page
                scrolling_attempt = 1  # we'll have 5 attempts before turning scrolling boolean to False

                # video_links, comments_video, posts_links, comments_posts = [], [], [], []
                articles_len = 0

                while scrolling == True:
                    htmlelement = driver.find_element_by_tag_name("body")  # locate html tag
                    htmlelement.send_keys(Keys.END)

                    new_height = driver.execute_script("return document.documentElement.scrollHeight")  # calculate current position
                    time.sleep(SCROLL_PAUSE_TIME)  # make pause because scrolling will take 0.5/1 seconds
                    driver.implicitly_wait(15)  # make longer pause if loading new comments takes longer

                    try:
                        article_titles, article_links = scrape_query_search_results()
                        articles['title'].extend(article_titles)
                        articles['link'].extend(article_links)
                        articles_len = len(articles)
                    except:
                        pass

                    try:
                        all_spans = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'span')))
                        for span in all_spans:
                            if span.text == 'More results':
                                driver.execute_script("arguments[0].scrollIntoView();", span)
                                driver.execute_script("arguments[0].click();", span)
                                time.sleep(3)
                                break
                    except:
                        pass

                    try:
                        atagrepeated = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.card-section a')))[0]
                        driver.execute_script("arguments[0].scrollIntoView();", atagrepeated)
                        driver.execute_script("arguments[0].click();", atagrepeated)
                        driver.get(atagrepeated)
                        time.sleep(random.randint(50, 10))
                        break
                    except:
                        pass

                    if len(articles) == articles_len:
                        print('scrolling attempt: {}'.format(scrolling_attempt))
                        scrolling_attempt -= 1

                    if (scrolling_attempt <= 0):
                        scrolling = False

                    if new_height == last_height:  # if current position  is the same as last position, it means we've reached bottom of the page, so we'll break the loop
                        scrolling_attempt -= 1
                        print(f"scrolling attempt {scrolling_attempt}")
                        if (scrolling_attempt <= 0):
                            scrolling = False  # this will break while loop
                    last_height = new_height  # if current position is not the same as last one, we'll set last position as new height


                print('Done collecting TikTok links ....')
                print('got in total {} unique links'.format(list(set(articles['link']))))


                tiktok_df = pd.DataFrame(articles)
                tiktok_df = tiktok_df.drop_duplicates()

                try:
                    t1 = time.time()
                    # df = apply_scraping_facebook(search_query=query_facebook, links_precomputed=list(set(articles['link'])))
                    if not os.path.isfile(os.path.join(save_dir_volume, 'TikTok.xlsx')):
                        with pd.ExcelWriter(os.path.join(save_dir_volume, 'TikTok.xlsx')) as writer:
                            # df.to_excel(writer, sheet_name='E{}-{}'.format(str(time_after_dt)[:10], j), index=False)
                            tiktok_df.to_excel(writer, sheet_name='E{}-{}'.format(str(time_after_dt)[:10], j), index=False)
                        writer.close()
                    else:
                        book = load_workbook(os.path.join(save_dir_volume, 'TikTok.xlsx'))
                        writer = pd.ExcelWriter(os.path.join(save_dir_volume, 'TikTok.xlsx'), engine='openpyxl')
                        writer.book = book

                        # df.to_excel(writer, sheet_name='E{}-{}'.format(str(time_after_dt)[:10], j), index=False)
                        tiktok_df.to_excel(writer, sheet_name='E{}-{}'.format(str(time_after_dt)[:10], j), index=False)
                        writer.close()

                    t2 = time.time()
                    print('This process took {} mins'.format((t2 - t1) / 60))

                    file_name = 'E{}-DB.txt'.format(str(time_after_dt)[:10])

                    if not os.path.isfile(os.path.join(save_dir_links, file_name)):
                        # db_links = list(df['Link'])
                        db_links = list(tiktok_df['Link'])
                        with open(os.path.join(save_dir_links, file_name), 'w') as f:
                            for link in db_links:
                                f.write(link + '\n')
                        f.close()
                    else:
                        # db_links = list(df['Link'])
                        db_links = list(tiktok_df['Link'])
                        with open(os.path.join(save_dir_links, file_name), 'a') as f:
                            for link in db_links:
                                f.write(link + '\n')
                        f.close()

                except:
                    print('Did not find results for query {}'.format(keywords_text))

                j += 1