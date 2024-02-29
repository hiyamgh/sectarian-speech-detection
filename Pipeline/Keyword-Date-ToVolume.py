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
        os.mkdir(folder_name)


# def scrape_query_search_results():
#     all_articles = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.yuRUbf')))
#     print(len(all_articles))
#
#     all_titles = []
#     for a in all_articles:
#         try:
#             title = a.find_element_by_css_selector('div.yuRUbf a h3').text
#             print(title)
#         except:
#             title = ''
#             print('did not find title')
#         all_titles.append(title)
#
#     all_links = []
#     for a in all_articles:
#         try:
#             link = a.find_element_by_css_selector('div.yuRUbf a').get_attribute('href')
#             print(link)
#         except:
#             link = ''
#             print('did not find link')
#         all_links.append(link)
#
#     for i in itertools.zip_longest(all_titles, all_links):
#         print(i)
#         print('===================================')
#
#     return all_titles, all_links


def get_accounts_per_entity():
    ''' creates a mapping between an entity (channel) and social media accounts associated with that entity '''
    df = pd.read_excel('Accounts.xlsx')
    entities = list(df['Name'])
    facebook_accs = list(df['Facebook Account'])
    twitter_accs = list(df['Twitter Account '])
    instagram_accs = list(df['Instagram Account'])
    youtube_accs = list(df['Youtube Account'])

    entities2accs = {} # dictionary mapping entities to accounts
    for i, ent in enumerate(entities):
        entities2accs[ent] = {}
        entities2accs[ent]['facebook'] = facebook_accs[i]
        entities2accs[ent]['twitter'] = twitter_accs[i]
        entities2accs[ent]['instagram'] = instagram_accs[i]
        entities2accs[ent]['youtube'] = youtube_accs[i]

    return entities2accs



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

# https://twitter.com/search?q=%D8%B7%D9%88%D9%81%D8%A7%D9%86%20%D8%A7%D9%84%D8%A7%D9%82%D8%B5%D9%89%20until%3A2023-11-22%20since%3A2023-11-19&src=typed_query



def get_youtube_volumes():
    videos = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'ytd-video-renderer')))
    all_links = []
    meta_data = []
    days = []
    all_comments_volume = []

    for v in videos:
        meta = v.find_element_by_css_selector('div#metadata').text
        link = v.find_element_by_css_selector('a#video-title').get_attribute('href')
        all_links.append(link)
        meta_data.append(meta)
        print('meta: {}\nvideo link: {}\n\n'.format(meta, link))

    print('=========================================================================')
    for link in all_links:
        driver.get(link)
        time.sleep(random.randint(5, 10))
        snippet = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div#snippet')))
        driver.execute_script("arguments[0].scrollIntoView();", snippet[0])
        driver.execute_script("arguments[0].click();", snippet[0])
        day = driver.find_element_by_css_selector('ytd-watch-info-text#ytd-watch-info-text').text
        print(day.strip())

        day_list = day.strip().split(' ')
        day_actual = day.strip()
        for i in range(len(day_list)):
            if day_list[i] in ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']:
                day_actual = ' '.join(day_list[i-1:i+2])
                break
        print('Day Actual: {}'.format(day_actual))
        days.append(day_actual)

        try:
            comments = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div#title h2#count')))
            comments_list = comments.text.strip().split(' ')
            comments_volume = comments.text.strip()
            for i in range(len(comments_list)):
                if comments_list[i] == 'Comments':
                    comments_volume = ' '.join(comments_list[i-1:i+1])
                    break
            print('Comments volume: {}'.format(comments_volume))
            all_comments_volume.append(comments_volume)
        except:
            print('Comments are turned off. Learn more')
            all_comments_volume.append('Comments are turned off. Learn more')

        if len(all_comments_volume) % 5 == 0:
            data = {
                'Link': all_links,
                'Meta Data': meta_data,
                'Day': days + ['' for _ in range(len(all_links) - len(days))],
                'Comments Volume': all_comments_volume + ['' for _ in range(len(all_links) - len(days))]
            }
            df = pd.DataFrame(data)
            df.to_excel('YouTubeVolume.xlsx', index=False)

        print('=========================================================================')
        time.sleep(random.randint(5, 10))

    data = {
        'Link': all_links,
        'Meta Data': meta_data,
        'Day': days,
        'Comments Volume': all_comments_volume
    }
    df = pd.DataFrame(data)
    df.to_excel('YouTubeVolume.xlsx', index=False)
    return df


def apply_scraping_youtube(search_query):
    driver.get('https://www.youtube.com/results?search_query={}'.format(search_query))
    time.sleep(random.randint(5, 10))

    SCROLL_PAUSE_TIME = 2  # I'll use this variable for code sleeping time
    delay = 30  # delay time for WebDriver (in seconds)
    scrolling = True  # boolean value -> TRUE means that we're still scrolling, FALSE means we're not scrolling anymore
    last_height = driver.execute_script("return document.documentElement.scrollHeight")  # this is our last/current position on the page
    scrolling_attempt = 5  # we'll have 5 attempts before turning scrolling boolean to False

    # video_description = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div#description-inner')))
    while scrolling == True:
        htmlelement = driver.find_element_by_tag_name("body")  # locate html tag
        htmlelement.send_keys(Keys.END)

        new_height = driver.execute_script("return document.documentElement.scrollHeight")  # calculate current position
        time.sleep(SCROLL_PAUSE_TIME)  # make pause because scrolling will take 0.5/1 seconds
        driver.implicitly_wait(30)  # make longer pause if loading new comments takes longer

        if new_height == last_height:  # if current position  is the same as last position, it means we've reached bottom of the page, so we'll break the loop
            scrolling_attempt -= 1
            print(f"scrolling attempt {scrolling_attempt}")
            if (scrolling_attempt == 0):
                scrolling = False  # this will break while loop
        last_height = new_height  # if current position is not the same as last one, we'll set last position as new height



    df = get_youtube_volumes()
    return df


def login_twitter():
    ''' function that logs in to twitter using Hiyam's credentials for now '''

    url = "https://twitter.com/i/flow/login"
    driver.get(url)
    username = WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[autocomplete="username"]')))
    username.send_keys("fatimamarsad")
    username.send_keys(Keys.ENTER)

    password = WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[name="password"]')))
    password.send_keys("rinro8-fAdbym-recjic")
    password.send_keys(Keys.ENTER)
    time.sleep(30)


def get_twitter_volumes():
    tweets = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'article[data-testid="tweet"]')))
    links, volumes, days = [], [], []
    for t in tweets:
        try:
            link = t.find_elements_by_css_selector('a')[3].get_attribute('href')
            # comments_volume = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.css-175oi2r.r-1kbdv8c.r-18u37iz.r-1wtj0ep.r-1ye8kvj.r-1s2bzr4 div')))[0].text
            # comments_volume = t.text.split('\n')
            comments_volume = [e.text for e in t.find_elements_by_css_selector('div.css-175oi2r div[role="group"] div.css-175oi2r.r-18u37iz.r-1h0z5md.r-13awgt0')][0]
            if comments_volume.strip() == '':
                comments_volume = '0'
            day = t.find_element_by_css_selector('time').get_attribute('datetime')

            print(link)
            print('Comments volume: {}'.format(comments_volume))
            print('Day: {}'.format(day))
            print('=========================================')

            links.append(link)
            volumes.append(comments_volume)
            days.append(day)

        except:
            pass

        print(len(links), len(volumes), len(days))

    data = {
        'Link': links,
        'Day': days,
        'Comments Volume': volumes
    }
    return data



def apply_scraping_twitter(search_query):
    driver.get('https://twitter.com/search?q={}'.format(search_query))
    time.sleep(random.randint(5, 10))

    SCROLL_PAUSE_TIME = 2  # I'll use this variable for code sleeping time
    delay = 30  # delay time for WebDriver (in seconds)
    scrolling = True  # boolean value -> TRUE means that we're still scrolling, FALSE means we're not scrolling anymore
    last_height = driver.execute_script("return document.documentElement.scrollHeight")  # this is our last/current position on the page
    scrolling_attempt = 5  # we'll have 5 attempts before turning scrolling boolean to False

    all_data = {
        'Link': [],
        'Day': [],
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
            data = get_twitter_volumes()
            all_data['Link'].extend(data['Link'])
            all_data['Day'].extend(data['Day'])
            all_data['Comments Volume'].extend(data['Comments Volume'])

        except:
            pass

        if new_height == last_height:  # if current position  is the same as last position, it means we've reached bottom of the page, so we'll break the loop
            scrolling_attempt -= 1
            print(f"scrolling attempt {scrolling_attempt}")
            if (scrolling_attempt == 0):
                scrolling = False  # this will break while loop
        last_height = new_height  # if current position is not the same as last one, we'll set last position as new height

    df = pd.DataFrame(all_data)
    df = df.drop_duplicates()
    # df.to_excel('TwitterVolume.xlsx', index=False)
    return df


# def apply_scraping_facebook(search_query):
#     login_facebook()
#     time.sleep(random.randint(10, 15))
#
#     # get the videos
#     driver.get('https://www.facebook.com/search/videos?q={}'.format(search_query))
#     time.sleep(5)
#
#     SCROLL_PAUSE_TIME = 2  # I'll use this variable for code sleeping time
#     delay = 30  # delay time for WebDriver (in seconds)
#     scrolling = True  # boolean value -> TRUE means that we're still scrolling, FALSE means we're not scrolling anymore
#     last_height = driver.execute_script("return document.documentElement.scrollHeight")  # this is our last/current position on the page
#     scrolling_attempt = 5  # we'll have 5 attempts before turning scrolling boolean to False
#
#     video_links, comments_video, posts_links, comments_posts = [], [], [], []
#
#     while scrolling == True:
#         htmlelement = driver.find_element_by_tag_name("body")  # locate html tag
#         htmlelement.send_keys(Keys.END)
#
#         new_height = driver.execute_script("return document.documentElement.scrollHeight")  # calculate current position
#         time.sleep(SCROLL_PAUSE_TIME)  # make pause because scrolling will take 0.5/1 seconds
#         driver.implicitly_wait(30)  # make longer pause if loading new comments takes longer
#
#         try:
#             all_links_videos = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a.x1i10hfl.xjbqb8w.x6umtig.x1b1mbwd.xaqea5y.xav7gou.x9f619.x1ypdohk.xt0psk2.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x16tdsg8.x1hl2dhg.xggy1nq.x1a2a7pz.x1heor9g.xt0b8zv.x1s688f')))
#             video_links.extend(all_links_videos)
#
#         except:
#             pass
#
#         if new_height == last_height:  # if current position  is the same as last position, it means we've reached bottom of the page, so we'll break the loop
#             scrolling_attempt -= 1
#             print(f"scrolling attempt {scrolling_attempt}")
#             if (scrolling_attempt == 0):
#                 scrolling = False  # this will break while loop
#         last_height = new_height  # if current position is not the same as last one, we'll set last position as new height
#
#     df = pd.DataFrame(all_data)
#     df = df.drop_duplicates()
#     # df.to_excel('TwitterVolume.xlsx', index=False)
#     return df
#
#
#     driver.get('https://www.facebook.com/movieseriesquotess/posts/pfbid02W3PZAeS9LunACHuSh8enbxrwMBDcRom9rEhNJ1E7cqZg2Hqs8r1KfU7YtCi7iG9Cl')
#     time.sleep(5)
#     comment_nb = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'span.x193iq5w.xeuugli.x13faqbe.x1vvkbs.x1xmvt09.x1lliihq.x1s928wv.xhkezso.x1gmr53x.x1cpjm7i.x1fgarty.x1943h6x.xudqn12.x3x7a5m.x6prxxf.xvq8zen.xo1l8bm.xi81zsa')))[1].text
#
#     driver.get('https://www.facebook.com/watch?v=863727587743953')
#     time.sleep(5)
#     comments_watch = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,
#                                                                                              'span.x193iq5w.xeuugli.x13faqbe.x1vvkbs.x1xmvt09.x1lliihq.x1s928wv.xhkezso.x1gmr53x.x1cpjm7i.x1fgarty.x1943h6x.x4zkp8e.x676frb.x1nxh6w3.x1sibtaa.xo1l8bm.xi81zsa')))[
#         0].text
#
#     driver.get('')
#
#     # x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x6prxxf xvq8zen xo1l8bm xi81zsa
#
#     driver.get(
#         'https://www.facebook.com/search/top?q=%D8%B7%D9%88%D9%81%D8%A7%D9%86%20%D8%A7%D9%84%D8%A7%D9%82%D8%B5%D9%89')
#     time.sleep(10)
#
#     # posts
#     all_links_posts = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,
#                                                                                               'a.x1i10hfl.xjbqb8w.x6umtig.x1b1mbwd.xaqea5y.xav7gou.x9f619.x1ypdohk.xt0psk2.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x16tdsg8.x1hl2dhg.xggy1nq.x1a2a7pz.x1heor9g.xt0b8zv.xo1l8bm')))
#     print()
#
#     driver.get('https://www.facebook.com/search/videos?q=%D8%B7%D9%88%D9%81%D8%A7%D9%86%20%D8%A7%D9%84%D8%A7%D9%82%D8%B5%D9%89')
#     print()


def add_volume_sheet_youtube(save_dir, df1, time_after, time_before):
    file_name = 'E'
    if time_after is not None:
        file_name += time_after
    if time_before is not None:
        file_name += '-' + time_before
    file_name += '-DB.txt'
    db_links = list(df['Link'])
    with open(os.path.join(save_dir, file_name), 'w') as f:
        for link in db_links:
            f.write(link + '\n')
    f.close()


    writer = pd.ExcelWriter(os.path.join(save_dir, 'YouTubeVolumeMod.xlsx'), engine='xlsxwriter')
    df2 = df1
    # comments_volume_updated = [int(l.split(' ')[0]) for l in list(df1['Comments Volume'])]
    comments_volume_updated = []
    for l in list(df1['Comments Volume']):
        try:
            comments_volume_updated.append(int(l.split(' ')[0]))
        except:
            comments_volume_updated.append(0)

    df2['Comments Volume'] = comments_volume_updated

    days_unique = list(set(list(df1['Day'])))
    data = []
    for d in days_unique:
        df_sub = df2[df2['Day'] == d]
        volume = 0
        links = len(df_sub)
        for i, row in df_sub.iterrows():
            volume += int(row['Comments Volume'])

        data.append([d, links, volume])

    df3 = pd.DataFrame(data, columns=['Day', 'Links', 'Comments Volume'])

    df1.to_excel(writer, sheet_name='original', index=False)
    df3.to_excel(writer, sheet_name='volume aggregation', index=False)
    writer.close()


def add_volume_sheet_twitter(save_dir, df1, time_after, time_before):
    file_name = 'E'
    if time_after is not None:
        file_name += time_after
    if time_before is not None:
        file_name += '-' + time_before
    file_name += '-DB.txt'
    db_links = list(df['Link'])
    with open(os.path.join(save_dir, file_name), 'w') as f:
        for link in db_links:
            f.write(link + '\n')
    f.close()

    writer = pd.ExcelWriter(os.path.join(save_dir, 'TwitterVolumeMod.xlsx'), engine='xlsxwriter')
    df2 = df1
    dates_updated = [l[:10] for l in list(df1['Day'])]
    df2['Day'] = dates_updated

    days_unique = list(set(list(df2['Day'])))
    data = []
    for d in days_unique:
        df_sub = df2[df2['Day'] == d]
        volume = 0
        links = len(df_sub)
        for i, row in df_sub.iterrows():
            try:
                volume += int(row['Comments Volume'])
            except:
                volume += 0

        data.append([d, links, volume])

    df3 = pd.DataFrame(data, columns=['Day', 'Links', 'Comments Volume'])

    df1.to_excel(writer, sheet_name='original', index=False)
    df3.to_excel(writer, sheet_name='volume aggregation', index=False)

    writer.close()


# FACEBOOK CODES
# login_facebook()
#     time.sleep(random.randint(10, 15))
#
#     driver.get('https://www.facebook.com/search/top?q=%D8%B7%D9%88%D9%81%D8%A7%D9%86%20%D8%A7%D9%84%D8%A7%D9%82%D8%B5%D9%89')
#     time.sleep(10)
#
#     # posts
#     all_links = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a.x1i10hfl.xjbqb8w.x6umtig.x1b1mbwd.xaqea5y.xav7gou.x9f619.x1ypdohk.xt0psk2.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x16tdsg8.x1hl2dhg.xggy1nq.x1a2a7pz.x1heor9g.xt0b8zv.xo1l8bm')))
#     print()
#
#     driver.get('https://www.facebook.com/search/videos?q=%D8%B7%D9%88%D9%81%D8%A7%D9%86%20%D8%A7%D9%84%D8%A7%D9%82%D8%B5%D9%89')
#
#     all_links_videos = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a.x1i10hfl.xjbqb8w.x6umtig.x1b1mbwd.xaqea5y.xav7gou.x9f619.x1ypdohk.xt0psk2.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x16tdsg8.x1hl2dhg.xggy1nq.x1a2a7pz.x1heor9g.xt0b8zv.x1s688f')))
#     print()
#     # https://www.facebook.com/search/videos/?q=%D8%B7%D9%88%D9%81%D8%A7%D9%86%20%D8%A7%D9%84%D8%A7%D9%82%D8%B5%D9%89
#     # x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x1heor9g xt0b8zv xo1l8bm


if __name__ == '__main__':
    driver = webdriver.Chrome('C:\Program Files\chromedriver-win32-119\chromedriver.exe')
    delay = 30
    # driver.get('https://twitter.com/search?q=%D8%B7%D9%88%D9%81%D8%A7%D9%86%20%D8%A7%D9%84%D8%A7%D9%82%D8%B5%D9%89%20until%3A2023-11-22%20since%3A2023-11-19&src=typed_query')
    # https://www.facebook.com/search/videos/?q=%D8%B7%D9%88%D9%81%D8%A7%D9%86%20%D8%A7%D9%84%D8%A7%D9%82%D8%B5%D9%89
    # x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x1heor9g xt0b8zv xo1l8bm

    include_timeframe = input("Do you have a particular time frame of interest? [y, n]: ")
    if include_timeframe.lower() in ['y', 'yes']:
        time_after = input("Do you want to get articles after certain date: YYYY-MM-DD: ")
        time_before = input("Do you want to get articles before certain date: YYYY-MM-DD: ")

        if time_after.strip() == '':
            time_after = None
        if time_before.strip() == '':
            time_before = None
    else:
        time_before, time_after = None, None

    keywords_text = input('Please put any keywords that you want them to appear in text: ')
    keywords_AND = input('Please put any keywords that you want to LOGICALLY combine with an AND: ')
    # keywords_OR = input('Please put any keywords that you want to LOGICALLY combine in an OR: ')
    # website_url = input('Please enter a website url: ')
    platform = input('Please enter a platform of interest, choose from: [facebook, youtube, instagram]: ')

    google_query_dir = 'Output-Raw-KeywordDate2LinkVol/'
    mkdir(google_query_dir)

    sub_folder_name = ''
    if keywords_text.strip() != '':
        if 'https' in keywords_text:
            keywords_text = keywords_text.replace(":", "").replace("/", "").replace(".", "_")
        sub_folder_name += 'keywords_' + keywords_text + '_'

    if time_after is not None:
        sub_folder_name += 'after_{}'.format(time_after) + '_'
    if time_before is not None:
        sub_folder_name += 'before_{}'.format(time_before) + '_'

    if keywords_AND.strip() != '':
        if 'https' in keywords_AND or 'http' in keywords_AND:
            keywords_AND = keywords_AND.replace(":", "").replace("/", "").replace(".", "_")
        sub_folder_name += 'keywords_' + 'AND'.join(keywords_AND.split(' ')) + '_'

    save_dir = os.path.join(google_query_dir, sub_folder_name + "/")
    mkdir(save_dir)

    query_keywords_and = None
    query = ''

    if platform.lower().strip() == 'youtube':
        if keywords_AND.strip() != '':
            splitted = keywords_AND.strip().split(' ')
            for i, k in enumerate(splitted):
                if i == 0 and len(splitted) > 1:
                    query += "\"" + k + "\"+AND+\""
                elif i == len(splitted) - 1:
                    query += "\"" + k + "\""
                else:
                    query += "\"" + k + "\"+AND+"

        if time_after is not None:
            query += '+after%3A{}'.format(time_after)
        #     +after%3A2023-11-19+before%3A2023-11-22

        if time_before is not None:
            query += '+before%3A{}'.format(time_before)
        #     +after%3A2023-11-19+before%3A2023-11-22

        t1 = time.time()
        df = apply_scraping_youtube(search_query=query)
        df.to_excel(os.path.join(save_dir, 'YouTubeVolume.xlsx'), index=False)
        add_volume_sheet_youtube(save_dir=save_dir, df1=df, time_after=time_after, time_before=time_before)
        if os.path.isfile(os.path.join(save_dir, 'YouTubeVolume.xlsx')):
            os.remove(os.path.join(save_dir, 'YouTubeVolume.xlsx'))
        t2 = time.time()

        print('This process took {} mins'.format((t2-t1)/60))

    elif platform.lower().strip() == 'twitter':
        if keywords_AND.strip() != '':
            splitted = keywords_AND.strip().split(' ')
            for i, k in enumerate(splitted):
                if i == 0 and len(splitted) > 1:
                    query += "\"" + k + "\"+AND+"
                elif i == len(splitted) - 1:
                    query += "\"" + k + "\""
                else:
                    query += "\"" + k + "\"+AND+"

        if time_before is not None:
            query += 'until%3A{}'.format(time_before)

        if time_after is not None:
            query += '%20since%3A{}'.format(time_after)

        query += '&src=typed_query'

        login_twitter()

        t1 = time.time()
        df = apply_scraping_twitter(search_query=query)
        df.to_excel(os.path.join(save_dir, 'TwitterVolume.xlsx'), index=False)
        add_volume_sheet_twitter(save_dir=save_dir, df1=df, time_after=time_after, time_before=time_before)
        if os.path.isfile(os.path.join(save_dir, 'TwitterVolume.xlsx')):
            os.remove(os.path.join(save_dir, 'TwitterVolume.xlsx'))
        t2 = time.time()
        print('This process took {} mins'.format((t2 - t1) / 60))

    else:
        pass


    # writer = pd.ExcelWriter(path, engine = 'xlsxwriter')
    # df1.to_excel(writer, sheet_name = 'x1')
    # df2.to_excel(writer, sheet_name = 'x2')
    # writer.close()


    # choose_entity = input('Do you want to choose a social media account of a particular influencer? please choose: [y, n]: ')
    # if choose_entity.lower() == 'y':
    #     influencer = input('Please enter the name of the influencer: ')
    # else:
    #     influencer = None
    # # page_selection = input('Please enter the page numbers of the pages you want to scrape: ')
    # # num_links = int(input('Please enter the total number of links you want to scrape: '))
    #

    # if platform.strip() != '':
    #     if influencer is None:
    #         if platform.lower() == 'facebook':
    #             query += 'site:{} '.format('https://www.facebook.com/')
    #         elif platform.lower() == 'youtube':
    #             query += 'site:{} '.format('https://www.youtube.com/')
    #         elif platform.lower() == 'instagram':
    #             query += 'site:{} '.format('https://www.youtube.com/')
    #     else:
    #         entities2accs = get_accounts_per_entity()
    #         # query += 'site:{}'.format(entities2accs[influencer][platform.lower()])
    #         query += 'site:https://www.facebook.com/AlArabiya/ '
    #
    # if query_keywords_text is not None:
    #     query += ' intext:\"{}\" '.format(query_keywords_text) # worked with quotations
    # if query_keywords_url is not None:
    #     query += 'inurl: \"{}\" '.format(query_keywords_url) #
    #