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
    # for a in all_articles:
    #     # try:
    #     #     title = a.find_element_by_css_selector('div.yuRUbf a h3').text
    #     #     print(title)
    #     # except:
    #     #     title = ''
    #     #     print('did not find title')
    #     all_titles.append('')

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


def login_facebook():
    url = 'https://www.facebook.com/login/'
    driver.get(url)

    # [(i, e) for i,e in enumerate(inputs) if e.get_attribute('name') == 'pass']

    inputs = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'input')))
    username = inputs[13]
    # username.send_keys("loulou1997.g@hotmail.com")
    # username.send_keys("fatimamarsad@gmail.com")
    username.send_keys("hiyamghannam97@gmail.com")
    # username.send_keys(Keys.ENTER)

    password = inputs[14]
    # password.send_keys("Hiyam1997")
    # password.send_keys("fatimamarsad2023")
    password.send_keys("Perl1997AUB")
    password.send_keys(Keys.ENTER)


def get_facebook_volumes_posts(driver, links_precomputed=None):
    if links_precomputed is None:
        all_data = {'Link': [], 'Day': [], 'scraping_time': [], 'Comments Volume': []}
        all_links_posts = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a.x1i10hfl.xjbqb8w.x6umtig.x1b1mbwd.xaqea5y.xav7gou.x9f619.x1ypdohk.xt0psk2.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x16tdsg8.x1hl2dhg.xggy1nq.x1a2a7pz.x1heor9g.xt0b8zv.xo1l8bm')))
        all_dates = [a.text for a in all_links_posts]
        for i, post in enumerate(all_links_posts):
            if 'pfbid' in post:
                driver.get(post)
                time.sleep(random.randint(3, 5))
                try:
                    comment_nb = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'span.x193iq5w.xeuugli.x13faqbe.x1vvkbs.x1xmvt09.x1lliihq.x1s928wv.xhkezso.x1gmr53x.x1cpjm7i.x1fgarty.x1943h6x.xudqn12.x3x7a5m.x6prxxf.xvq8zen.xo1l8bm.xi81zsa')))[1].text
                except:
                    comment_nb = 0
                print('{} - {} comments on the post: {}'.format(all_dates[i], comment_nb, post))

                all_data['Link'].append(post)
                all_data['Day'].append(all_dates[i])
                all_data['scraping_time'].append(str(time.time()))
                all_data['Comments Volume'].append(comment_nb)
    else:
        all_data = {'Link': [], 'Day': [], 'scraping_time': [], 'Comments Volume': []}
        # all_links_posts = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a.x1i10hfl.xjbqb8w.x6umtig.x1b1mbwd.xaqea5y.xav7gou.x9f619.x1ypdohk.xt0psk2.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x16tdsg8.x1hl2dhg.xggy1nq.x1a2a7pz.x1heor9g.xt0b8zv.xo1l8bm')))
        # all_dates = [a.text for a in all_links_posts]
        all_links_posts = links_precomputed
        for i, post in enumerate(all_links_posts):
            if 'pfbid' in post or 'photo' in post or 'post' in post:
                driver.get(post)
                time.sleep(random.randint(3, 5))
                comment_numbers = []

                try:
                    comment_nb = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'span.x193iq5w.xeuugli.x13faqbe.x1vvkbs.x1xmvt09.x1lliihq.x1s928wv.xhkezso.x1gmr53x.x1cpjm7i.x1fgarty.x1943h6x.xudqn12.x3x7a5m.x6prxxf.xvq8zen.xo1l8bm.xi81zsa')))
                    comment_numbers.append(';'.join([cn.text for cn in comment_nb]))
                    print(comment_nb)
                except:

                    try:
                        all_spans = [s.text for s in WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'span.x193iq5w.xeuugli.x13faqbe.x1vvkbs.x1xmvt09.x1lliihq.x1s928wv.xhkezso.x1gmr53x.x1cpjm7i.x1fgarty.x1943h6x.xudqn12.x3x7a5m.x6prxxf.xvq8zen.xo1l8bm.xi81zsa')))]
                        comment_numbers.extend(all_spans)
                        print(all_spans)
                    except:
                        comment_nb = 0
                        comment_numbers.append(comment_nb)
                        print(comment_nb)

                try:
                    date_watch = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,'a.x1i10hfl.xjbqb8w.x6umtig.x1b1mbwd.xaqea5y.xav7gou.x9f619.x1ypdohk.xt0psk2.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x16tdsg8.x1hl2dhg.xggy1nq.x1a2a7pz.x1heor9g.xt0b8zv.xo1l8bm')))[0].text
                except:
                    date_watch = ''
                # print('{} - {} comments on the post: {}'.format(all_dates[i], comment_nb, post))
                print('{} - {} comments on the post: {}'.format('', ','.join(comment_numbers), post))

                all_data['Link'].append(post)
                # all_data['Day'].append(all_dates[i])
                all_data['Day'].append(date_watch)
                all_data['scraping_time'].append(str(time.time()))
                all_data['Comments Volume'].append(';'.join(comment_numbers))
                print('The list that we will be joining: {}'.format(';'.join(comment_numbers)))

    return all_data


def get_facebook_volumes_videos(driver, links_precomputed=None):
    if links_precomputed is None:
        all_data = {'Link': [], 'Day': [], 'scraping_time': [], 'Comments Volume': []}
        all_links_videos = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,  'a.x1i10hfl.xjbqb8w.x6umtig.x1b1mbwd.xaqea5y.xav7gou.x9f619.x1ypdohk.xt0psk2.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x16tdsg8.x1hl2dhg.xggy1nq.x1a2a7pz.x1heor9g.xt0b8zv.x1s688f')))
        all_links_videos = [a.get_attribute('href') for a in all_links_videos]

        for watch in all_links_videos:
            # if 'watch' in all_links_videos:
            driver.get(watch)
            time.sleep(random.randint(3, 5))
            comments_watch = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'span.x193iq5w.xeuugli.x13faqbe.x1vvkbs.x1xmvt09.x1lliihq.x1s928wv.xhkezso.x1gmr53x.x1cpjm7i.x1fgarty.x1943h6x.x4zkp8e.x676frb.x1nxh6w3.x1sibtaa.xo1l8bm.xi81zsa')))[
                0].text
            date_watch = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a.x1i10hfl.xjbqb8w.x6umtig.x1b1mbwd.xaqea5y.xav7gou.x9f619.x1ypdohk.xt0psk2.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x16tdsg8.x1hl2dhg.xggy1nq.x1a2a7pz.x1heor9g.xt0b8zv.xo1l8bm')))[
                0].text
            print('{} - {} comments on the post: {}'.format(date_watch, comments_watch, watch))

            all_data['Link'].append(watch)
            all_data['Day'].append(date_watch)
            all_data['scraping_time'].append(str(time.time()))
            all_data['Comments Volume'].append(comments_watch)

        return all_data
    else:
        all_data = {'Link': [], 'Day': [], 'scraping_time': [], 'Comments Volume': []}
        # all_links_videos = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a.x1i10hfl.xjbqb8w.x6umtig.x1b1mbwd.xaqea5y.xav7gou.x9f619.x1ypdohk.xt0psk2.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x16tdsg8.x1hl2dhg.xggy1nq.x1a2a7pz.x1heor9g.xt0b8zv.x1s688f')))
        # all_links_videos = [a.get_attribute('href') for a in all_links_videos]
        all_links_videos = links_precomputed
        for watch in all_links_videos:
            if 'watch' in watch or 'videos' in watch:
                driver.get(watch)
                time.sleep(random.randint(3, 5))
                comments_watch = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'span.x193iq5w.xeuugli.x13faqbe.x1vvkbs.x1xmvt09.x1lliihq.x1s928wv.xhkezso.x1gmr53x.x1cpjm7i.x1fgarty.x1943h6x.x4zkp8e.x676frb.x1nxh6w3.x1sibtaa.xo1l8bm.xi81zsa')))[0].text
                date_watch = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a.x1i10hfl.xjbqb8w.x6umtig.x1b1mbwd.xaqea5y.xav7gou.x9f619.x1ypdohk.xt0psk2.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x16tdsg8.x1hl2dhg.xggy1nq.x1a2a7pz.x1heor9g.xt0b8zv.xo1l8bm')))[0].text
                print('{} - {} comments on the post: {}'.format(date_watch, comments_watch, watch))

                all_data['Link'].append(watch)
                all_data['Day'].append(date_watch)
                all_data['scraping_time'].append(str(time.time()))
                all_data['Comments Volume'].append(comments_watch)

        return all_data


def apply_scraping_facebook(search_query, links_precomputed=None):
    login_facebook()
    time.sleep(10)

    SCROLL_PAUSE_TIME = 2  # I'll use this variable for code sleeping time
    delay = 30  # delay time for WebDriver (in seconds)
    scrolling = True  # boolean value -> TRUE means that we're still scrolling, FALSE means we're not scrolling anymore
    last_height = driver.execute_script("return document.documentElement.scrollHeight")  # this is our last/current position on the page
    scrolling_attempt = 3  # we'll have 5 attempts before turning scrolling boolean to False

    if links_precomputed is None:
        all_data = {
            'Link': [],
            'Day': [],
            'scraping_time': [],
            'Comments Volume': []
        }

        # video_description = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div#description-inner')))
        while scrolling == True:
            htmlelement = driver.find_element_by_tag_name("body")  # locate html tag
            htmlelement.send_keys(Keys.END)

            new_height = driver.execute_script("return document.documentElement.scrollHeight")  # calculate current position
            time.sleep(SCROLL_PAUSE_TIME)  # make pause because scrolling will take 0.5/1 seconds
            driver.implicitly_wait(30)  # make longer pause if loading new comments takes longer

            try:
                data = get_facebook_volumes_posts(driver=driver)
                all_data['Link'].extend(data['Link'])
                all_data['Day'].extend(data['Day'])
                all_data['scraping_time'].extend(data['scraping_time'])
                all_data['Comments Volume'].extend(data['Comments Volume'])

            except:
                pass

            if new_height == last_height:  # if current position  is the same as last position, it means we've reached bottom of the page, so we'll break the loop
                scrolling_attempt -= 1
                print(f"scrolling attempt {scrolling_attempt}")
                if (scrolling_attempt == 0):
                    scrolling = False  # this will break while loop
            last_height = new_height  # if current position is not the same as last one, we'll set last position as new height

        # Get Facebook Videos/Watch
        driver.get('https://www.facebook.com/search/videos?q={}'.format(search_query))
        time.sleep(random.randint(5, 10))
        scrolling = True
        while scrolling == True:
            htmlelement = driver.find_element_by_tag_name("body")  # locate html tag
            htmlelement.send_keys(Keys.END)

            new_height = driver.execute_script("return document.documentElement.scrollHeight")  # calculate current position
            time.sleep(SCROLL_PAUSE_TIME)  # make pause because scrolling will take 0.5/1 seconds
            driver.implicitly_wait(30)  # make longer pause if loading new comments takes longer

            if new_height == last_height:  # if current position  is the same as last position, it means we've reached bottom of the page, so we'll break the loop
                scrolling_attempt -= 1
                print(f"scrolling attempt {scrolling_attempt}")
                if (scrolling_attempt <= 0):
                    scrolling = False  # this will break while loop
            last_height = new_height  # if current position is not the same as last one, we'll set last position as new height

        try:
            data = get_facebook_volumes_videos(driver=driver)
            all_data['Link'].extend(data['Link'])
            all_data['Day'].extend(data['Day'])
            all_data['scraping_time'].extend(data['scraping_time'])
            all_data['Comments Volume'].extend(data['Comments Volume'])

        except:
            pass

        df = pd.DataFrame(all_data)
        df = df.drop_duplicates()
        return df

    else:
        all_data = {
            'Link': [],
            'Day': [],
            'scraping_time': [],
            'Comments Volume': []
        }

        try:
            data = get_facebook_volumes_posts(driver=driver, links_precomputed=links_precomputed)
            all_data['Link'].extend(data['Link'])
            all_data['Day'].extend(data['Day'])
            all_data['scraping_time'].extend(data['scraping_time'])
            all_data['Comments Volume'].extend(data['Comments Volume'])
        except:
            pass

        try:
            data = get_facebook_volumes_videos(driver=driver, links_precomputed=links_precomputed)
            all_data['Link'].extend(data['Link'])
            all_data['Day'].extend(data['Day'])
            all_data['scraping_time'].extend(data['scraping_time'])
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

    driver = webdriver.Chrome('C:\Program Files\chromedriver-win32-119\chromedriver.exe')
    delay = 30
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

        # if i < 14:
        #     continue

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

            # for i, k in enumerate(kt.split(" ")):
            #     if i == 0:
            #         if len(kt.split(" ")) > 1:
            #             knew = "\"" + k + "\" AND"
            #         else:
            #             knew = "\"" + k + "\""
            #     elif i == len(kt.split(" ")) - 1:
            #         knew = "\"" + k + "\""
            #     else:
            #         knew = "\"" + k + "\" AND"
            #
            #     ktnew.append(knew)
            #
            # kt = " ".join(ktnew)

            # ktyoutube = "intitle:{}".format(kt)
            # kt = ' AND '.join(kt.split(' '))

            queries_facebook = []

            # query_facebook = 'site:{} '.format('https://www.facebook.com/')

            # Query over facebook videos
            query_facebook = 'site:{} '.format('https://www.facebook.com/*videos/')
            query_facebook += kt
            query_facebook += ' after:{} '.format(str(time_after_dt)[:10])
            query_facebook += ' before:{} '.format(str(time_before_dt)[:10])
            queries_facebook.append(query_facebook)

            # Query over facebook posts
            query_facebook = 'site:{} '.format('https://www.facebook.com/*posts/')
            query_facebook += kt
            query_facebook += ' after:{} '.format(str(time_after_dt)[:10])
            query_facebook += ' before:{} '.format(str(time_before_dt)[:10])
            queries_facebook.append(query_facebook)

            save_dir_volume = 'Volume-FACEBOOK/{}/Total-KD/'.format(category_en)
            save_dir_links = 'Events-FACEBOOK/E{}-KD/'.format(str(time_after_dt)[:10])

            for qf in queries_facebook:
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
                scrolling_attempt = 2  # we'll have 5 attempts before turning scrolling boolean to False

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


                print('Done collecting FB links, now getting volumes ....')
                print('got in total {} unique links'.format(list(set(articles['link']))))

                ####################################### FACEBOOK ############################################
                # links_new = []
                # for l in articles['link']:
                #     if 'locale=ar_AR' in l:
                #         links_new.append(l.replace('locale=ar_AR', 'locale=en'))
                #     else:
                #         links_new.append(l)
                # articles['link'] = links_new
                facebook_df = pd.DataFrame(articles)
                facebook_df = facebook_df.drop_duplicates()

                try:
                    t1 = time.time()
                    # df = apply_scraping_facebook(search_query=query_facebook, links_precomputed=list(set(articles['link'])))
                    if not os.path.isfile(os.path.join(save_dir_volume, 'Facebook.xlsx')):
                        with pd.ExcelWriter(os.path.join(save_dir_volume, 'Facebook.xlsx')) as writer:
                            # df.to_excel(writer, sheet_name='E{}-{}'.format(str(time_after_dt)[:10], j), index=False)
                            facebook_df.to_excel(writer, sheet_name='E{}-{}'.format(str(time_after_dt)[:10], j), index=False)
                        writer.close()
                    else:
                        book = load_workbook(os.path.join(save_dir_volume, 'Facebook.xlsx'))
                        writer = pd.ExcelWriter(os.path.join(save_dir_volume, 'Facebook.xlsx'), engine='openpyxl')
                        writer.book = book

                        # df.to_excel(writer, sheet_name='E{}-{}'.format(str(time_after_dt)[:10], j), index=False)
                        facebook_df.to_excel(writer, sheet_name='E{}-{}'.format(str(time_after_dt)[:10], j), index=False)
                        writer.close()

                    t2 = time.time()
                    print('This process took {} mins'.format((t2 - t1) / 60))

                    file_name = 'E{}-DB.txt'.format(str(time_after_dt)[:10])

                    if not os.path.isfile(os.path.join(save_dir_links, file_name)):
                        # db_links = list(df['Link'])
                        db_links = list(facebook_df['Link'])
                        with open(os.path.join(save_dir_links, file_name), 'w') as f:
                            for link in db_links:
                                f.write(link + '\n')
                        f.close()
                    else:
                        # db_links = list(df['Link'])
                        db_links = list(facebook_df['Link'])
                        with open(os.path.join(save_dir_links, file_name), 'a') as f:
                            for link in db_links:
                                f.write(link + '\n')
                        f.close()

                except:
                    print('Did not find results for query {}'.format(keywords_text))

                j += 1


    # articles = {'title': [], 'link': []}
    #
    # driver.get('http://www.google.com')
    # search = driver.find_element_by_name('q')
    # search.send_keys(query)
    # search.send_keys(Keys.RETURN)
    #
    # SCROLL_PAUSE_TIME = 2  # I'll use this variable for code sleeping time
    # delay = 30  # delay time for WebDriver (in seconds)
    # scrolling = True  # boolean value -> TRUE means that we're still scrolling, FALSE means we're not scrolling anymore
    # last_height = driver.execute_script("return document.documentElement.scrollHeight")  # this is our last/current position on the page
    # scrolling_attempt = 5  # we'll have 5 attempts before turning scrolling boolean to False
    #
    # # video_links, comments_video, posts_links, comments_posts = [], [], [], []
    #
    # while scrolling == True:
    #     htmlelement = driver.find_element_by_tag_name("body")  # locate html tag
    #     htmlelement.send_keys(Keys.END)
    #
    #     new_height = driver.execute_script("return document.documentElement.scrollHeight")  # calculate current position
    #     time.sleep(SCROLL_PAUSE_TIME)  # make pause because scrolling will take 0.5/1 seconds
    #     driver.implicitly_wait(30)  # make longer pause if loading new comments takes longer
    #
    #     try:
    #         article_titles, article_links = scrape_query_search_results()
    #         articles['title'].extend(article_titles)
    #         articles['link'].extend(article_links)
    #     except:
    #         pass
    #
    #     try:
    #         all_spans = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'span')))
    #         for span in all_spans:
    #             if span.text == 'More results':
    #                 driver.execute_script("arguments[0].scrollIntoView();", span)
    #                 driver.execute_script("arguments[0].click();", span)
    #                 time.sleep(3)
    #                 break
    #     except:
    #         pass
    #
    #     if new_height == last_height:  # if current position  is the same as last position, it means we've reached bottom of the page, so we'll break the loop
    #         scrolling_attempt -= 1
    #         print(f"scrolling attempt {scrolling_attempt}")
    #         if (scrolling_attempt == 0):
    #             scrolling = False  # this will break while loop
    #     last_height = new_height  # if current position is not the same as last one, we'll set last position as new height
    #

    # google_query_dir = 'query_google/'
    # mkdir(google_query_dir)
    # sub_folder_name = ''
    # if keywords_text.strip() != '':
    #     if 'https' in keywords_text:
    #         keywords_text = keywords_text.replace(":", "").replace("/", "").replace(".", "_")
    #     sub_folder_name += 'keywords_' + keywords_text + '_'
    #
    # if time_after is not None:
    #     sub_folder_name += 'after_{}'.format(time_after) + '_'
    # if time_before is not None:
    #     sub_folder_name += 'before_{}'.format(time_before) + '_'
    #
    # if keywords_AND.strip() != '':
    #     if 'https' in keywords_AND or 'http' in keywords_AND:
    #         keywords_AND = keywords_AND.replace(":", "").replace("/", "").replace(".", "_")
    #     sub_folder_name += 'keywords_' + 'AND'.join(keywords_AND.split(' ')) + '_'
    #
    # if keywords_OR.strip() != '':
    #     if 'https' in keywords_OR:
    #         keywords_OR = keywords_OR.replace(":", "").replace("/", "").replace(".", "_")
    #     sub_folder_name += 'keywords_' + 'OR'.join(keywords_OR.split(' ')) + '_'
    #
    # if query_keywords_text is not None:
    #     if 'https' in query_keywords_text or 'http' in query_keywords_text:
    #         query_keywords_text = query_keywords_text.replace(":", "").replace("/", "").replace(".", "_")
    #     sub_folder_name += 'intext_' + '_'.join(query_keywords_text.split(' ')) + '_'
    #
    # if query_keywords_url is not None:
    #     if 'https' in query_keywords_url or 'http' in query_keywords_url:
    #         query_keywords_url = query_keywords_url.replace(":", "").replace("/", "").replace(".", "_")
    #     sub_folder_name += 'inurl_' + '_'.join(query_keywords_url.split(' ')) + '_'
    #
    # if website_url.strip() != '':
    #     sub_folder_name += 'site_' + website_url.strip().replace(':', '').replace('/', '').replace('.', '') + '/'
    #
    # save_dir = os.path.join(google_query_dir, sub_folder_name + "/")
    # mkdir(save_dir)
    #
    # df = pd.DataFrame(articles)
    # df = df.drop_duplicates()
    # with open(os.path.join(save_dir, 'links.txt'), 'w') as f:
    #     for i, row in df.iterrows():
    #         f.write(row['link'] + '\n')
    # f.close()
    # df.to_excel(os.path.join(save_dir, 'articles_titles_links.xlsx'), index=False)