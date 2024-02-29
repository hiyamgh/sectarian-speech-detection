import time
from time import sleep
import pandas as pd
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


def twitter_signin(driver):
    delay=30
    url = "https://twitter.com/i/flow/login"
    driver.get(url)
    username = WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[autocomplete="username"]')))
    username.send_keys("fatimamarsad")
    username.send_keys(Keys.ENTER)

    password = WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[name="password"]')))
    password.send_keys("rinro8-fAdbym-recjic")
    password.send_keys(Keys.ENTER)
    time.sleep(30)
    
def get_tweet_replies(tweet_url, driver,folder_path,event_name):
    delay=30
    filename= tweet_url.split("/")[-1]
    print(filename)
    driver.get(tweet_url)
    time.sleep(30)
    tweet_date=driver.find_element(By.XPATH, '//time[@datetime]')
    tweet_date = tweet_date.get_attribute("datetime")

    reply_list =  {'TweetID':[], 'Tweet Text': [], 'Tweet Date': [], 'Twitter User': [], 'Name':[], 'Comment': [], 'CommentDate': [], '#Total Comments':[]}
    tweet_name  = driver.find_element(By.XPATH, '//div[@data-testid="User-Name"]').text.split('\n')[0]
    tweet_user = driver.find_element(By.XPATH, '//div[@data-testid="User-Name"]').text.split('\n')[1]
    tweet_content_elements = driver.find_element(By.XPATH, '//div[@data-testid="tweetText"]')
    
    reply_number= (driver.find_element(By.XPATH, '//div[@data-testid="reply"]').text)
    tweet_content=tweet_content_elements.text

    scrolling = True 
    last_height=0 
    while(scrolling):

        time.sleep(30)  
        new_height = driver.execute_script("return document.body.scrollHeight")
        if(new_height==last_height):    #reach the end
            scrolling=False
            break 
        discover_more=False
        # dates_elements= driver.find_elements(By.XPATH, '//div[@data-testid="User-Name"]')
        reply_elements = driver.find_elements(By.XPATH, '//div[@data-testid="tweetText"]')
        comment_dates_elements= driver.find_elements(By.XPATH, '//time[@datetime]')
        try:
            h2_element = driver.find_element(By.XPATH, '//span[text()="Discover more"]')
            discover_more=True
        except:
            pass
        # Show more replies button
        try:   
            # Wait for the button to become clickable
            wait = WebDriverWait(driver, 15)
            show_more_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//span[text()="Show more replies"]')))
            show_more_button.click()
            wait = WebDriverWait(driver, 20)
            wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(30)
            # dates_elements= driver.find_elements(By.XPATH, '//div[@data-testid="User-Name"]')
            reply_elements = driver.find_elements(By.XPATH, '//div[@data-testid="tweetText"]')
            comment_dates_elements= driver.find_elements(By.XPATH, '//time[@datetime]')
            try:
                h2_element = driver.find_element(By.XPATH, '//span[text()="Discover more"]')
                discover_more=True
            except:
                pass
        except: 
            pass

        # Show offensive replies button
        try:   
            # Wait for the button to become clickable
            wait = WebDriverWait(driver, 15)
            show_more_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//span[text()="Show"]')))
            show_more_button.click()
            wait = WebDriverWait(driver, 20)
            wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(30)
            # dates_elements= driver.find_elements(By.XPATH, '//div[@data-testid="User-Name"]')
            reply_elements = driver.find_elements(By.XPATH, '//div[@data-testid="tweetText"]')
            comment_dates_elements= driver.find_elements(By.XPATH, '//time[@datetime]')
            try:
                h2_element = driver.find_element(By.XPATH, '//span[text()="Discover more"]')
                discover_more=True
            except:
                pass
        except: 
            pass

        # Combine the two lists into pairs
        for reply_element, comment_date in zip(reply_elements, comment_dates_elements):
            try:
                
                reply_list["CommentDate"].append(comment_date.get_attribute("datetime"))

                reply_list["TweetID"].append(filename)
                reply_list["Tweet Text"].append(tweet_content)
                reply_list["Twitter User"].append(tweet_user)
                reply_list["Name"].append(tweet_name)
                reply_list["Tweet Date"].append(tweet_date)
                
                reply_content = reply_element.text
                reply_list["Comment"].append(reply_content)
                reply_list["#Total Comments"].append(reply_number)
                
            except: 
                #reply_date_list.append(date_text)
                #print("pass")
                pass     
        # reply_count = len(reply_list["Comment"])
        print(len(reply_list["Comment"]))
        # print(len(reply_list["CommentDate"]))
        
          
        # if(reply_count>= reply_number):    
        #     scrolling=False
        #     break
        last_height=new_height
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        #time.sleep(30)
    headers = ['TweetID', 'Tweet Text', 'Tweet Date', 'Twitter User','Name', 'Comment', 'CommentDate','#Total Comments', '#Comments Retrieved']
    directory_path = folder_path
    file_name = f'{event_name}_Comments.csv'
    print(file_name)
    file_path = os.path.join(directory_path, file_name)
    if not os.path.exists(file_path):
        df = pd.DataFrame(columns=headers)
        df.to_csv(file_path, index=False)

    df=pd.DataFrame(reply_list)
    df.drop_duplicates(inplace=True)
    df.drop_duplicates(subset='Comment', keep="last", inplace=True)
    df=df[df['Tweet Text'] != df['Comment']]
    if (discover_more):
        df = df.iloc[:-4] # drop discover more tweets i.e. the last discover more tweets shown at the end of the page
    df['#Comments Retrieved']= df.shape[0]

    df.to_csv(file_path, mode="a", header=False, encoding="utf-8", index=False)

def get_tweet_likes(tweet_url,driver):
    delay=30
    retweet_url= tweet_url+"/likes"
    driver.get(retweet_url)
    time.sleep(30)
    retweet_list=[]
    scrolling = True
    last_height=0 
    while(scrolling):
        time.sleep(30)  
        new_height = driver.execute_script("return document.body.scrollHeight")
        if(new_height==last_height):    #reach the end
            scrolling=False
            break 

        reply_elements= driver.find_elements(By.XPATH, '//div[@data-testid="UserCell"]')
         # remove last 3 users i.e. suggested people to follow
        for reply_element in reply_elements[:-3]:
            user_information = reply_element.text.split('\n')
            user_profile = user_information[1]
            retweet_list.append(user_profile)

        last_height=new_height
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        print(len(list(set(retweet_list))))
    return list(set(retweet_list)), len(list(set(retweet_list)))

def likes_tweet(tweet_url,driver,folder_path,event_name):
    delay=30
    # get tweet content and date
    driver.get(tweet_url)
    time.sleep(30)
    tweet_content_elements = driver.find_element(By.XPATH, '//div[@data-testid="tweetText"]')
    tweet_content=tweet_content_elements.text

    tweet_date=driver.find_element(By.XPATH, '//time[@datetime]')
    tweet_date = tweet_date.get_attribute("datetime")

    likes_number= (driver.find_element(By.XPATH, '//div[@data-testid="like"]').text)
    # get retweets
    tweet_likes_list, tweets_retrieved=get_tweet_likes(tweet_url, driver)
    tweet_likes_list=';'.join(tweet_likes_list)
    
    headers = ['TweetID', 'Tweet Text', 'Tweet Date', 'Likes', '#Total likes', '# likes retrieved']
    directory_path = folder_path
    file_name = f'{event_name}_Likes.csv'
    file_path = os.path.join(directory_path, file_name)
    if not os.path.exists(file_path):
        df = pd.DataFrame(columns=headers)
        df.to_csv(file_path, index=False)

    # get tweetID
    filename= tweet_url.split("/")[-1]
    likes_list =  {'TweetID':[], 'Tweet Text': [], 'Tweet Date': [], 'Likes':[], '#Total likes':[], '# likes retrieved':[]}
    likes_list["TweetID"].append(filename)
    likes_list["Tweet Text"].append(tweet_content)
    likes_list["Tweet Date"].append(tweet_date)
    likes_list["Likes"].append(tweet_likes_list)
    likes_list["#Total likes"].append(likes_number)
    likes_list["# likes retrieved"].append(tweets_retrieved)

    df=pd.DataFrame(likes_list)
    df.to_csv(file_path,encoding="utf-8",mode="a", header=False, index=False)

def get_tweet_retweets(tweet_url, driver):
    delay=30
    retweet_url= tweet_url+"/retweets"
    driver.get(retweet_url)
    time.sleep(30)
    retweet_list=[]
    scrolling = True
    last_height=0 
    while(scrolling):
        time.sleep(30)  
        new_height = driver.execute_script("return document.body.scrollHeight")
        if(new_height==last_height):    #reach the end
            scrolling=False
            break 

        reply_elements= driver.find_elements(By.XPATH, '//div[@data-testid="UserCell"]')
        # remove last 3 users i.e. suggested people to follow
        for reply_element in reply_elements[:-3]:
            user_information = reply_element.text.split('\n')
            user_profile = user_information[1]
            retweet_list.append(user_profile)

        last_height=new_height
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        print(len(list(set(retweet_list))))
    return list(set(retweet_list)), len(list(set(retweet_list)))

def retweets_tweet(tweet_url,driver,folder_path,event_name):
    delay=30
    # get tweet content and date
    driver.get(tweet_url)
    time.sleep(30)
    tweet_content_elements = driver.find_element(By.XPATH, '//div[@data-testid="tweetText"]')
    tweet_content=tweet_content_elements.text

    tweet_date=driver.find_element(By.XPATH, '//time[@datetime]')
    tweet_date = tweet_date.get_attribute("datetime")

    retweets_number= (driver.find_element(By.XPATH, '//div[@data-testid="retweet"]').text)
    # get retweets
    retweet_list, retweets_retrieved=get_tweet_retweets(tweet_url, driver)
    retweet_list=';'.join(retweet_list)
    
    # get tweetID
    filename= tweet_url.split("/")[-1]

    headers = ['TweetID', 'Tweet Text', 'Tweet Date','Retweets','#Total Retweets', '#Retweets retrieved']
    directory_path = folder_path
    file_name = f'{event_name}_Retweets.csv'
    file_path = os.path.join(directory_path, file_name)
    if not os.path.exists(file_path):
        df = pd.DataFrame(columns=headers)
        df.to_csv(file_path, index=False)
    reply_list =  {'TweetID':[], 'Tweet Text': [], 'Tweet Date': [], 'Retweets':[],'#Total Retweets':[], '#Retweets retrieved':[]}

    reply_list["TweetID"].append(filename)
    reply_list["Tweet Text"].append(tweet_content)
    reply_list["Tweet Date"].append(tweet_date)
    reply_list["Retweets"].append(retweet_list)
    reply_list["#Total Retweets"].append(retweets_number)
    reply_list["#Retweets retrieved"].append(retweets_retrieved)


    df=pd.DataFrame(reply_list)
    # df.drop_duplicates(inplace=True)
    df.to_csv(file_path,encoding="utf-8",mode="a", header=False, index=False)
def get_user_information(user_url,driver):
    delay=30
    driver.get(user_url)
    time.sleep(30)
    try:
        bio = driver.find_element(By.CSS_SELECTOR, 'div[data-testid="UserDescription"]').text
    except :
        bio = ""

    try:
        name, username = driver.find_element(By.CSS_SELECTOR, 'div[data-testid="UserName"]').text.split('\n')
    except :
        name = ""
        username = ""

    try:
        location = driver.find_element(By.CSS_SELECTOR, 'span[data-testid="UserLocation"]').text
    except :
        location = ""

    try:
        website = driver.find_element(By.CSS_SELECTOR, 'a[data-testid="UserUrl"]').text
    except :
        website = ""

    try:
        join_date = driver.find_element(By.CSS_SELECTOR, 'span[data-testid="UserJoinDate"]').text
    except :
        join_date = ""

    try:
        following = driver.find_element(By.XPATH, "//span[contains(text(), 'Following')]/ancestor::a/span").text
    except :
        following = ""

    try:
        followers = driver.find_element(By.XPATH, "//span[contains(text(), 'Followers')]/ancestor::a/span").text
    except :
        followers = ""

    return bio, name, username, location, website, join_date, following, followers



def get_user_followers(tweet_url, driver):
    delay=30

    retweet_url= tweet_url+"/followers"
    driver.get(retweet_url)
    time.sleep(30)
    retweet_list=[]
    scrolling = True
    last_height=0 
    while(scrolling):
        time.sleep(30)  
        new_height = driver.execute_script("return document.body.scrollHeight")
        if(new_height==last_height):    #reach the end
            scrolling=False
            break 

        followers_elements= driver.find_elements(By.XPATH, '//div[@data-testid="UserCell"]')
         # remove last 3 users i.e. suggested people to follow
        for follower_element in followers_elements[:-3]:
            user_information = follower_element.text.split('\n')
            user_profile = user_information[1]
            retweet_list.append(user_profile)

        last_height=new_height
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        print(len(list(set(retweet_list))))
    return list(set(retweet_list)), len(list(set(retweet_list)))

def get_user(user_url, driver,folder_path,event_name):
    delay=30
    bio, name, username, location, website, join_date, following, followers=get_user_information(user_url,driver)
    # get followers
    followers_list, followers_retrieved= get_user_followers(user_url,driver)
    followers_list=';'.join(followers_list)
    headers = ['Bio', 'Name','Username','Location','Website','Join Date','Following number', 'Followers number','Followers users', '#Followers retrieved']
    directory_path = folder_path
    file_name = f'{event_name}_users.csv'
    file_path = os.path.join(directory_path, file_name)
    if not os.path.exists(file_path):
        df = pd.DataFrame(columns=headers)
        df.to_csv(file_path, index=False)
    reply_list =  {"Bio": [],
    "Name": [],
    "Username": [],
    "Location": [],
    "Website": [],
    "Join Date": [],
    "Following number": [],
    "Followers number": [], 'Followers users':[], '#Followers retrieved':[]}

    reply_list["Bio"].append(bio)
    reply_list["Name"].append(name)
    reply_list["Username"].append(username)
    reply_list["Location"].append(location)
    reply_list["Website"].append(website)
    reply_list["Join Date"].append(join_date)
    reply_list["Following number"].append(following)
    reply_list["Followers number"].append(followers)
    reply_list["Followers users"].append(followers_list)
    reply_list["#Followers retrieved"].append(followers_retrieved)
    df=pd.DataFrame(reply_list)
    df.to_csv(file_path,encoding="utf-8",mode="a", header=False, index=False)
