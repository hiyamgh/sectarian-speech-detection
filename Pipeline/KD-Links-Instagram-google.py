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


def login_instagram():
    url = "https://www.instagram.com/accounts/login/"
    driver.get(url)

    inputs = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'input')))

    username = inputs[0]
    print(username.get_attribute('innerHTML'))
    # username = WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[name="username"]')))
    username.send_keys("fatimamarsad@gmail.com")
    username.send_keys(Keys.ENTER)

    password = inputs[1]
    # password = WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[name="password"]')))
    password.send_keys("fatimamarsad2023!")
    password.send_keys(Keys.ENTER)


def apply_scraping_comments_instagram_updated(links_precomputed):
    all_data = {'Link': [], 'Day': [], 'Comments Volume': []}
    for link in tqdm(links_precomputed):
        link = '/'.join(link.split('/')[:5])

        if link.split('/')[3] not in ['p', 'reel']:
            print(f'skipping {link}')
            continue
        print(f'processing link {link}')

        driver.get(link)
        time.sleep(random.randint(5, 10))

        # comments_body = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.x5yr21d.xw2csxc.x1odjw0f.x1n2onr6')))[0]

        comments_old = []

        # In case there is a plus button for loading more comments
        while True:
            try:
                load_more_btn = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'button._abl-')))
                found = False
                for b in load_more_btn:
                    if b.find_element_by_css_selector('svg').get_attribute('aria-label') == 'Load more comments':
                        found = True
                        driver.execute_script("arguments[0].scrollIntoView();", b)
                        b.click()
                        time.sleep(5)
                if not found:
                    break
            except:
                break


        while True:
            # driver.execute_script("arguments[0].scrollIntoView();", comments_body)
            try:
                # comments_new = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'li._a9zj._a9zl')))

                try:
                    comments_new = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.x9f619.xjbqb8w.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.xsag5q8.xz9dl7a.x1uhb9sk.x1plvlek.xryxfnj.x1c4vz4f.x2lah0s.x1q0g3np.xqjyukv.x1qjc9v5.x1oa3qoh.x1nhvcw1')))
                except:
                    try:
                        comments_new = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.x1qjc9v5.x972fbf.xcfux6l.x1qhh985.xm0m39n.x9f619.x78zum5.xdt5ytf.x2lah0s.xk390pu.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x1n2onr6.xggy1nq.x11njtxf')))
                    except:
                        pass

                driver.execute_script("arguments[0].scrollIntoView();", comments_new[-1])
                time.sleep(5)

                if len(comments_new) == len(comments_old):
                    try:
                        print(f'GOT SO FAR {len(comments_new)} - GETTING HIDDEN REPLIES')
                        btn_view_hidden = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.x9f619.xjbqb8w.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.xwib8y2.x1y1aw1k.x1uhb9sk.x1plvlek.xryxfnj.x1c4vz4f.x2lah0s.x1q0g3np.xqjyukv.x6s0dn4.x1oa3qoh.x1nhvcw1')))
                        for b in btn_view_hidden:
                            try:
                                driver.execute_script("arguments[0].scrollIntoView();", b)
                                driver.execute_script("arguments[0].click();", b)
                                time.sleep(5)
                            except:
                                pass
                        comments_new = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((
                                                                                                              By.CSS_SELECTOR,
                                                                                                              'div.x9f619.xjbqb8w.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.xsag5q8.xz9dl7a.x1uhb9sk.x1plvlek.xryxfnj.x1c4vz4f.x2lah0s.x1q0g3np.xqjyukv.x1qjc9v5.x1oa3qoh.x1nhvcw1')))
                        comments_old = comments_new
                        break
                    except:
                        pass

                    try:
                        btn_view_hidden_v2 = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'button._acan._acao._acas._aj1-._ap30')))
                        for b in btn_view_hidden_v2:
                            try:
                                driver.execute_script("arguments[0].scrollIntoView();", b)
                                driver.execute_script("arguments[0].click();", b)
                                time.sleep(5)
                            except:
                                pass
                    except:
                        pass

                    break
                comments_old = comments_new
            except:
                print('End of scrolling')
                break

        # Reveal hidden comments
        try:
            btn_view_hidden =  WebDriverWait(driver, 2).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.x1i10hfl.xjbqb8w.x6umtig.x1b1mbwd.xaqea5y.xav7gou.x9f619.x1ypdohk.xt0psk2.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x16tdsg8.x1hl2dhg.xggy1nq.x1a2a7pz.x87ps6o.x1d5wrs8')))
            for b in btn_view_hidden:
                try:
                    b.click()
                except:
                    pass
                # driver.execute_script("arguments[0].scrollIntoView();", b)
                # driver.execute_script("arguments[0].click();", b)
        except:
            pass
        try:
            comments_new = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,
                                                                                                   'div.x9f619.xjbqb8w.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.xsag5q8.xz9dl7a.x1uhb9sk.x1plvlek.xryxfnj.x1c4vz4f.x2lah0s.x1q0g3np.xqjyukv.x1qjc9v5.x1oa3qoh.x1nhvcw1')))
        except:
            try:
                comments_new = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,
                                                                                                       'div.x1qjc9v5.x972fbf.xcfux6l.x1qhh985.xm0m39n.x9f619.x78zum5.xdt5ytf.x2lah0s.xk390pu.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x1n2onr6.xggy1nq.x11njtxf')))
            except:
                pass
        comments_old = comments_new

        print(f'Total number of comments: {len(comments_old)}')
        try:
            post_time = comments_old[0].find_element_by_css_selector('time').get_attribute('datetime')
        except:
            try:
                post_time = comments_old[1].find_element_by_css_selector('time').get_attribute('datetime')
            except:
                post_time = ''
        print(f'post time: {post_time}')

        try:
            all_data['Link'].append(link)
            all_data['Day'].append(post_time)
            all_data['Comments Volume'].append(len(comments_old)-1)
        except:
            all_data['Link'].append('')
            all_data['Day'].append('')
            all_data['Comments Volume'].append('')

        print(all_data)

    return all_data


def apply_scraping_instagram(links_precomputed):
    login_instagram()
    time.sleep(10)

    SCROLL_PAUSE_TIME = 2  # I'll use this variable for code sleeping time
    delay = 30  # delay time for WebDriver (in seconds)
    scrolling = True  # boolean value -> TRUE means that we're still scrolling, FALSE means we're not scrolling anymore
    last_height = driver.execute_script("return document.documentElement.scrollHeight")  # this is our last/current position on the page
    scrolling_attempt = 3  # we'll have 5 attempts before turning scrolling boolean to False

    all_data = {
        'Link': [],
        'Day': [],
        'Comments Volume': []
    }

    try:
        data = apply_scraping_comments_instagram_updated(links_precomputed=links_precomputed)
        all_data['Link'] = data['Link']
        all_data['Day'] = data['Day']
        all_data['Comments Volume'] = data['Comments Volume']
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

        if i < 17:
            continue

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

            queries_instagram = []

            query_instagram = 'site:{} '.format('https://www.instagram.com/')
            query_instagram += kt
            query_instagram += ' after:{} '.format(str(time_after_dt)[:10])
            query_instagram += ' before:{} '.format(str(time_before_dt)[:10])
            queries_instagram.append(query_instagram)

            save_dir_volume = 'Volume-New/{}/Total-KD/'.format(category_en)
            save_dir_links = 'Events-New/E{}-KD/'.format(str(time_after_dt)[:10])

            for qf in queries_instagram:
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


                print('Done collecting IG links, now getting volumes ....')
                print('got in total {} unique links'.format(list(set(articles['link']))))

                try:
                    t1 = time.time()
                    instagram_df = apply_scraping_instagram(links_precomputed=list(set(articles['link'])))
                    if not os.path.isfile(os.path.join(save_dir_volume, 'Instagram.xlsx')):
                        with pd.ExcelWriter(os.path.join(save_dir_volume, 'Instagram.xlsx')) as writer:
                            # df.to_excel(writer, sheet_name='E{}-{}'.format(str(time_after_dt)[:10], j), index=False)
                            instagram_df.to_excel(writer, sheet_name='E{}-{}'.format(str(time_after_dt)[:10], j), index=False)
                        writer.close()
                    else:
                        book = load_workbook(os.path.join(save_dir_volume, 'Instagram.xlsx'))
                        writer = pd.ExcelWriter(os.path.join(save_dir_volume, 'Instagram.xlsx'), engine='openpyxl')
                        writer.book = book

                        # df.to_excel(writer, sheet_name='E{}-{}'.format(str(time_after_dt)[:10], j), index=False)
                        instagram_df.to_excel(writer, sheet_name='E{}-{}'.format(str(time_after_dt)[:10], j), index=False)
                        writer.close()

                    t2 = time.time()
                    print('This process took {} mins'.format((t2 - t1) / 60))

                    file_name = 'E{}-DB.txt'.format(str(time_after_dt)[:10])

                    if not os.path.isfile(os.path.join(save_dir_links, file_name)):
                        # db_links = list(df['Link'])
                        db_links = list(instagram_df['Link'])
                        with open(os.path.join(save_dir_links, file_name), 'w') as f:
                            for link in db_links:
                                f.write(link + '\n')
                        f.close()
                    else:
                        # db_links = list(df['Link'])
                        db_links = list(instagram_df['Link'])
                        with open(os.path.join(save_dir_links, file_name), 'a') as f:
                            for link in db_links:
                                f.write(link + '\n')
                        f.close()

                except:
                    print('Did not find results for query {}'.format(keywords_text))

                j += 1