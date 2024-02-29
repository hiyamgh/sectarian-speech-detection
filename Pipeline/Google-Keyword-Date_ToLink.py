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


def get_article_annahar(article_link):
    driver.get(article_link)
    time.sleep(3)
    try:
        paragraphs = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div#bodyToAddTags div')))
        paragraphs = '\n'.join([p.text for p in paragraphs])
    except:
        paragraphs = ''
    return paragraphs


#     bodyToAddTags
def get_article_bintjbeil(article_link):
    driver.get(article_link)
    time.sleep(3)
    try:
        paragraphs = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'p')))
        paragraphs = '\n'.join([p.text for p in paragraphs])
    except:
        paragraphs = ''
    return paragraphs


def get_article_lebanonfiles(article_link):
    driver.get(article_link)
    time.sleep(3)
    try:
        paragraphs = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'p')))
        paragraphs = '\n'.join([p.text for p in paragraphs])
    except:
        paragraphs = ''
    return paragraphs


def get_article_aljoumhouriya(article_link):
    driver.get(article_link)
    time.sleep(3)
    try:
        paragraphs = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'p')))
        paragraphs = '\n'.join([p.text for p in paragraphs])
    except:
        paragraphs = ''
    return paragraphs

def get_article_sawt_beirut(article_link):
    driver.get(article_link)
    time.sleep(3)
    try:
        paragraphs = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'p')))
        paragraphs = '\n'.join([p.text for p in paragraphs])
    except:
        paragraphs = ''
    return paragraphs


def get_article_lbc(article_link):
    driver.get(article_link)
    time.sleep(3)
    try:
        article = driver.find_element_by_css_selector('div.LongDesc div').text
    except:
        article = ''

    return article


def get_article_mtv(article_link):
    driver.get(article_link)
    time.sleep(3)
    try:
        article = driver.find_element_by_css_selector('div#article-MainText p._pragraphs').text
    except:
        article = ''
    return article


def get_article_kataeb(article_link):
    driver.get(article_link)
    time.sleep(3)
    try:
        paragraphs = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'p')))
        paragraphs = '\n'.join([p.text for p in paragraphs])
    except:
        paragraphs = ''
    return paragraphs


def get_article_nna(article_link):
    driver.get(article_link)
    time.sleep(3)
    try:
        paragraphs = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'p')))
        paragraphs = '\n'.join([p.text for p in paragraphs])
    except:
        paragraphs = ''
    return paragraphs


def get_article_lebanese_forces(article_link):
    driver.get(article_link)
    time.sleep(3)
    try:
        paragraphs = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'p')))
        paragraphs = '\n'.join([p.text for p in paragraphs])
    except:
        paragraphs = ''
    return paragraphs


def get_articles_lebanon24(article_link):
    driver.get(article_link)
    time.sleep(3)
    try:
        paragraphs = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'span')))
        paragraphs = '\n'.join([p.text for p in paragraphs])
    except:
        paragraphs = ''
    return paragraphs


def get_articles_lebanonfiles(article_link):
    driver.get(article_link)
    time.sleep(3)
    try:
        paragraphs = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'p')))
        paragraphs = '\n'.join([p.text for p in paragraphs])
    except:
        paragraphs = ''
    return paragraphs


def get_article_elnashra(article_link):
    driver.get(article_link)
    time.sleep(3)
    try:
        paragraphs = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'p')))
        paragraphs = '\n'.join([p.text for p in paragraphs])
    except:
        paragraphs = ''
    return paragraphs


def get_article_tayyar(article_link):
    driver.get(article_link)
    time.sleep(3)
    try:
        paragraphs = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'p')))
        paragraphs = '\n'.join([p.text for p in paragraphs])
    except:
        paragraphs = ''
    return paragraphs


def get_article_alakhbar(article_link):
    driver.get(article_link)
    time.sleep(3)
    try:
        paragraphs = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'p')))
        paragraphs = '\n'.join([p.text for p in paragraphs])
    except:
        paragraphs = ''
    return paragraphs


def get_article_addiyar(article_link):
    driver.get(article_link)
    time.sleep(3)
    try:
        paragraphs = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'p')))
        paragraphs = '\n'.join([p.text for p in paragraphs])
    except:
        paragraphs = ''
    return paragraphs


def get_article_lebanon_debate(article_link):
    driver.get(article_link)
    time.sleep(3)
    try:
        article = driver.find_element_by_css_selector('span#ctl00_ContentPlaceHolder1_FormView1_newsLabel').text
    except:
        article = ''
    return article


def get_article(article_link):
    if 'annahar' in article_link:
        article = get_article_annahar(article_link=article_link)
    elif 'bintjbeil' in article_link:
        article = get_article_bintjbeil(article_link=article_link)
    elif 'lebanondebate' in article_link:
        article = get_article_lebanon_debate(article_link=article_link)
    elif 'lebanonfiles' in article_link:
        article = get_article_lebanonfiles(article_link=article_link)
    elif 'addiyar' in article_link:
        article = get_article_addiyar(article_link=article_link)
    elif 'al-akhbar' in article_link:
        # article = get_article_alakhbar(article_link=article_link)
        article = ''
    elif 'tayyar' in article_link:
        article = get_article_tayyar(article_link=article_link)
    elif 'elnashra' in article_link:
        article = get_article_elnashra(article_link=article_link)
    elif 'lebanon24' in article_link:
        article = get_articles_lebanon24(article_link=article_link)
    elif 'lebanese-forces' in article_link:
        article = get_article_lebanese_forces(article_link=article_link)
    elif 'aljoumhouria' in article_link:
        article = get_article_aljoumhouriya(article_link=article_link)
    elif 'nna-leb' in article_link:
        article = get_article_nna(article_link=article_link)
    elif 'kataeb' in article_link:
        article = get_article_kataeb(article_link=article_link)
    elif 'mtv' in article_link:
        article = get_article_mtv(article_link=article_link)
    elif 'lbcgroup' in article_link:
        article = get_article_lbc(article_link=article_link)
    else:
        article = get_article_sawt_beirut(article_link=article_link)

    return article


def link_is_news_website(article_link):
    if 'annahar' in article_link:
        return True
    elif 'bintjbeil' in article_link:
        return True
    elif 'lebanondebate' in article_link:
        return True
    elif 'lebanonfiles' in article_link:
        return True
    elif 'addiyar' in article_link:
        return True
    # elif 'al-akhbar' in article_link:
    #     return True
    elif 'tayyar' in article_link:
        return True
    elif 'elnashra' in article_link:
        return True
    elif 'lebanon24' in article_link:
        return True
    elif 'lebanese-forces' in article_link:
        return True
    elif 'aljoumhouria' in article_link:
        return True
    elif 'nna-leb' in article_link:
        return True
    elif 'kataeb' in article_link:
        return True
    elif 'mtv' in article_link:
        return True
    elif 'lbcgroup' in article_link:
        return True
    elif 'sawtbeirut' in article_link:
        return True
    else:
        return False


def mkdir(folder_name):
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)


def scrape_query_search_results():
    all_articles = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.yuRUbf')))
    print(len(all_articles))

    all_titles = []
    for a in all_articles:
        try:
            title = a.find_element_by_css_selector('div.yuRUbf a h3').text
            print(title)
        except:
            title = ''
            print('did not find title')
        all_titles.append(title)

    all_links = []
    for a in all_articles:
        try:
            link = a.find_element_by_css_selector('div.yuRUbf a').get_attribute('href')
            print(link)
        except:
            link = ''
            print('did not find link')
        all_links.append(link)

    for i in itertools.zip_longest(all_titles, all_links):
        print(i)
        print('===================================')

    return all_titles, all_links


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


if __name__ == '__main__':

    include_timeframe = input("Do you have a particular time frame of interest? ")

    if include_timeframe.lower() in ['y', 'yes']:
        time_after = input("Do you want to get articles after certain date: YYYY-MM-DD")
        time_before = input("Do you want to get articles before certain date: YYYY-MM-DD")

        if time_after.strip() == '':
            time_after = None
        if time_before.strip() == '':
            time_before = None
    else:
        time_before, time_after = None, None

    keywords_text = input('Please put any keywords that you want them to appear in text: ')
    keywords_url = input('Please put any keywords that you want them to appear in the url: ')
    keywords_AND = input('Please put any keywords that you want to LOGICALLY combine in an AND: ')
    keywords_OR = input('Please put any keywords that you want to LOGICALLY combine in an OR: ')
    website_url = input('Please enter a website url: ')
    platform = input('Please enter a platform of interest, choose from: [facebook, youtube, instagram]: ')
    choose_entity = input('Do you want to choose a social media account of a particular influencer? please choose: [y, n]: ')
    if choose_entity.lower() == 'y':
        influencer = input('Please enter the name of the influencer: ')
    else:
        influencer = None
    # page_selection = input('Please enter the page numbers of the pages you want to scrape: ')
    num_links = int(input('Please enter the total number of links you want to scrape: '))

    query_keywords_text, query_keywords_url = None, None
    if keywords_text.strip() != '':
        query_keywords_text = keywords_text
    if keywords_url.strip() != '':
        query_keywords_url = keywords_url

    query = ''
    if platform.strip() != '':
        if influencer is None:
            if platform.lower() == 'facebook':
                query += 'site:{} '.format('https://www.facebook.com/')
            elif platform.lower() == 'youtube':
                query += 'site:{} '.format('https://www.youtube.com/')
            elif platform.lower() == 'instagram':
                query += 'site:{} '.format('https://www.youtube.com/')
        else:
            entities2accs = get_accounts_per_entity()
            query += 'site:{}'.format(entities2accs[influencer][platform.lower()])
            # query += 'site:https://www.facebook.com/AlArabiya/ '

    if query_keywords_text is not None:
        query += ' intext:\"{}\" '.format(query_keywords_text) # worked with quotations
    if query_keywords_url is not None:
        query += 'inurl: \"{}\" '.format(query_keywords_url) #

    if time_after is not None:
        query += ' after:{} '.format(time_after)

    if time_before is not None:
        query += ' before:{} '.format(time_before)

    query_keywords_and, query_keywords_or = None, None

    if keywords_AND.strip() != '':
        splitted = keywords_AND.strip().split(' ')
        for i, k in enumerate(splitted):
            if i == 0 and len(splitted) > 1:
                query += "\"" + k + "\" AND "
            elif i == len(splitted)-1:
                query += "\"" + k + "\" "
            else:
                query += "\"" + k + "\" AND "

    if keywords_OR.strip() != '':
        splitted = keywords_OR.strip().split(' ')
        for i, k in enumerate(splitted):
            if i == 0 and len(splitted)>1:
                query += "\"" + k + "\" OR "
            elif i == len(splitted) - 1:
                query += "\" " + k + "\" "
            else:
                query += "\" " + k + "\" OR "

    if website_url.strip() != '':
        query += 'site:{}'.format(website_url)

    driver = webdriver.Chrome('C:\Program Files\chromedriver-win32-119\chromedriver.exe')

    delay = 30 # delay time for WebDriver (in seconds)

    articles = {'title': [], 'link': []}

    news_websites = [
                    'https://www.annahar.com/arabic/section/',
                     'https://bintjbeil.org/',
                     'https://addiyar.com/', #*
                     # 'https://www.yasour.org/2022/ar/',
                     'https://al-akhbar.com/', #*
                     'https://www.tayyar.org/', #*
                     'http://elnashra.com/', #*
                     'http://lebanondebate.com/', #*
                     'https://www.lebanonfiles.com/', #*
                     'http://lebanon24.com/', #*
                     'https://www.lebanese-forces.com/', #*
                     'https://www.aljoumhouria.com/ar/news/', #*
                     'https://www.nna-leb.gov.lb/ar/', #*
                     'https://kataeb.org/', #*
                     'https://www.mtv.com.lb/', #*
                     # 'https://www.aljadeed.tv/',
                     'https://www.lbcgroup.tv/', #*
                     'https://www.sawtbeirut.com/' #*
                     ]


    driver.get('http://www.google.com')
    search = driver.find_element_by_name('q')
    search.send_keys(query)
    search.send_keys(Keys.RETURN)

    SCROLL_PAUSE_TIME = 2  # I'll use this variable for code sleeping time
    delay = 30  # delay time for WebDriver (in seconds)
    scrolling = True  # boolean value -> TRUE means that we're still scrolling, FALSE means we're not scrolling anymore
    last_height = driver.execute_script("return document.documentElement.scrollHeight")  # this is our last/current position on the page
    scrolling_attempt = 5  # we'll have 5 attempts before turning scrolling boolean to False

    video_links, comments_video, posts_links, comments_posts = [], [], [], []

    while scrolling == True:
        htmlelement = driver.find_element_by_tag_name("body")  # locate html tag
        htmlelement.send_keys(Keys.END)

        new_height = driver.execute_script("return document.documentElement.scrollHeight")  # calculate current position
        time.sleep(SCROLL_PAUSE_TIME)  # make pause because scrolling will take 0.5/1 seconds
        driver.implicitly_wait(30)  # make longer pause if loading new comments takes longer

        try:
            article_titles, article_links = scrape_query_search_results()
            articles['title'].extend(article_titles)
            articles['link'].extend(article_links)
        except:
            pass

        try:
            all_spans = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'span')))
            for span in all_spans:
                if span.text == 'More results':
                    driver.execute_script("arguments[0].scrollIntoView();", span)
                    driver.execute_script("arguments[0].click();", span)
                    time.sleep(3)
                    break
        except:
            pass

        if new_height == last_height:  # if current position  is the same as last position, it means we've reached bottom of the page, so we'll break the loop
            scrolling_attempt -= 1
            print(f"scrolling attempt {scrolling_attempt}")
            if (scrolling_attempt == 0):
                scrolling = False  # this will break while loop
        last_height = new_height  # if current position is not the same as last one, we'll set last position as new height


    # links = None
    # attempts = 3
    #
    # len_df_old = 0
    # while True:
    #     try:
    #         print('scrolling ....')
    #         article_titles, article_links = scrape_query_search_results()
    #         articles['title'].extend(article_titles)
    #         articles['link'].extend(article_links)
    #     except:
    #         print("error while trying to load comments")
    #
    #     df = pd.DataFrame(articles)
    #     df = df.drop_duplicates()
    #
    #     if len(df) == len_df_old:
    #         attempts -= 1
    #
    #     len_df_old = len(df)
    #
    #     if len(df) > num_links:
    #         break
    #
    #     if attempts == 0:
    #         break
    #
    #     try:
    #         more_results = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.GNJvt.ipz2Oe span.RVQdVd')))
    #         driver.execute_script("arguments[0].scrollIntoView();", more_results)
    #         driver.execute_script("arguments[0].click();", more_results)
    #         time.sleep(3)
    #     except:
    #         break

    # https://www.annahar.com/

    google_query_dir = 'query_google/'
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

    if keywords_OR.strip() != '':
        if 'https' in keywords_OR:
            keywords_OR = keywords_OR.replace(":", "").replace("/", "").replace(".", "_")
        sub_folder_name += 'keywords_' + 'OR'.join(keywords_OR.split(' ')) + '_'

    if query_keywords_text is not None:
        if 'https' in query_keywords_text or 'http' in query_keywords_text:
            query_keywords_text = query_keywords_text.replace(":", "").replace("/", "").replace(".", "_")
        sub_folder_name += 'intext_' + '_'.join(query_keywords_text.split(' ')) + '_'

    if query_keywords_url is not None:
        if 'https' in query_keywords_url or 'http' in query_keywords_url:
            query_keywords_url = query_keywords_url.replace(":", "").replace("/", "").replace(".", "_")
        sub_folder_name += 'inurl_' + '_'.join(query_keywords_url.split(' ')) + '_'

    if website_url.strip() != '':
        sub_folder_name += 'site_' + website_url.strip().replace(':', '').replace('/', '').replace('.', '') + '/'

    save_dir = os.path.join(google_query_dir, sub_folder_name + "/")
    mkdir(save_dir)

    df = pd.DataFrame(articles)
    df = df.drop_duplicates()
    with open(os.path.join(save_dir, 'links.txt'), 'w') as f:
        for i, row in df.iterrows():
            f.write(row['link'] + '\n')
    f.close()
    df.to_excel(os.path.join(save_dir, 'articles_titles_links.xlsx'), index=False)