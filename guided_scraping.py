import time
import praw
from selenium import webdriver
import datetime
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import pandas as pd
import itertools
import os
import concurrent.futures as futures
import random
import bs4, requests

TWITTER_USERNAME = None
TWITTER_PASSWORD = None
FACEBOOK_USERNAME = None
FACEBOOK_PASSWORD = None
INSTAGRAM_USERNAME = None
INSTAGRAM_PASSWORD = None
TIKTOK_USERNAME = None
TIKTOK_PASSWORD = None

def mkdir(folder):
    if not os.path.exists(folder):
        os.makedirs(folder, exist_ok=True)


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

@timeout(10)
def getting_the_article_bs4(article_link):
    response = requests.get(article_link, headers={'User-Agent': 'Mozilla/5.0'})
    soup = bs4.BeautifulSoup(response.text, features='html.parser')

    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()  # rip it out

    # get text
    text = soup.get_text()

    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)

    print('got body text')
    return text


@timeout(10)
def getting_the_article(article_link):
    ''' function that gets the body of an article given a url that DOES NOT belong to any of the predefined lebanese news websites '''

    driver.get(article_link)
    body_wait = WebDriverWait(driver, delay).until(EC.visibility_of_all_elements_located((By.TAG_NAME, "body")))
    article = body_wait[0].text
    print('got body text')
    return article


def get_article_annahar(article_link):
    driver.get(article_link)
    time.sleep(3)
    try:
        paragraphs = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div#bodyToAddTags div')))
        paragraphs = '\n'.join([p.text for p in paragraphs])
    except:
        paragraphs = ''
    return paragraphs


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
    ''' function that returns the article text of a url that pertains to any pre-defined lebanese news website '''

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
    ''' function that returns a boolean indicating whether the url pertains to any pre-defined lebanese news website '''

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


def get_tweet_replies(tweet_link):
    ''' function that returns the list of replies over a certain tweet given its link '''
    driver.get(tweet_link)
    time.sleep(5)
    SCROLL_PAUSE_TIME = 2  # I'll use this variable for code sleeping time
    scrolling = True  # boolean value -> TRUE means that we're still scrolling, FALSE means we're not scrolling anymore
    last_height = driver.execute_script("return document.documentElement.scrollHeight")  # this is our last/current position on the page
    scrolling_attempt = 2  # we'll have 5 attempts before turning scrolling boolean to False
    post_replies = {'reply_user_name': [], 'reply_user_profile': [], 'reply': []}
    while scrolling == True:
        htmlelement = driver.find_element_by_tag_name("body")  # locate html tag
        htmlelement.send_keys(Keys.END)  # scroll to the bottom of html tag

        try:
            replies = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.css-1dbjc4n.r-1iusvr4.r-16y2uox.r-1777fci.r-kzbkwu')))
            replies_text = [r.text for r in replies]
            for rp in replies_text:
                user_name = rp.split('\n')[0]
                user_profile = 'https://twitter.com/' + rp.split('\n')[1]
                reply = rp.split('\n')[4]

                print(user_name)
                print(user_profile)
                print(reply)
                print('===================================================================')

                post_replies['reply_user_name'].append(user_name)
                post_replies['reply_user_profile'].append(user_profile)
                post_replies['reply'].append(reply)

            print(len(replies))

            # all_replies.extend(replies[-7:])

        except:
            print("Failed loading replies to tweets")

        new_height = driver.execute_script("return document.documentElement.scrollHeight")  # calculate current position
        time.sleep(SCROLL_PAUSE_TIME)  # make pause because scrolling will take 0.5/1 seconds
        driver.implicitly_wait(30)  # make longer pause if loading new comments takes longer

        if new_height == last_height:  # if current position  is the same as last position, it means we've reached bottom of the page, so we'll break the loop
            scrolling_attempt -= 1
            print(f"scrolling attempt {scrolling_attempt}")
            if (scrolling_attempt == 0):
                scrolling = False  # this will break while loop
        last_height = new_height  # if current position is not the same as last one, we'll set last position as new height

    return post_replies


def scrape_twitter_article(tweet_link):
    ''' function that returns the body of the tweet given the tweet link '''
    driver.get(tweet_link)
    driver.implicitly_wait(3)
    article = driver.find_element_by_css_selector('article.css-1dbjc4n.r-18u37iz.r-1ny4l3l.r-1udh08x.r-1qhn6m8.r-i023vh')
    user = article.find_element_by_css_selector('div.css-1dbjc4n.r-1wbh5a2.r-dnmrzs.r-1ny4l3l').text
    text = article.find_element_by_css_selector('div.css-901oao.r-18jsvk2.r-37j5jr.r-1inkyih.r-16dba41.r-135wba7.r-bcqeeo.r-bnwqim.r-qvutc0').text

    print('user: {}'.format(user))
    print('text: {}'.format(text))

    return user, text


def login_tiktok():
    url = "https://www.tiktok.com/login/phone-or-email/email"
    driver.get(url)

    inputs = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'input')))
    print(inputs)
    print(len(inputs))

    if (len(inputs) == 2):
        username = inputs[0]
        username.send_keys(TIKTOK_USERNAME)
        username.send_keys(Keys.ENTER)

        password = inputs[1]
        password.send_keys(TIKTOK_PASSWORD)
        password.send_keys(Keys.ENTER)
    else:
        pass


def login_facebook():
    url = 'https://www.facebook.com/login/'
    driver.get(url)

    # [(i, e) for i,e in enumerate(inputs) if e.get_attribute('name') == 'pass']

    inputs = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'input')))
    username = inputs[13]
    username.send_keys(FACEBOOK_USERNAME)
    # username.send_keys("fatimamarsad@gmail.com")
    # username.send_keys(Keys.ENTER)

    password = inputs[14]
    password.send_keys(FACEBOOK_PASSWORD)
    # password.send_keys("fatimamarsad2023")
    password.send_keys(Keys.ENTER)


def login_twitter():
    ''' function that logs in to twitter using Hiyam's credentials for now '''
    url = "https://twitter.com/i/flow/login"
    driver.get(url)

    inputs = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'input')))
    username = inputs[0]
    # username = WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[autocomplete="username"]')))
    username.send_keys(TWITTER_USERNAME)
    # username.send_keys("fatimamarsad")
    username.send_keys(Keys.ENTER)

    inputs = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'input')))
    password = inputs[1]
    # password = WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[name="password"]')))
    password.send_keys(TWITTER_PASSWORD)
    # password.send_keys("rinro8-fAdbym-recjic")
    password.send_keys(Keys.ENTER)


def scrape_loaded_comments_youtube():
    ''' function that gets current comments fitting in the browser window for a youtube video '''
    loaded_comments = []
    all_comments = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div#body')))
    print(len(all_comments))
    all_usernames = [c.find_element_by_css_selector('div#header-author h3').text for c in all_comments]
    print(len(all_usernames))
    all_times = [c.find_element_by_css_selector('div#header-author yt-formatted-string').text for c in all_comments]
    print(len(all_times))
    all_texts = [c.find_element_by_css_selector('div#comment-content').text for c in all_comments]
    print(len(all_texts))

    try:
        all_usernames = all_usernames[-20:]
        all_times = all_times[-20:]
        all_texts = all_texts[-20:]
    except:
        print("could not get last 20 elements")

    # we'll loop parallel through all usernames and comments
    for (username, timeframe, comment) in zip(all_usernames, all_times, all_texts):
        current_comment = {"username": username, "comment": comment, "time": timeframe}
        print(f"Username : {username}\nTime: {timeframe}\nComment : {comment}")
        loaded_comments.append(current_comment)  # here we'll store comments

    return loaded_comments


def apply_scraping_comments_youtube(video_link):
    ''' function that scrolls over and extracts all comments for a certain youtube video and returns dataframe of comments '''
    driver.get(video_link)

    SCROLL_PAUSE_TIME = 2  # I'll use this variable for code sleeping time
    delay = 30  # delay time for WebDriver (in seconds)
    scrolling = True  # boolean value -> TRUE means that we're still scrolling, FALSE means we're not scrolling anymore
    last_height = driver.execute_script("return document.documentElement.scrollHeight")  # this is our last/current position on the page
    scrolling_attempt = 5  # we'll have 5 attempts before turning scrolling boolean to False

    video_owner = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div#owner')))
    video_owner_txt = [v.text for v in video_owner][0].split('\n')[0]
    print('video owner: {}'.format(video_owner_txt))

    video_title = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div#title')))
    video_title_txt = ' '.join([v.text for v in video_title])

    # video_description = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div#description-inner')))
    video_description = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'span.yt-core-attributed-string--link-inherit-color')))
    video_description_txt = ' '.join([v.text for v in video_description])
    print('video description: {}'.format(video_description_txt))

    # print('Loading comments of the video {}: {}'.format(video_title, video_link))
    all_comments_list = {"username": [], "time": [], "comment": []}
    while scrolling == True:
        htmlelement = driver.find_element_by_tag_name("body")  # locate html tag
        htmlelement.send_keys(Keys.END)

        try:
            last_20_comments = scrape_loaded_comments_youtube()  # calling function to scrape last 20 comments
            all_comments_list["username"].extend([e["username"] for e in last_20_comments])  # appending last 20 comments to the list
            all_comments_list["comment"].extend([e["comment"] for e in last_20_comments])  # appending last 20 comments to the list
            all_comments_list["time"].extend([e["time"] for e in last_20_comments])

        except:
            print("error while trying to load comments")

        new_height = driver.execute_script("return document.documentElement.scrollHeight")  # calculate current position
        time.sleep(SCROLL_PAUSE_TIME)  # make pause because scrolling will take 0.5/1 seconds
        driver.implicitly_wait(30)  # make longer pause if loading new comments takes longer

        if new_height == last_height:  # if current position  is the same as last position, it means we've reached bottom of the page, so we'll break the loop
            scrolling_attempt -= 1
            print(f"scrolling attempt {scrolling_attempt}")
            if (scrolling_attempt == 0):
                scrolling = False  # this will break while loop
        last_height = new_height  # if current position is not the same as last one, we'll set last position as new height

    try:
        buttons = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'ytd-button-renderer#more-replies div.yt-spec-touch-feedback-shape__fill')))
        for btn in buttons:
            driver.execute_script("arguments[0].scrollIntoView();", btn)
            driver.execute_script("arguments[0].click();", btn)
            time.sleep(3)
    except:
        pass
    all_c_r = list(set([e.text for e in WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div#body.style-scope.ytd-comment-renderer')))]))
    for comment_reply in all_c_r:
        all_comments_list["username"].append(comment_reply.split('\n')[0])
        all_comments_list["comment"].append(comment_reply.split('\n')[2])
        all_comments_list["time"].append(comment_reply.split('\n')[1])

    df_comments = pd.DataFrame(all_comments_list)
    df_comments = df_comments.drop_duplicates()
    df_comments['video_owner'] = [video_owner_txt for _ in range(len(df_comments))]
    df_comments['video_title'] = [video_title_txt for _ in range(len(df_comments))]
    df_comments['video_description'] = [video_description_txt for _ in range(len(df_comments))]
    df_comments = df_comments[['video_owner', 'video_title', 'video_description', 'username', 'comment', 'time']]
    return df_comments


def get_reddit_post_comments(post_link):
    ''' function that gets reddit post meta data + comments '''
    post = r.submission(url=post_link)
    date = post.created_utc

    post_info = {}
    post_info['post_id'] = [post.id]
    post_info['post_title'] = [post.title]
    post_info['post_body'] = [post.selftext]
    post_info['post_date'] = [datetime.datetime.fromtimestamp(date)]
    post_info['post_url'] = [post.url]
    post_info['nb_comments'] = [len(post.comments)]
    post_info['subreddit'] = [list(r.info([post.subreddit_id]))[0].display_name]
    post_info['comment_section'] = {'username': [], 'comment': [], 'date': []}

    for comment in post.comments:
        comment_p = comment.body.strip()
        comment_a = comment.author.name if comment.author is not None else 'NA'
        comment_d = comment.created_utc

        post_info['comment_section']['username'].append(comment_a)
        post_info['comment_section']['comment'].append(comment_p)
        post_info['comment_section']['date'].append(datetime.datetime.fromtimestamp(comment_d))
    return post_info


def scrape_post_facebook(post_link):
    ''' function that scrapes the post of a facebook article '''
    driver.get(post_link)
    try:
        inputs = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'input')))
        username = inputs[17]
        username.send_keys("loulou1997.g@hotmail.com")
        # username.send_keys(Keys.ENTER)

        password = inputs[18]
        password.send_keys("Hiyam1997")
        password.send_keys(Keys.ENTER)
    except:
        pass

    try:
        article = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.x1iorvi4.x1pi30zi.x1l90r2v.x1swvt13'))).text
    except:
        print('could not load article')
        article = ''
    return article


def scrape_facebook_post_owner(post_link):
    driver.get(post_link)
    try:
        post_owner = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'strong')))[0].text
    except:
        print('could not load post owner ...')
        post_owner = ''
    return post_owner


def scrape_likes_facebook(post_link):
    ''' function that gets the number of reactions on a facebook post '''
    try:
        driver.get(post_link)
        time.sleep(2)
        reactions = [d.text for d in WebDriverWait(driver, 3).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.x78zum5.x1iyjqo2 div.x6s0dn4.xi81zsa.x78zum5.x1a02dak.x13a6bvl.xyesn5m.x6ikm8r.x10wlt62')))][0].split('\n')[0]
        return reactions
    except:
        return '-'

def scrape_comments_facebook_post(post_link):
    ''' scrapes comments for a facebook POST not a facebook VIDEO/WATCH '''

    # if '&ref=sharing' not in post_link:
    #     post_link = post_link + '&ref=sharing'
    #     print(post_link)

    driver.get(post_link)
    all_comments = []

    # time.sleep(3)
    #
    # if '&ref=sharing' in driver.current_url:
    #     url = driver.current_url.replace('&ref=sharing', '')
    #     driver.get(url)
    #     time.sleep(2)

    SCROLL_PAUSE_TIME = 2  # I'll use this variable for code sleeping time
    delay = 5  # delay time for WebDriver (in seconds)
    scrolling = True  # boolean value -> TRUE means that we're still scrolling, FALSE means we're not scrolling anymore
    last_height = driver.execute_script(
        "return document.documentElement.scrollHeight")  # this is our last/current position on the page
    scrolling_attempt = 3  # we'll have 5 attempts before turning scrolling boolean to False

    # new by Hiyam
    try:
        see_all_comments = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,'span.x193iq5w.xeuugli.x13faqbe.x1vvkbs.x1xmvt09.x1lliihq.x1s928wv.xhkezso.x1gmr53x.x1cpjm7i.x1fgarty.x1943h6x.xudqn12.x3x7a5m.x6prxxf.xvq8zen.xo1l8bm.x1fey0fg')))
        driver.execute_script("arguments[0].click();", see_all_comments[0])
    except:
        pass
    ##########

    while scrolling == True:
        htmlelement = driver.find_element_by_tag_name("body")  # locate html tag
        htmlelement.send_keys(Keys.END)  # scroll to the bottom of html tag

        comments_btn = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.x9f619.x1n2onr6.x1ja2u2z.x6s0dn4.x3nfvp2.xxymvpz i')))[0]
        driver.execute_script("arguments[0].click();", comments_btn)

        all_comments_btn = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,
                                                                                                   'div.x1i10hfl.xjbqb8w.x6umtig.x1b1mbwd.xaqea5y.xav7gou.xe8uvvx.x1hl2dhg.xggy1nq.x1o1ewxj.x3x9cwd.x1e5q0jg.x13rtm0m.x87ps6o.x1lku1pv.x1a2a7pz.xjyslct.x9f619.x1ypdohk.x78zum5.x1q0g3np.x2lah0s.xnqzcj9.x1gh759c.xdj266r.xat24cr.x1344otq.x1de53dj.xz9dl7a.xsag5q8.x1n2onr6.x16tdsg8.x1ja2u2z.x6s0dn4')))[
            2]
        driver.execute_script("arguments[0].click();", all_comments_btn)

        len_all_comments_old = 0
        while True:

            try:
                # view_more_comments = driver.find_element_by_xpath('//*[@id="mount_0_0_8n"]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div/div/div/div/div/div/div/div/div/div/div/div/div[2]/div/div/div[4]/div/div/div[2]/div[4]/div/div[2]/span/span[contains(., "more comments")]')
                # view_more_comments = driver.find_element_by_xpath('//*[@id="watch_feed"]/div/div[1]/div/div/div[2]/div[3]/div[1]/div[2]/div/div[1]/div[2]/span/span[contains(., "more comments")]')
                view_more_comments = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((
                                                                                                            By.CSS_SELECTOR,
                                                                                                            'span.x193iq5w.xeuugli.x13faqbe.x1vvkbs.x1xmvt09.x1lliihq.x1s928wv.xhkezso.x1gmr53x.x1cpjm7i.x1fgarty.x1943h6x.xudqn12.x3x7a5m.x6prxxf.xvq8zen.x1s688f.xi81zsa')))
                for b in view_more_comments:
                    if 'View' in b.text and 'more comments' in b.text:
                        # print('View more comments text: '.format(view_more_comments.text))
                        # if view_more_comments.text == 'Write a comment':
                        #     scrolling_attempt -= 1

                        driver.execute_script("arguments[0].scrollIntoView();", b)
                        driver.execute_script("arguments[0].click();", b)
                # print('View more comments text: '.format(view_more_comments.text))
                # if view_more_comments.text == 'Write a comment':
                #     scrolling_attempt -= 1
                #
                # driver.execute_script("arguments[0].scrollIntoView();", view_more_comments)
                # driver.execute_script("arguments[0].click();", view_more_comments)
                # driver.execute_script("arguments[0].scrollIntoView();", view_more_comments)

                # check for replies
                try:
                    view_replies = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((
                                                                                                          By.CSS_SELECTOR,
                                                                                                          'span.x193iq5w.xeuugli.x13faqbe.x1vvkbs.x1xmvt09.x1lliihq.x1s928wv.xhkezso.x1gmr53x.x1cpjm7i.x1fgarty.x1943h6x.xudqn12.x3x7a5m.x6prxxf.xvq8zen.x1s688f.xi81zsa')))
                    for repl in view_replies:
                        if 'replies' in repl.text or 'reply' in repl.text:
                            driver.execute_script("arguments[0].click();", repl)
                except:
                    pass

                comments = WebDriverWait(driver, delay).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.xv55zj0.x1vvkbs.x1rg5ohu.xxymvpz')))
                try:
                    btn__with_see_more = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((
                                                                                                                By.CSS_SELECTOR,
                                                                                                                'div.xv55zj0.x1vvkbs.x1rg5ohu.xxymvpz > * div.x1i10hfl.xjbqb8w.x6umtig.x1b1mbwd.xaqea5y.xav7gou.x9f619.x1ypdohk.xt0psk2.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x16tdsg8.x1hl2dhg.xggy1nq.x1a2a7pz.xt0b8zv.xzsf02u.x1s688f')))
                    for btn in btn__with_see_more:
                        driver.execute_script("arguments[0].click();", btn)
                        time.sleep(1)
                    # get comments again
                    comments = WebDriverWait(driver, delay).until(
                        EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.xv55zj0.x1vvkbs.x1rg5ohu.xxymvpz')))

                except:
                    pass
                comments_text = [c.text for c in comments]
                all_comments.extend(comments_text)
                if len(set(all_comments)) == len_all_comments_old:
                    scrolling_attempt -= 1
                len_all_comments_old = len(set(all_comments))
                for c in comments_text:
                    print(c)
            except:
                comments = WebDriverWait(driver, delay).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.xv55zj0.x1vvkbs.x1rg5ohu.xxymvpz')))
                comments_text = [c.text for c in comments]
                all_comments.extend(comments_text)

                if len(set(all_comments)) == len_all_comments_old:
                    scrolling_attempt -= 1
                len_all_comments_old = len(set(all_comments))

                for c in comments_text:
                    print(c)
                scrolling_attempt -= 1
                if scrolling_attempt < 0:
                    scrolling = False
                    break

            if scrolling_attempt <= 0:
                scrolling = False
                break

        if (scrolling_attempt <= 0):
            scrolling = False  # this will break while loop

        new_height = driver.execute_script("return document.documentElement.scrollHeight")  # calculate current position
        time.sleep(SCROLL_PAUSE_TIME)  # make pause because scrolling will take 0.5/1 seconds
        driver.implicitly_wait(30)  # make longer pause if loading new comments takes longer

        if new_height == last_height:  # if current position  is the same as last position, it means we've reached bottom of the page, so we'll break the loop
            scrolling_attempt -= 1
            print(f"scrolling attempt {scrolling_attempt}")
            if (scrolling_attempt <= 0):
                scrolling = False  # this will break while loop
        last_height = new_height  # if current position is not the same as last one, we'll set last position as new height

        print('scrolling attempt: {}'.format(scrolling_attempt))
    return [c for c in all_comments if 'See more' not in c]

    # driver.get(post_link)
    # time.sleep(5)
    # all_comments = []
    #
    # SCROLL_PAUSE_TIME = 2  # I'll use this variable for code sleeping time
    # delay = 5  # delay time for WebDriver (in seconds)
    # scrolling = True  # boolean value -> TRUE means that we're still scrolling, FALSE means we're not scrolling anymore
    # last_height = driver.execute_script("return document.documentElement.scrollHeight")  # this is our last/current position on the page
    # scrolling_attempt = 3  # we'll have 5 attempts before turning scrolling boolean to False
    #
    # while scrolling == True:
    #     htmlelement = driver.find_element_by_tag_name("body")  # locate html tag
    #     htmlelement.send_keys(Keys.END)  # scroll to the bottom of html tag
    #
    #     comments_btn = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.x9f619.x1n2onr6.x1ja2u2z.x6s0dn4.x3nfvp2.xxymvpz i')))[0]
    #     driver.execute_script("arguments[0].click();", comments_btn)
    #
    #     all_comments_btn = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.x1i10hfl.xjbqb8w.x6umtig.x1b1mbwd.xaqea5y.xav7gou.xe8uvvx.x1hl2dhg.xggy1nq.x1o1ewxj.x3x9cwd.x1e5q0jg.x13rtm0m.x87ps6o.x1lku1pv.x1a2a7pz.xjyslct.x9f619.x1ypdohk.x78zum5.x1q0g3np.x2lah0s.xnqzcj9.x1gh759c.xdj266r.xat24cr.x1344otq.x1de53dj.xz9dl7a.xsag5q8.x1n2onr6.x16tdsg8.x1ja2u2z.x6s0dn4')))[2]
    #     driver.execute_script("arguments[0].click();", all_comments_btn)
    #
    #     len_all_comments_old = 0
    #     while True:
    #
    #         try:
    #             # view_more_comments = driver.find_element_by_xpath('//*[@id="mount_0_0_8n"]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div/div/div/div/div/div/div/div/div/div/div/div/div[2]/div/div/div[4]/div/div/div[2]/div[4]/div/div[2]/span/span[contains(., "more comments")]')
    #             # view_more_comments = driver.find_element_by_xpath('//*[@id="watch_feed"]/div/div[1]/div/div/div[2]/div[3]/div[1]/div[2]/div/div[1]/div[2]/span/span[contains(., "more comments")]')
    #             view_more_comments = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'span.x193iq5w.xeuugli.x13faqbe.x1vvkbs.x1xmvt09.x1lliihq.x1s928wv.xhkezso.x1gmr53x.x1cpjm7i.x1fgarty.x1943h6x.xudqn12.x3x7a5m.x6prxxf.xvq8zen.x1s688f.xi81zsa')))[5]
    #             print('View more comments text: '.format(view_more_comments.text))
    #             if view_more_comments.text == 'Write a comment':
    #                 scrolling_attempt -= 1
    #
    #             driver.execute_script("arguments[0].scrollIntoView();", view_more_comments)
    #             driver.execute_script("arguments[0].click();", view_more_comments)
    #             # driver.execute_script("arguments[0].scrollIntoView();", view_more_comments)
    #
    #             comments = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.xv55zj0.x1vvkbs.x1rg5ohu.xxymvpz')))
    #             try:
    #                 btn__with_see_more = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.xv55zj0.x1vvkbs.x1rg5ohu.xxymvpz > * div.x1i10hfl.xjbqb8w.x6umtig.x1b1mbwd.xaqea5y.xav7gou.x9f619.x1ypdohk.xt0psk2.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x16tdsg8.x1hl2dhg.xggy1nq.x1a2a7pz.xt0b8zv.xzsf02u.x1s688f')))
    #                 for btn in btn__with_see_more:
    #                     driver.execute_script("arguments[0].click();", btn)
    #                     time.sleep(1)
    #                 # get comments again
    #                 comments = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.xv55zj0.x1vvkbs.x1rg5ohu.xxymvpz')))
    #
    #             except:
    #                 pass
    #             comments_text = [c.text for c in comments]
    #             all_comments.extend(comments_text)
    #             if len(set(all_comments)) == len_all_comments_old:
    #                 scrolling_attempt -= 1
    #             len_all_comments_old = len(set(all_comments))
    #             for c in comments_text:
    #                 print(c)
    #         except:
    #             comments = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.xv55zj0.x1vvkbs.x1rg5ohu.xxymvpz')))
    #             comments_text = [c.text for c in comments]
    #             all_comments.extend(comments_text)
    #
    #             if len(set(all_comments)) == len_all_comments_old:
    #                 scrolling_attempt -= 1
    #             len_all_comments_old = len(set(all_comments))
    #
    #             for c in comments_text:
    #                 print(c)
    #             scrolling_attempt -= 1
    #             if scrolling_attempt < 0:
    #                 scrolling = False
    #                 break
    #
    #         if scrolling_attempt <= 0:
    #             scrolling = False
    #             break
    #
    #     if (scrolling_attempt <= 0):
    #         scrolling = False  # this will break while loop
    #
    #     new_height = driver.execute_script("return document.documentElement.scrollHeight")  # calculate current position
    #     time.sleep(SCROLL_PAUSE_TIME)  # make pause because scrolling will take 0.5/1 seconds
    #     driver.implicitly_wait(30)  # make longer pause if loading new comments takes longer
    #
    #     if new_height == last_height:  # if current position  is the same as last position, it means we've reached bottom of the page, so we'll break the loop
    #         scrolling_attempt -= 1
    #         print(f"scrolling attempt {scrolling_attempt}")
    #         if (scrolling_attempt <= 0):
    #             scrolling = False  # this will break while loop
    #     last_height = new_height  # if current position is not the same as last one, we'll set last position as new height
    #
    #     print('scrolling attempt: {}'.format(scrolling_attempt))
    # return [c for c in all_comments if 'See more' not in c]


def scrape_comments_facebook(post_link):
    ''' function that scrapes the comments of a facebook article '''
    # if '&ref=sharing' not in post_link:
    #     post_link = post_link + '&ref=sharing'
    #     print(post_link)

    # if '&ref=sharing' not in post_link:
    #     post_link = post_link + '&ref=sharing'
    #     print(post_link)

    if 'm.facebook' in post_link:
        post_link = post_link.replace('m.facebook.com', 'facebook.com')
    driver.get(post_link)
    all_comments = []

    SCROLL_PAUSE_TIME = 2  # I'll use this variable for code sleeping time
    delay = 30  # delay time for WebDriver (in seconds)
    scrolling = True  # boolean value -> TRUE means that we're still scrolling, FALSE means we're not scrolling anymore
    last_height = driver.execute_script("return document.documentElement.scrollHeight")  # this is our last/current position on the page
    scrolling_attempt = 2  # we'll have 5 attempts before turning scrolling boolean to False
    len_old = 0
    while scrolling == True:
        htmlelement = driver.find_element_by_tag_name("body")  # locate html tag
        htmlelement.send_keys(Keys.END)  # scroll to the bottom of html tag

        try:
            comments_btn = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.x9f619.x1n2onr6.x1ja2u2z.x6s0dn4.x3nfvp2.xxymvpz i')))[0]
            # driver.execute_script("arguments[0].scrollIntoView();", comments_btn)
            driver.execute_script("arguments[0].click();", comments_btn)

            all_comments_btn = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.xu06os2.x1ok221b span.x193iq5w.xeuugli.x13faqbe.x1vvkbs.x1xmvt09.x1lliihq.x1s928wv.xhkezso.x1gmr53x.x1cpjm7i.x1fgarty.x1943h6x.x4zkp8e.x676frb.x1pg5gke.xvq8zen.xo1l8bm.xi81zsa.x1yc453h')))[2]
            # all_comments_btn = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="mount_0_0_1g"]/div/div[1]/div/div[3]/div/div/div/div[2]/div/div/div[1]/div[1]/div/div/div/div/div/div/div[1]/div/div[3]/div[1]/div/div[2]/span')))
            # all_comments_btn = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="mount_0_0_1g"]/div/div[1]/div/div[3]/div/div/div/div[2]/div/div/div[1]/div[1]/div/div')))[0].find_elements_by_tag_name('span')[5]
            driver.execute_script("arguments[0].click();", all_comments_btn)
        except:
            pass

        # comments_section = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.x1n2onr6.x1vjfegm.x1iyjqo2.x1odjw0f ul')))
        while True:
            try:
                try:
                    # view_more_comments = driver.find_element_by_xpath('//*[@id="watch_feed"]/div/div[1]/div/div/div[2]/div[3]/div[1]/div[2]/div/div[1]/div[2]/span/span[contains(., "more comments")]')
                    view_more_comments = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'span.x193iq5w.xeuugli.x13faqbe.x1vvkbs.x1xmvt09.x1lliihq.x1s928wv.xhkezso.x1gmr53x.x1cpjm7i.x1fgarty.x1943h6x.xudqn12.x3x7a5m.x6prxxf.xvq8zen.x1s688f.xi81zsa')))
                    for b in view_more_comments:
                        if 'View' in b.text and 'more comments' in b.text:
                            driver.execute_script("arguments[0].click();", b)
                            driver.execute_script("arguments[0].scrollIntoView();", b)
                            time.sleep(1)
                except:
                    pass

                try:
                    replies = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'span.x193iq5w.xeuugli.x13faqbe.x1vvkbs.x1xmvt09.x1lliihq.x1s928wv.xhkezso.x1gmr53x.x1cpjm7i.x1fgarty.x1943h6x.xudqn12.x3x7a5m.x6prxxf.xvq8zen.x1s688f.xi81zsa')))
                    for repl in replies:
                        if 'replies' in repl.text or '1 reply' in repl.text:
                            driver.execute_script("arguments[0].click();", repl)
                except:
                    pass

                try:
                    see_more = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.x1i10hfl.xjbqb8w.x6umtig.x1b1mbwd.xaqea5y.xav7gou.x9f619.x1ypdohk.xt0psk2.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x16tdsg8.x1hl2dhg.xggy1nq.x1a2a7pz.xt0b8zv.xzsf02u.x1s688f')))
                    for s in see_more:
                        if 'See more' in s.text:
                            driver.execute_script("arguments[0].click();", s)
                except:
                    pass

                comments = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.x1y1aw1k.xn6708d.xwib8y2.x1ye3gou')))
                comments_text = [c.text for c in comments]
                all_comments.extend(comments_text)
                for c in comments_text:
                    print(c)

                if len_old == len(set(comments_text)):
                    scrolling_attempt -= 1
                else:
                    len_old = len(set(comments_text))

                if scrolling_attempt < 0:
                    break

            except:
                comments = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.x1y1aw1k.xn6708d.xwib8y2.x1ye3gou')))
                comments_text = [c.text for c in comments]
                all_comments.extend(comments_text)
                for c in comments_text:
                    print(c)
                scrolling_attempt -= 1
                if scrolling_attempt < 0:
                    break

            # if len(set(all_comments)) >= 500:
            #     break

                # break
                # if scrolling_attempt < 0:
                #     break
                # scrolling = False
                # break

        if (scrolling_attempt <= 0):
            scrolling = False  # this will break while loop

        new_height = driver.execute_script("return document.documentElement.scrollHeight")  # calculate current position
        time.sleep(SCROLL_PAUSE_TIME)  # make pause because scrolling will take 0.5/1 seconds
        driver.implicitly_wait(30)  # make longer pause if loading new comments takes longer

        if new_height == last_height:  # if current position  is the same as last position, it means we've reached bottom of the page, so we'll break the loop
            scrolling_attempt -= 1
            print(f"scrolling attempt {scrolling_attempt}")
            if (scrolling_attempt <= 0):
                scrolling = False  # this will break while loop
        last_height = new_height  # if current position is not the same as last one, we'll set last position as new height

    return all_comments

    # if '&ref=sharing' not in post_link:
    #     post_link = post_link + '&ref=sharing'
    #     print(post_link)
    # driver.get(post_link)
    # all_comments = []
    #
    # SCROLL_PAUSE_TIME = 2  # I'll use this variable for code sleeping time
    # delay = 30  # delay time for WebDriver (in seconds)
    # scrolling = True  # boolean value -> TRUE means that we're still scrolling, FALSE means we're not scrolling anymore
    # last_height = driver.execute_script("return document.documentElement.scrollHeight")  # this is our last/current position on the page
    # scrolling_attempt = 2  # we'll have 5 attempts before turning scrolling boolean to False
    #
    # while scrolling == True:
    #     htmlelement = driver.find_element_by_tag_name("body")  # locate html tag
    #     htmlelement.send_keys(Keys.END)  # scroll to the bottom of html tag
    #
    #     comments_btn = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located(
    #         (By.CSS_SELECTOR, 'div.x9f619.x1n2onr6.x1ja2u2z.x6s0dn4.x3nfvp2.xxymvpz i')))[0]
    #     # driver.execute_script("arguments[0].scrollIntoView();", comments_btn)
    #     driver.execute_script("arguments[0].click();", comments_btn)
    #
    #     all_comments_btn = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.xu06os2.x1ok221b span.x193iq5w.xeuugli.x13faqbe.x1vvkbs.x1xmvt09.x1lliihq.x1s928wv.xhkezso.x1gmr53x.x1cpjm7i.x1fgarty.x1943h6x.x4zkp8e.x676frb.x1pg5gke.xvq8zen.xo1l8bm.xi81zsa.x1yc453h')))[2]
    #     # all_comments_btn = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="mount_0_0_1g"]/div/div[1]/div/div[3]/div/div/div/div[2]/div/div/div[1]/div[1]/div/div/div/div/div/div/div[1]/div/div[3]/div[1]/div/div[2]/span')))
    #     # all_comments_btn = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="mount_0_0_1g"]/div/div[1]/div/div[3]/div/div/div/div[2]/div/div/div[1]/div[1]/div/div')))[0].find_elements_by_tag_name('span')[5]
    #     driver.execute_script("arguments[0].click();", all_comments_btn)
    #
    #     # comments_section = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.x1n2onr6.x1vjfegm.x1iyjqo2.x1odjw0f ul')))
    #     while True:
    #         try:
    #             view_more_comments = driver.find_element_by_xpath('//*[@id="watch_feed"]/div/div[1]/div/div/div[2]/div[3]/div[1]/div[2]/div/div[1]/div[2]/span/span[contains(., "more comments")]')
    #             driver.execute_script("arguments[0].click();", view_more_comments)
    #             driver.execute_script("arguments[0].scrollIntoView();", view_more_comments)
    #
    #             comments = WebDriverWait(driver, delay).until(
    #                 EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.x1y1aw1k.xn6708d.xwib8y2.x1ye3gou')))
    #             comments_text = [c.text for c in comments]
    #             all_comments.extend(comments_text)
    #             for c in comments_text:
    #                 print(c)
    #         except:
    #             comments = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.x1y1aw1k.xn6708d.xwib8y2.x1ye3gou')))
    #             comments_text = [c.text for c in comments]
    #             all_comments.extend(comments_text)
    #             for c in comments_text:
    #                 print(c)
    #             scrolling_attempt -= 1
    #             if scrolling_attempt < 0:
    #                 break
    #
    #         if len(set(all_comments)) >= 500:
    #             break
    #             # break
    #             # if scrolling_attempt < 0:
    #             #     break
    #             # scrolling = False
    #             # break
    #
    #     if (scrolling_attempt <= 0):
    #         scrolling = False  # this will break while loop
    #
    #     new_height = driver.execute_script("return document.documentElement.scrollHeight")  # calculate current position
    #     time.sleep(SCROLL_PAUSE_TIME)  # make pause because scrolling will take 0.5/1 seconds
    #     driver.implicitly_wait(30)  # make longer pause if loading new comments takes longer
    #
    #     if new_height == last_height:  # if current position  is the same as last position, it means we've reached bottom of the page, so we'll break the loop
    #         scrolling_attempt -= 1
    #         print(f"scrolling attempt {scrolling_attempt}")
    #         if (scrolling_attempt <= 0):
    #             scrolling = False  # this will break while loop
    #     last_height = new_height  # if current position is not the same as last one, we'll set last position as new height
    #
    # return all_comments


def login_instagram():
    url = "https://www.instagram.com/accounts/login/"
    driver.get(url)
    time.sleep(3)

    username = WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[name="username"]')))
    username.send_keys(INSTAGRAM_USERNAME)
    # username.send_keys("fatimamarsad@gmail.com")
    username.send_keys(Keys.ENTER)

    password = WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[name="password"]')))
    password.send_keys(INSTAGRAM_PASSWORD)
    # password.send_keys("fatimamarsad2023!")
    password.send_keys(Keys.ENTER)


def login_instagram_colab():
    url = "https://www.instagram.com/accounts/login/"
    driver.get(url)

    inputs = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'input')))
    print(inputs)
    print(len(inputs))

    if (len(inputs) == 2):
        username = inputs[0]
        username.send_keys("fatimamarsad@gmail.com")
        username.send_keys(Keys.ENTER)

        password = inputs[1]
        password.send_keys("fatimamarsad2023!")
        password.send_keys(Keys.ENTER)
    else:
        pass


# def scrape_loaded_comments_instagram(driver, delay, get_meta_data=True):
#     all_comments = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'ul._a9ym')))
#     all_texts = [c.text for c in all_comments]
#
#     if get_meta_data:
#         description = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.x1qjc9v5.x972fbf.xcfux6l.x1qhh985.xm0m39n.x9f619.x78zum5.xdt5ytf.x2lah0s.xk390pu.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x1n2onr6.xggy1nq.x11njtxf')))[1]
#         description_txt = [d for d in description.text.split('\n')]
#         channel_name = description_txt[0]
#         description_txt_actual = ' '.join(description_txt[1:])
#         post_time = description.find_element(By.CSS_SELECTOR, 'time').get_attribute('datetime')
#
#     usernames = [c.split('\n')[0] for c in all_texts]
#     comments = [c.split('\n')[1] for c in all_texts]
#     times = [c.find_element(By.CSS_SELECTOR, 'time._a9ze._a9zf').get_attribute('datetime') for c in all_comments]
#
#     loaded_comments = {}
#     loaded_comments['username'] = usernames
#     loaded_comments['comment'] = comments
#     loaded_comments['time'] = times
#
#     if get_meta_data:
#         return channel_name, description_txt_actual, post_time, loaded_comments
#     else:
#         return loaded_comments
#
#
# def apply_scraping_comments_instagram(video_link):
#     login_instagram()
#     time.sleep(random.randint(5, 10))
#     driver.get(video_link)
#
#     delay = 30  # delay time for WebDriver (in seconds)
#     print('Loading comments of the video: {}'.format(video_link))
#     all_comments_list = {"username": [], "time": [], "comment": []}
#     count = 0
#     attempts = 5
#     len_old = 0
#     channel_name, description, post_time = None, None, None
#     while True:
#         htmlelement = driver.find_element(By.TAG_NAME, "body")  # locate html tag
#         htmlelement.send_keys(Keys.END)
#
#         try:
#             btn = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'button._abl-')))
#             try:
#                 btn[0].click()
#             except:
#                 pass
#             count += 1
#             print(count)
#
#             try:
#                 btn_close = WebDriverWait(driver, 2).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'svg[aria-label="Close"]')))
#                 btn_close.close()
#             except:
#                 pass
#
#             try:
#                 btn_view_hidden = WebDriverWait(driver, 2).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'svg[aria-label="View hidden comments"]')))
#                 btn_view_hidden.click()
#             except:
#                 pass
#
#             if count%5 == 0:
#                 if count == 5:
#                     channel_name, description, post_time, last_20_comments = scrape_loaded_comments_instagram(driver=driver, delay=delay)  # calling function to scrape last 20 comments
#                 else:
#                     last_20_comments = scrape_loaded_comments_instagram(driver=driver, delay=delay, get_meta_data=False)  # calling function to scrape last 20 comments
#
#                 print(last_20_comments)
#                 print(len(last_20_comments['username']))
#
#                 if len(last_20_comments) == len_old:
#                     attempts -= 1
#                     print('attempts = {}'.format(attempts))
#                 else:
#                     len_old = len(last_20_comments)
#
#                 all_comments_list["username"].extend(last_20_comments["username"])
#                 all_comments_list["comment"].extend(last_20_comments["comment"])
#                 all_comments_list["time"].extend(last_20_comments["time"])
#
#             if attempts == 0:
#                 return channel_name, description, post_time, all_comments_list
#
#         except:
#             print("error while trying to load comments")
#             if channel_name is None:
#                 channel_name, description, post_time, last_20_comments = scrape_loaded_comments_instagram(driver=driver, delay=delay)  # calling function to scrape last 20 comments
#             else:
#                 last_20_comments = scrape_loaded_comments_instagram(driver=driver, delay=delay)
#             print(last_20_comments)
#             print(len(last_20_comments))
#
#             all_comments_list["username"].extend(last_20_comments["username"])
#             all_comments_list["comment"].extend(last_20_comments["comment"])
#             all_comments_list["time"].extend(last_20_comments["time"])
#             return channel_name, description, post_time, all_comments_list


# def apply_scraping_comments_instagram(video_link):
#     login_instagram()
#     time.sleep(random.randint(5, 10))
#     driver.get(video_link)
#
#     delay = 30  # delay time for WebDriver (in seconds)
#     print('Loading comments of the video: {}'.format(video_link))
#     all_comments_list = {"username": [], "time": [], "comment": []}
#     count = 0
#     attempts = 3
#     len_old = 0
#     channel_name, description, post_time = None, None, None
#     while True:
#         htmlelement = driver.find_element_by_tag_name("body")  # locate html tag
#         htmlelement.send_keys(Keys.END)
#
#         try:
#             # btn = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'button._abl-')))
#             # try:
#             #     btn[0].click()
#             # except:
#             #     pass
#             # //*[@id="mount_0_0_es"]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div/div[2]/div/div[2]/div/div/ul/li/div
#             btn = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'button._abl-')))
#             driver.execute_script("arguments[0].click();", btn[0])
#             count += 1
#             print(count)
#
#             try:
#                 btn_close = WebDriverWait(driver, 2).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'svg[aria-label="Close"]')))
#                 # btn_close.close()
#                 driver.execute_script("arguments[0].close();", btn_close)
#             except:
#                 pass
#
#             try:
#                 # btn_view_hidden = WebDriverWait(driver, 2).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'svg[aria-label="View hidden comments"]')))
#                 # btn_view_hidden = WebDriverWait(driver, 2).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'span[contains(., "View hidden comments")]')))[0]
#                 # btn_view_hidden.click()
#                 # btn_view_hidden =  WebDriverWait(driver, 2).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="mount_0_0_i3"]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div/div[2]/div/div[2]/div/div/ul/div[2]/div/div')))[0]
#                 # driver.execute_script("arguments[0].scrollIntoView();", comments_btn)
#                 all_spans = WebDriverWait(driver, 2).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'span')))
#                 for s in all_spans:
#                     if 'View hidden comments' in s.text:
#                         btn_view_hidden = s
#                         driver.execute_script("arguments[0].click();", btn_view_hidden)
#                         break
#
#             #     //*[@id="mount_0_0_i3"]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div/div[2]/div/div[2]/div/div/ul/div[2]/div/div
#             except:
#                 pass
#
#             if count%5 == 0:
#                 if count == 5:
#                     channel_name, description, post_time, last_20_comments = scrape_loaded_comments_instagram(driver=driver, delay=delay)  # calling function to scrape last 20 comments
#                 else:
#                     last_20_comments = scrape_loaded_comments_instagram(driver=driver, delay=delay, get_meta_data=False)  # calling function to scrape last 20 comments
#
#                 print(last_20_comments)
#                 print(len(last_20_comments['username']))
#
#                 if len(last_20_comments) == len_old:
#                     attempts -= 1
#                     print('attempts = {}'.format(attempts))
#                 else:
#                     len_old = len(last_20_comments)
#
#                 all_comments_list["username"].extend(last_20_comments["username"])
#                 all_comments_list["comment"].extend(last_20_comments["comment"])
#                 all_comments_list["time"].extend(last_20_comments["time"])
#
#             if attempts == 0:
#                 return channel_name, description, post_time, all_comments_list
#
#         except:
#             print("error while trying to load comments")
#             if channel_name is None:
#                 channel_name, description, post_time, last_20_comments = scrape_loaded_comments_instagram(driver=driver, delay=delay)  # calling function to scrape last 20 comments
#             else:
#                 last_20_comments = scrape_loaded_comments_instagram(driver=driver, delay=delay)
#             print(last_20_comments)
#             print(len(last_20_comments))
#
#             all_comments_list["username"].extend(last_20_comments["username"])
#             all_comments_list["comment"].extend(last_20_comments["comment"])
#             all_comments_list["time"].extend(last_20_comments["time"])
#             return channel_name, description, post_time, all_comments_list


def scrape_loaded_comments_instagram(driver, delay, get_meta_data=True):
    # all_comments_ACTUAL = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.x9f619.xjbqb8w.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.x1uhb9sk.x1plvlek.xryxfnj.x1c4vz4f.x2lah0s.xdt5ytf.xqjyukv.x1qjc9v5.x1oa3qoh.x1nhvcw1')))
    # all_comments_orig = [c.text for c in WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.x9f619.xjbqb8w.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.x1uhb9sk.x1plvlek.xryxfnj.x1c4vz4f.x2lah0s.xdt5ytf.xqjyukv.x1qjc9v5.x1oa3qoh.x1nhvcw1 span.x1lliihq.x1plvlek.xryxfnj.x1n2onr6.x193iq5w.xeuugli.x1fj9vlw.x13faqbe.x1vvkbs.x1s928wv.xhkezso.x1gmr53x.x1cpjm7i.x1fgarty.x1943h6x.x1i0vuye.xvs91rp.xo1l8bm.x5n08af.x10wh9bi.x1wdrske.x8viiok.x18hxmgj')))]
    # i = 1
    # all_comments = []
    # while i < len(all_comments_orig):
    #     all_comments.append(all_comments_orig[i-1]+'\n'+all_comments_orig[i])
    #     i += 2
    # all_texts = all_comments

    all_text = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.x9f619.xjbqb8w.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.x1uhb9sk.x1plvlek.xryxfnj.x1iyjqo2.x2lwn1j.xeuugli.xdt5ytf.xqjyukv.x1qjc9v5.x1oa3qoh.x1nhvcw1')))
    usernames = [c.text.split('\n')[0] for c in all_text]
    comments = [' '.join(c.text.split('\n')[1:]) for c in all_text]
    times_final = []
    for c in all_text:
        try:
            times_final.append(c.find_element_by_css_selector('time').get_attribute('datetime'))
        except:
            times_final.append('')
    # times_final = [c.find_element_by_css_selector('time').get_attribute('datetime') for c in all_text]

    # [c.text for c in WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.x9f619.xjbqb8w.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.x1uhb9sk.x1plvlek.xryxfnj.x1iyjqo2.x2lwn1j.xeuugli.xdt5ytf.xqjyukv.x1qjc9v5.x1oa3qoh.x1nhvcw1')))]
    # [c.find_element_by_css_selector('time').get_attribute('datetime') for c in WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.x9f619.xjbqb8w.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.x1uhb9sk.x1plvlek.xryxfnj.x1iyjqo2.x2lwn1j.xeuugli.xdt5ytf.xqjyukv.x1qjc9v5.x1oa3qoh.x1nhvcw1')))]


    if get_meta_data:
        # description = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.x1qjc9v5.x972fbf.xcfux6l.x1qhh985.xm0m39n.x9f619.x78zum5.xdt5ytf.x2lah0s.xk390pu.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x1n2onr6.xggy1nq.x11njtxf')))[1]
        description = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.x9f619.xjbqb8w.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.xsag5q8.xz9dl7a.x1uhb9sk.x1plvlek.xryxfnj.x1c4vz4f.x2lah0s.x1q0g3np.xqjyukv.x1qjc9v5.x1oa3qoh.x1nhvcw1')))[0]
        description_txt = [d for d in description.text.split('\n')]
        channel_name = description_txt[0]
        description_txt_actual = ' '.join(description_txt[1:])
        post_time = description.find_element(By.CSS_SELECTOR, 'time').get_attribute('datetime')

    # usernames = [c.split('\n')[0] for c in all_texts]
    # comments = [c.split('\n')[1] for c in all_texts]
    # times = []
    # for c in all_comments_ACTUAL:
    #     try:
    #         times.append(c.find_element_by_css_selector('time.x1ejq31n.xd10rxx.x1sy0etr.x17r0tee.x1roi4f4.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x1n2onr6').get_attribute('datetime'))
    #     except:
    #         try:
    #             times.append(c.find_element_by_css_selector('time.xsgj6o6').get_attribute('datetime'))
    #         except:
    #             try:
    #                 times.append(c.find_element_by_css_selector('time._aaqe').get_attribute('datetime'))
    #             except:
    #                 times.append('')
    #     # times.append('')
    #
    # times_filtered = set([t for t in times if t != '']) # to maintain order after set() operation
    # times_final = []
    # for t in times:
    #     if t in times_filtered and t not in times_final:
    #         times_final.append(t)
    print(len(usernames), len(comments), len(times_final))

    loaded_comments = {}
    loaded_comments['username'] = usernames
    loaded_comments['comment'] = comments
    loaded_comments['time'] = times_final

    if get_meta_data:
        return channel_name, description_txt_actual, post_time, loaded_comments
    else:
        return loaded_comments


def apply_scraping_comments_instagram_updated(video_link):
    link = '/'.join(video_link.split('/')[:5])

    if link.split('/')[3] not in ['p', 'reel']:
        print(f'skipping this link because its not in the correct format {link}')
        return '', '', '',  {'comment': [], 'time': []}
    print(f'processing link {link}')

    login_instagram()
    time.sleep(random.randint(5, 10))
    driver.get(video_link)

    # comments_body = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.x5yr21d.xw2csxc.x1odjw0f.x1n2onr6')))[0]

    comments_old = []

    # In case there is a plus button for loading more comments
    while True:
        try:
            load_more_btn = WebDriverWait(driver, delay).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'button._abl-')))
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
                comments_new = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,
                                                                                                       'div.x9f619.xjbqb8w.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.xsag5q8.xz9dl7a.x1uhb9sk.x1plvlek.xryxfnj.x1c4vz4f.x2lah0s.x1q0g3np.xqjyukv.x1qjc9v5.x1oa3qoh.x1nhvcw1')))
            except:
                try:
                    comments_new = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((
                                                                                                          By.CSS_SELECTOR,
                                                                                                          'div.x1qjc9v5.x972fbf.xcfux6l.x1qhh985.xm0m39n.x9f619.x78zum5.xdt5ytf.x2lah0s.xk390pu.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x1n2onr6.xggy1nq.x11njtxf')))
                except:
                    pass

            driver.execute_script("arguments[0].scrollIntoView();", comments_new[-1])
            time.sleep(5)

            if len(comments_new) == len(comments_old):
                try:
                    print(f'GOT SO FAR {len(comments_new)} - GETTING HIDDEN REPLIES')
                    btn_view_hidden = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((
                                                                                                         By.CSS_SELECTOR,
                                                                                                         'div.x9f619.xjbqb8w.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.xwib8y2.x1y1aw1k.x1uhb9sk.x1plvlek.xryxfnj.x1c4vz4f.x2lah0s.x1q0g3np.xqjyukv.x6s0dn4.x1oa3qoh.x1nhvcw1')))
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
                    btn_view_hidden_v2 = WebDriverWait(driver, delay).until(
                        EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'button._acan._acao._acas._aj1-._ap30')))
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
        btn_view_hidden = WebDriverWait(driver, 2).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,
                                                                                              'div.x1i10hfl.xjbqb8w.x6umtig.x1b1mbwd.xaqea5y.xav7gou.x9f619.x1ypdohk.xt0psk2.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x16tdsg8.x1hl2dhg.xggy1nq.x1a2a7pz.x87ps6o.x1d5wrs8')))
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

    channel_name = comments_old[0].text.split('\n')[0]
    if channel_name.strip() == '':
        try:
            channel_name = comments_old[1].text.split('\n')[0]
        except:
            channel_name = ''
    try:
        description = comments_old[0].text.split('\n')[2]
    except:
        try:
            description = comments_old[1].text.split('\n')[1]
        except:
            description = ''
    try:
        post_time = comments_old[0].find_element_by_css_selector('time').get_attribute('datetime')
    except:
        try:
            post_time = comments_old[1].find_element_by_css_selector('time').get_attribute('datetime')
        except:
            post_time = ''

    all_comments_list = {'comment': [], 'time': []}
    for c in comments_old:
        try:
            comment = c.text
            timeposted = c.find_element_by_css_selector('time').get_attribute('datetime')

            all_comments_list['comment'].append(comment)
            all_comments_list['time'].append(timeposted)
        except:
            pass

    return channel_name, description, post_time, all_comments_list


def apply_scraping_comments_instagram(video_link):
    time.sleep(random.randint(5, 10))
    driver.get(video_link)

    delay = 30  # delay time for WebDriver (in seconds)
    print('Loading comments of the video: {}'.format(video_link))
    all_comments_list = {"username": [], "time": [], "comment": []}
    count = 0
    attempts = 1
    len_old = 0
    channel_name, description, post_time = None, None, None
    while True:
        try:

            main = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.x5yr21d.xw2csxc.x1odjw0f.x1n2onr6')))[0]
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", main)

            try:
                close = WebDriverWait(driver, 2).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'svg[aria-label="Close"]')))[0]
                close.click()
            except:
                pass
            count += 1
            print(count)
            try:
                all_spans = WebDriverWait(driver, 2).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'span')))
                for s in all_spans:
                    if 'View hidden comments' in s.text:
                        btn_view_hidden = s
                        driver.execute_script("arguments[0].click();", btn_view_hidden)
                        break
            except:
                pass

            try:
                all_replies = WebDriverWait(driver, 2).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'span.x1lliihq.x1plvlek.xryxfnj.x1n2onr6.x193iq5w.xeuugli.x1fj9vlw.x13faqbe.x1vvkbs.x1s928wv.xhkezso.x1gmr53x.x1cpjm7i.x1fgarty.x1943h6x.x1i0vuye.x1fhwpqd.x1s688f.x1roi4f4.x1s3etm8.x676frb.x10wh9bi.x1wdrske.x8viiok.x18hxmgj')))
                for r in all_replies:
                    if 'replies' in r.text and 'View all' in r.text:
                        btn_view_hidden = r
                        driver.execute_script("arguments[0].click();", btn_view_hidden)
            except:
                pass


            if count%5 == 0:
                if count == 5:
                    channel_name, description, post_time, last_20_comments = scrape_loaded_comments_instagram(driver=driver, delay=delay)  # calling function to scrape last 20 comments
                else:
                    last_20_comments = scrape_loaded_comments_instagram(driver=driver, delay=delay, get_meta_data=False)  # calling function to scrape last 20 comments

                print(last_20_comments)
                print(len(last_20_comments['username']))

                if len(last_20_comments) == len_old:
                    attempts -= 1
                    print('attempts = {}'.format(attempts))
                else:
                    len_old = len(last_20_comments)

                all_comments_list["username"].extend(last_20_comments["username"])
                all_comments_list["comment"].extend(last_20_comments["comment"])
                all_comments_list["time"].extend(last_20_comments["time"])

            if attempts == 0:
                return channel_name, description, post_time, all_comments_list

        except:
            print("error while trying to load comments")
            if channel_name is None:
                channel_name, description, post_time, last_20_comments = scrape_loaded_comments_instagram(driver=driver, delay=delay)  # calling function to scrape last 20 comments
            else:
                last_20_comments = scrape_loaded_comments_instagram(driver=driver, delay=delay)
            print(last_20_comments)
            print(len(last_20_comments))

            all_comments_list["username"].extend(last_20_comments["username"])
            all_comments_list["comment"].extend(last_20_comments["comment"])
            all_comments_list["time"].extend(last_20_comments["time"])
            return channel_name, description, post_time, all_comments_list


def scrape_loaded_comments_tiktok(video_link):
    driver.get(video_link)
    comments_old = []

    num_comments = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'p.css-1xwyks2-PCommentTitle.e1a7v7ak1')))
    num_comments = num_comments.text
    print(f'Total number of comments: {num_comments}')

    while True:
        comments_new = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.css-1i7ohvi-DivCommentItemContainer.eo72wou0')))
        driver.execute_script("arguments[0].scrollIntoView();", comments_new[-1])
        time.sleep(random.randint(5, 10))

        if len(comments_new) == len(comments_old):
            comments_old = comments_new
            break

        # if len(comments_new) > 5:
        #     comments_old = comments_new
        #     break

        comments_old = comments_new
        print(f'Got so far {len(comments_old)} comments ...')

    # get all replies
    print('Getting all replies ...')
    try:
        all_replies = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.css-zn6r1p-DivReplyContainer.eo72wou1')))
        for r in all_replies:
            try:
                view_reply_btn = r.find_element_by_css_selector('p.css-1flplee-PReplyActionText.eo72wou4')
                driver.execute_script("arguments[0].scrollIntoView();", view_reply_btn)
                driver.execute_script("arguments[0].click();", view_reply_btn)
                time.sleep(random.randint(5, 10))
            except:
                pass
        comments_new = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.css-1i7ohvi-DivCommentItemContainer.eo72wou0')))
        if len(comments_new) > len(comments_old):
            comments_old = comments_new
    except:
        pass

    print('Getting channel information ...')
    try:
        channel_name = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.css-31630c-DivInfoContainer.e17fzhrb0'))).text
    except:
        channel_name = ''
    print(f'channel name: {channel_name}')

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

    print('Getting post description ...')
    try:
        div_post = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.css-3lfoqn-DivDescriptionContentWrapper-StyledDetailContentWrapper.eqrezik15')))[0]
        description = div_post.text
    except:
        description = ''
        pass

    print(f'post description: {description}')

    all_comments_list = {'comment': [], 'time': []}
    for c in comments_old:
        try:
            comment = c.text
            time_posted = c.find_element_by_css_selector('span.css-1esugaz-SpanCreatedTime.e1g2efjf8').text

            all_comments_list['comment'].append(comment)
            all_comments_list['time'].append(time_posted)
            # print(f'{time_posted}, {comment}')
        except:
            all_comments_list['comment'].append('')
            all_comments_list['time'].append('')

    return channel_name, description, post_time, all_comments_list



def get_facebook_likes(save_dir, links):
    ''' '''
    login_facebook()
    time.sleep(2)
    total_reactions = []
    facebook_links = []
    for link in links:
        if 'facebook' in link:
            if '&ref=sharing' not in link:
                link = link + '&ref=sharing'
            print(link)
            facebook_links.append(link)
            num_reactions = scrape_likes_facebook(post_link=link)
            total_reactions.append(num_reactions)

    with open(os.path.join(save_dir, 'facebook_reactions.txt'), 'w') as f:
        for i, link in enumerate(facebook_links):
            f.write('{} - {}\n'.format(total_reactions[i], link))
    f.close()


def get_youtube_likes(save_dir, links):
    youtube_links = []
    likes = []
    for link in links:
        if 'youtube' in link:
            driver.get(link)
            time.sleep(2)
            try:
                reacts = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'ytd-segmented-like-dislike-button-renderer')))
                # [e.text for e in WebDriverWait(driver, 3).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div#top-level-buttons-computed div.yt-spec-touch-feedback-shape__fill')))]
                like_num = reacts[0].text
                youtube_links.append(link)
                likes.append(like_num)
            except:
                youtube_links.append(link)
                likes.append('-')

    with open(os.path.join(save_dir, 'YouTube_reactions.txt'), 'w') as f:
        for i, link in enumerate(youtube_links):
            f.write('{} - {}\n'.format(likes[i], link))
    f.close()


def twitter_login():
    url = "https://twitter.com/i/flow/login"
    driver.get(url)
    username = WebDriverWait(driver, delay).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[autocomplete="username"]')))
    username.send_keys("fatimamarsad")
    username.send_keys(Keys.ENTER)

    password = WebDriverWait(driver, delay).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[name="password"]')))
    password.send_keys("rinro8-fAdbym-recjic")
    password.send_keys(Keys.ENTER)
    time.sleep(30)


if __name__ == '__main__':
    delay = 30  # delay time for WebDriver (in seconds)
    driver = webdriver.Chrome("C:\Program Files\chromedriver-win32-119\chromedriver.exe")
    database_file = input('please enter the name of the database file: ').strip()  # Fatima, please insert the name of the Database file .txt (Must be in the same directory)
    if 'Twitter' in database_file:
        full_path_database_file = 'Events/{}/{}-Twitter/{}'.format(database_file[:11], database_file[:11], database_file)

    elif 'TikTok' in database_file:
        full_path_database_file = 'Events/{}/{}-TikTok/{}'.format(database_file[:11], database_file[:11],
                                                                   database_file)
    else:
        full_path_database_file = 'Events/{}/{}'.format(database_file[:11], database_file)

    if not os.path.isfile(full_path_database_file):
        raise ValueError('The file you specified does not exist!')
    sliding_window_size = int(input('please enter the number of posts to scrape every time chunk').strip())  # Fatima, please enter the number of posts to read from the DB every time chunk.

    print('Reading from Directory: {}'.format(full_path_database_file))
    print('DB File name: {}'.format(database_file))
    # translator = Translator()
    # define credentials for using reddit API
    r = praw.Reddit(client_id="8FFgAqlPUYJuqjtQ0K-cvg",
                    client_secret="AKiDrJuqxMqvdNDERmk9ShgjswQAGQ",
                    user_agent="ChangeMeClientHiyamGh/0.1 by HiyamGh",
                    username="Hiyam_Gh",
                    password="Perl1997AUB", )

    save_dir = 'Output-Raw/{}/'.format(database_file[:11])
    mkdir(folder=save_dir)
    # archive_file_name = '{}.xlsx'.format(database_file.split('.')[0])
    archive_file_name = '{}'.format(database_file.split('.')[0] + '.xlsx') if 'Twitter' not in database_file else '{}'.format(database_file.split('.')[0] + '_Twitter.xlsx')

    TWITTER_USERNAME = input("Please enter the Twitter user name: ").strip()
    TWITTER_PASSWORD = input("Please enter the Twitter password: ").strip()
    FACEBOOK_USERNAME = input("Please enter the Facebook username: ").strip()
    FACEBOOK_PASSWORD = input("Please enter the Facebook password: ").strip()
    INSTAGRAM_USERNAME = input("Please enter the Instagram username: ").strip()
    INSTAGRAM_PASSWORD = input("Please enter the Instagram password: ").strip()
    TIKTOK_USERNAME = input("Please enter the Tiktok username: ").strip()
    TIKTOK_PASSWORD = input("Please enter the Tiktok password: ").strip()

    print('Saving to directory: {}'.format(save_dir))
    print('archive file name: {}'.format(archive_file_name))
    logged_in_to_facebook = False
    logged_in_to_instagram = False
    logged_in_to_twitter = False
    logged_in_to_tiktok = False

    with open(full_path_database_file, 'r', encoding='utf-8-sig') as f:
        links = [l[:-1] for l in f.readlines()]
        for i, link in enumerate(links):

            # link is a tweet
            if 'twitter.com' in link or 'x.com' in link:
                pass

            # link is a facebook post
            elif 'facebook.com' in link:
                if 'm.facebook.com' in link:
                    link = link.replace('m.facebook.com', 'facebook.com')
                print(link)
                # try:
                #     article = scrape_post_facebook(post_link=link)
                # except:
                #     article = ''

                article = ''

                # try:
                #     post_owner = scrape_facebook_post_owner(post_link=link[3:])
                # except:
                #     post_owner = ''

                post_owner = ''

                try:
                    if not logged_in_to_facebook:
                        login_facebook()
                        logged_in_to_facebook = True

                    if logged_in_to_instagram:
                        logged_in_to_instagram = False
                    if logged_in_to_twitter:
                        logged_in_to_twitter = False
                    if logged_in_to_tiktok:
                        logged_in_to_tiktok = False

                    time.sleep(3)
                    if 'fbid' in link:
                        comments = scrape_comments_facebook(post_link=link)
                    else:
                        comments = scrape_comments_facebook_post(post_link=link)
                except:
                    comments = []

                # Name of Youtube Channel,Original Language,Link to Original Post,Date of Post,Comment Date,Comment,
                if comments != []:
                    # mkdir(save_dir_sub)
                    df = pd.DataFrame()
                    df['comments'] = comments
                    df['post_owner'] = [post_owner for _ in range(len(df))]
                    df = df[['post_owner', 'comments']]
                    df = df.drop_duplicates()
                    # df.to_excel(os.path.join(save_dir_sub, 'article{}_comments_facebook.xlsx'.format(i)), index=False)

                    if os.path.isfile(os.path.join(save_dir, archive_file_name)):
                        print('the archive is already there, adding rows to it')
                        df_archive_old = pd.read_excel(os.path.join(save_dir, archive_file_name))
                    else:
                        df_archive_old = None

                    df_archive = pd.DataFrame(
                        columns=['Name of Youtube Channel', 'Original Language', 'Link to Original Post',
                                 'Date of Post', 'Comment Date', 'Comment', 'Translated Comment'])
                    for i, row in df.iterrows():
                        df_archive = df_archive.append({
                            'Name of Youtube Channel': row['post_owner'],
                            'Original Language': '',
                            'Link to Original Post': link,
                            'Source (FB, Youtube, News website, Twitter, Instagram, TikTok)': 'Facebook',
                            'Date of Post': '',
                            'Description of the video and/or title': article,
                            'Comment Date': '',
                            'Comment': row['comments'],
                            'Translated Comment': '',
                        }, ignore_index=True)

                    if df_archive_old is not None:
                        df_merged = pd.concat([df_archive_old, df_archive])
                        df_merged.to_excel(os.path.join(save_dir, archive_file_name), index=False)
                        print('len of df_merged: {}'.format(len(df_merged)))
                    else:
                        df_archive.to_excel(os.path.join(save_dir, archive_file_name), index=False)
                        print('len of df_archive: {}'.format(len(df_archive)))

            # link is a youtube video
            elif 'youtube' in link:
                try:
                    df_youtube_comments = apply_scraping_comments_youtube(video_link=link)
                    df_youtube_comments = df_youtube_comments.drop_duplicates()
                    # df_youtube_comments.to_excel(os.path.join(save_dir, 'article{}_comments_youtube.xlsx'.format(i)),
                    #                              index=False)

                    if os.path.isfile(os.path.join(save_dir, archive_file_name)):
                        print('the archive is already there, adding rows to it')
                        df_archive_old = pd.read_excel(os.path.join(save_dir, archive_file_name))
                    else:
                        df_archive_old = None

                    df_archive = pd.DataFrame(
                        columns=['Name of Youtube Channel', 'Original Language', 'Link to Original Post',
                                 'Date of Post', 'Comment Date', 'Comment', 'Translated Comment'])
                    for i, row in df_youtube_comments.iterrows():
                        row = {
                            'Name of Youtube Channel': row['video_owner'],
                            'Original Language': '',
                            'Link to Original Post': link,
                            'Source (FB, Youtube, News website, Twitter, Instagram, TikTok)': 'YouTube',
                            'Date of Post': '',
                            'Description of the video and/or title': row['video_title'] + '\n' + row['video_description'],
                            'Comment Date': row['time'],
                            'Comment': row['comment'],
                            'Translated Comment': '',
                        }
                        df_archive = df_archive.append(row, ignore_index=True)
                        print('len of df_archive: {}'.format(len(df_archive)))

                    if df_archive_old is not None:
                        df_merged = pd.concat([df_archive_old, df_archive])
                        df_merged.to_excel(os.path.join(save_dir, archive_file_name), index=False)
                        print('len of df_merged: {}'.format(len(df_merged)))

                    else:
                        df_archive.to_excel(os.path.join(save_dir, archive_file_name), index=False)
                        print('len of df_archive: {}'.format(len(df_archive)))

                except:
                    pass

            elif 'instagram' in link:
                if not logged_in_to_instagram:
                    login_instagram()
                    time.sleep(random.randint(5, 10))
                # channel_name, description, post_time, all_comments_list = apply_scraping_comments_instagram(video_link=link)
                channel_name, description, post_time, all_comments_list = apply_scraping_comments_instagram_updated(video_link=link)
                logged_in_to_instagram = True

                if logged_in_to_facebook:
                    logged_in_to_facebook = False
                if logged_in_to_twitter:
                    logged_in_to_twitter = False
                if logged_in_to_tiktok:
                    logged_in_to_tiktok = False

                print('channel_name', channel_name)
                print('description', description)
                print('post_time', post_time)

                df = pd.DataFrame(all_comments_list)
                df = df.drop_duplicates()

                if os.path.isfile(os.path.join(save_dir, archive_file_name)):
                    print('the archive is already there, adding rows to it')
                    df_archive_old = pd.read_excel(os.path.join(save_dir, archive_file_name))
                else:
                    df_archive_old = None

                df_archive = pd.DataFrame(
                    columns=['Name of Youtube Channel', 'Original Language', 'Link to Original Post', 'Date of Post',
                             'Comment Date', 'Comment', 'Translated Comment'])
                for i, row in df.iterrows():
                    df_archive = df_archive.append({
                        'Name of Youtube Channel': channel_name,
                        'Original Language': '',
                        'Link to Original Post': link,
                        'Source (FB, Youtube, News website, Twitter, Instagram, TikTok)': 'Instagram',
                        'Date of Post': post_time,
                        'Description of the video and/or title': description,
                        'Comment Date': row['time'],
                        'Comment': row['comment'],
                        'Translated Comment': '',
                    }, ignore_index=True)
                if df_archive_old is not None:
                    df_merged = pd.concat([df_archive_old, df_archive])
                    df_merged.to_excel(os.path.join(save_dir, archive_file_name), index=False)
                    print('len of df_merged: {}'.format(len(df_merged)))
                else:
                    df_archive.to_excel(os.path.join(save_dir, archive_file_name), index=False)
                    print('len of df_archive: {}'.format(len(df_archive)))

            elif 'tiktok.com' in link:
                if not logged_in_to_tiktok:
                    login_tiktok()
                    user_input = input('Please enter \'y\' when done logging in manually: ')
                    time.sleep(random.randint(5, 10))
                # channel_name, description, post_time, all_comments_list = apply_scraping_comments_instagram(video_link=link)
                channel_name, description, post_time, all_comments_list = scrape_loaded_comments_tiktok(video_link=link)
                logged_in_to_tiktok = True

                if logged_in_to_facebook:
                    logged_in_to_facebook = False
                if logged_in_to_twitter:
                    logged_in_to_twitter = False
                if logged_in_to_instagram:
                    logged_in_to_instagram = False

                print('channel_name', channel_name)
                print('description', description)
                print('post_time', post_time)

                df = pd.DataFrame(all_comments_list)
                df = df.drop_duplicates()

                if os.path.isfile(os.path.join(save_dir, archive_file_name)):
                    print('the archive is already there, adding rows to it')
                    df_archive_old = pd.read_excel(os.path.join(save_dir, archive_file_name))
                else:
                    df_archive_old = None

                df_archive = pd.DataFrame(
                    columns=['Name of Youtube Channel', 'Original Language', 'Link to Original Post', 'Date of Post',
                             'Comment Date', 'Comment', 'Translated Comment'])
                for i, row in df.iterrows():
                    df_archive = df_archive.append({
                        'Name of Youtube Channel': channel_name,
                        'Original Language': '',
                        'Link to Original Post': link,
                        'Source (FB, Youtube, News website, Twitter, Instagram, TikTok)': 'TikTok',
                        'Date of Post': post_time,
                        'Description of the video and/or title': description,
                        'Comment Date': row['time'],
                        'Comment': row['comment'],
                        'Translated Comment': '',
                    }, ignore_index=True)
                if df_archive_old is not None:
                    df_merged = pd.concat([df_archive_old, df_archive])
                    df_merged.to_excel(os.path.join(save_dir, archive_file_name), index=False)
                    print('len of df_merged: {}'.format(len(df_merged)))
                else:
                    df_archive.to_excel(os.path.join(save_dir, archive_file_name), index=False)
                    print('len of df_archive: {}'.format(len(df_archive)))

            # link is a reddit post
            elif 'reddit.com' in link:
                try:
                    reddit_post_info = get_reddit_post_comments(post_link=link)
                except:
                    reddit_post_info = {}

                if reddit_post_info != {}:
                    df_meta = pd.DataFrame.from_dict(
                        {k: v for k, v in reddit_post_info.items() if k != 'comment_section'})
                    df_comments = pd.DataFrame.from_dict(reddit_post_info['comment_section'])
                    df_all = pd.concat([df_meta, df_comments], ignore_index=True, axis=1)
                    df_all.columns = [k for k in reddit_post_info if k != 'comment_section'] + [k for k in
                                                                                                reddit_post_info[
                                                                                                    'comment_section']]
                    df_all = df_all.drop_duplicates()
                    # df_all.to_excel(os.path.join(save_dir, 'article{}_reddit.xlsx'.format(i)), index=False)

            # the link is not a tweet, facebook post, youtube video, or reddit post
            else:
                if link_is_news_website(article_link=link):
                    try:
                        article = get_article(article_link=link)
                        print('got article - was in list of news websites')
                    except:
                        article = ''
                else:
                    try:
                        # article = getting_the_article(article_link=link)
                        article = getting_the_article_bs4(article_link=link)
                    except:
                        article = ''
                        print('not able to load {}'.format(link))

                # detected_lang = translator.detect(article).lang
                # print('the detected language is: ({}), will be converting to (ar)'.format(detected_lang))
                # if detected_lang != 'ar':
                #     article = translator.translate(article, src=detected_lang, dest='ar').text

                # if article != '':
                #     with open(os.path.join(save_dir, 'article{}.txt'.format(i)), 'w', encoding='utf-8') as f:
                #         f.write(article)
                #     f.close()
                if os.path.isfile(os.path.join(save_dir, archive_file_name)):
                    print('the archive is already there, adding rows to it')
                    df_archive_old = pd.read_excel(os.path.join(save_dir, archive_file_name))
                else:
                    df_archive_old = None

                df_archive = pd.DataFrame(
                    columns=['Name of Youtube Channel', 'Original Language', 'Link to Original Post', 'Date of Post',
                             'Comment Date', 'Comment', 'Translated Comment'])
                df_archive = df_archive.append({
                    'Name of Youtube Channel': '',
                    'Original Language': '',
                    'Link to Original Post': link,
                    'Source (FB, Youtube, News website, Twitter, Instagram)': 'News Website',
                    'Date of Post': '',
                    'Description of the video and/or title': '',
                    'Comment Date': '',
                    'Comment': article,
                    'Translated Comment': '',
                }, ignore_index=True)

                if df_archive_old is not None:
                    df_merged = pd.concat([df_archive_old, df_archive])
                    df_merged.to_excel(os.path.join(save_dir, archive_file_name), index=False)
                    print('len of df_merged: {}'.format(len(df_merged)))
                else:
                    df_archive.to_excel(os.path.join(save_dir, archive_file_name), index=False)
                    print('len of df_archive: {}'.format(len(df_archive)))

            if (i + 1) % sliding_window_size == 0:
                print('sleeping for 3 minutes ...')
                time.sleep(180)  # sleep for 3 mins'''


    # with open(full_path_database_file, 'r', encoding='utf-8-sig') as f:
    #     links = [l[:-1] for l in f.readlines()]
    # f.close()
    # # get_facebook_likes(save_dir, links)
    # get_youtube_likes(save_dir, links)
