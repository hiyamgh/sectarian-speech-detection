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


def login_facebook():
    url = 'https://www.facebook.com/login/'
    driver.get(url)

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

        return all_data
    else:
        all_data = {'Link': [], 'Day': [], 'scraping_time': [], 'Comments Volume': []}
        # all_links_posts = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a.x1i10hfl.xjbqb8w.x6umtig.x1b1mbwd.xaqea5y.xav7gou.x9f619.x1ypdohk.xt0psk2.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x16tdsg8.x1hl2dhg.xggy1nq.x1a2a7pz.x1heor9g.xt0b8zv.xo1l8bm')))
        # all_dates = [a.text for a in all_links_posts]
        all_links_posts = links_precomputed
        for i, post in enumerate(all_links_posts):
            if 'pfbid' in post or 'photo' in post or 'post' in post:
                if i == 13:
                    print()
                print('post link: {}'.format(i))
                driver.get(post)
                time.sleep(random.randint(3, 5))
                comment_numbers = []

                try:
                    comment_nb = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'span.x193iq5w.xeuugli.x13faqbe.x1vvkbs.x1xmvt09.x1lliihq.x1s928wv.xhkezso.x1gmr53x.x1cpjm7i.x1fgarty.x1943h6x.xudqn12.x3x7a5m.x6prxxf.xvq8zen.xo1l8bm.xi81zsa')))
                    comment_numbers.append(';'.join([cn.text for cn in comment_nb]))
                    print(comment_nb)
                except:
                    print('in except 1')
                    try:
                        all_spans = [s.text for s in WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'span.x193iq5w.xeuugli.x13faqbe.x1vvkbs.x1xmvt09.x1lliihq.x1s928wv.xhkezso.x1gmr53x.x1cpjm7i.x1fgarty.x1943h6x.xudqn12.x3x7a5m.x6prxxf.xvq8zen.xo1l8bm.xi81zsa')))]
                        comment_numbers.extend(all_spans)
                        print(all_spans)
                    except:
                        print('in except 2')
                        comment_nb = 0
                        comment_numbers.append(comment_nb)
                        print(comment_nb)

                try:
                    date_watch = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,'a.x1i10hfl.xjbqb8w.x6umtig.x1b1mbwd.xaqea5y.xav7gou.x9f619.x1ypdohk.xt0psk2.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x16tdsg8.x1hl2dhg.xggy1nq.x1a2a7pz.x1heor9g.xt0b8zv.xo1l8bm')))[0].text
                except:
                    print('in except 3')
                    date_watch = ''
                # print('{} - {} comments on the post: {}'.format(all_dates[i], comment_nb, post))
                print('{} - {} comments on the post: {}'.format('', ','.join([str(c) for c in comment_numbers]), post))

                try:
                    all_data['Link'].append(post)
                    # all_data['Day'].append(all_dates[i])
                    all_data['Day'].append(date_watch)
                    all_data['scraping_time'].append(str(time.time()))
                    all_data['Comments Volume'].append(';'.join([str(c) for c in comment_numbers]))
                    print('The list that we will be joining: {}'.format(';'.join([str(c) for c in comment_numbers])))
                    print(all_data)
                except:
                    print('in except 4')
                    all_data['Link'].append(post)
                    all_data['Day'].append('')
                    all_data['scraping_time'].append(str(time.time()))
                    all_data['Comments Volume'].append('')
                    print('The list that we will be joining: {}'.format(''))
                    print(all_data)
        print('Done for current posts')
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
                try:
                    date_watch = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a.x1i10hfl.xjbqb8w.x6umtig.x1b1mbwd.xaqea5y.xav7gou.x9f619.x1ypdohk.xt0psk2.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x16tdsg8.x1hl2dhg.xggy1nq.x1a2a7pz.x1heor9g.xt0b8zv.xo1l8bm')))[0].text
                except:
                    date_watch = ''
                print('{} - {} comments on the post: {}'.format(date_watch, comments_watch, watch))

                all_data['Link'].append(watch)
                all_data['Day'].append(date_watch)
                all_data['scraping_time'].append(str(time.time()))
                all_data['Comments Volume'].append(comments_watch)

        return all_data


def apply_scraping_facebook(search_query, links_precomputed=None):
    # login_facebook()
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
            print(data)
            all_data['Link'].extend(data['Link'])
            all_data['Day'].extend(data['Day'])
            all_data['scraping_time'].extend(data['scraping_time'])
            all_data['Comments Volume'].extend(data['Comments Volume'])
        except:
            pass

        try:
            data = get_facebook_volumes_videos(driver=driver, links_precomputed=links_precomputed)
            print(data)
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

    login_facebook()

    for subdir, dirs, files in os.walk('Volume-FACEBOOK/'):
        for file in files:
            if 'Accounts' not in file and 'Total-KD' in subdir and 'Facebook' in file and 'Comments' not in file:
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
                        links_new = []
                        for link in list([str(l) for l in list(df['link'])]):
                            # https://www.facebook.com/groups/107172179392330/?locale=fi_FI
                            result = re.search('locale=[a-z]{2}_[A-Z]{2}', link)
                            if result:
                                print('This link matched: {}'.format(link))
                                link_new = re.sub('locale=[a-z]{2}_[A-Z]{2}', 'locale=en_EN', link)
                                print('New link: {}'.format(link_new))
                            else:
                                link_new = link

                            links_new.append(link_new)
                        df['link'] = links_new

                        save_dir_volume = 'Volume-FACEBOOK/{}/Total-KD/'.format(category)
                        comments_df = apply_scraping_facebook(search_query='', links_precomputed=list(set(df['link'])))
                        if not os.path.isfile(os.path.join(save_dir_volume, 'Facebook-Comments.xlsx')):
                            with pd.ExcelWriter(os.path.join(save_dir_volume, 'Facebook-Comments.xlsx')) as writer:
                                # df.to_excel(writer, sheet_name='E{}-{}'.format(str(time_after_dt)[:10], j), index=False)
                                comments_df.to_excel(writer, sheet_name=sheet_name, index=False)
                            writer.close()
                        else:
                            book = load_workbook(os.path.join(save_dir_volume, 'Facebook-Comments.xlsx'))
                            writer = pd.ExcelWriter(os.path.join(save_dir_volume, 'Facebook-Comments.xlsx'), engine='openpyxl')
                            writer.book = book

                            # df.to_excel(writer, sheet_name='E{}-{}'.format(str(time_after_dt)[:10], j), index=False)
                            comments_df.to_excel(writer, sheet_name=sheet_name, index=False)
                            writer.close()



# # open tab
#                     # driver.get("http://www.google.com/")
#
#
#
#                     # for link in links_new:
#                     #     # driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 't')
#                     #     # driver.get(link)
#                     #     # driver.execute_script("window.open('about:blank','secondtab');")
#                     #     #
#                     #     # # It is switching to second tab now
#                     #     # driver.switch_to.window("secondtab")
#                     #
#                     #     # driver.switch_to.new_window(window.WindowTypes.TAB)
#                     #     driver.get(link)
#                     #     driver.execute_script("window.open('');")
#                     #     chwd = driver.window_handles
#                     #     driver.switch_to.window(chwd[-1])
#
#                     # try:
#                     #     df = apply_scraping_facebook(search_query='', links_precomputed=list(set(df['link'])))
#                     #     df.to_excel(os.path.join(subdir, f'Facebook-{sheet_name}.xlsx'))
#                     #     print(df)
#                     #     print('==================================================================================')
#                     # except:
#                     #     pass