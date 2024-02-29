from main import *
import re
import os
import glob

def create_folder_if_not_exists(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Folder '{folder_path}' created successfully.")
    else:
        print(f"Folder '{folder_path}' already exists.")

def remove_csv_word(input_string):
    filename = input_string.split("\\")
    filename = os.path.splitext(filename[-1])[0]
    return filename

if __name__ == '__main__':
    # current_directory = os.getcwd()
    # Get the directory of the current Python script
    current_directory = os.getcwd()

    output_raw = "Output-Raw"

    new_folder_path = os.path.join(current_directory, output_raw)

    print(new_folder_path)

    if not os.path.exists(new_folder_path):
        os.makedirs(new_folder_path)
        print(f"Folder '{output_raw}' created successfully at {new_folder_path}")
    else:
        print(f"Folder '{output_raw}' already exists at {new_folder_path}")
    #os.chdir(output_raw)

    file_name = input("Enter the file name to search for: ")

    for folder_path, _, file_list in os.walk(os.getcwd()):
        for text_folder_path, _, text_file_list in os.walk(folder_path):
            if file_name in text_file_list:
                file_path = os.path.join(text_folder_path, file_name)
                print(f"File '{file_name}' found at {file_path}")
                file_found = True

                # print(file_path)
                delay = 30
                driver = webdriver.Chrome()
                twitter_signin(driver)

                print(f"###### START OF EVENT {file_path}#########")
                with open(file_path, 'r') as file:
                    # Read the content of the file
                    file_content = file.read()
                event_name= file_path.split("\\")[-1][:-4]
                print(event_name)
                sub_folder_path = event_name.split(".")[0][:11]
                print(sub_folder_path)

                create_folder_if_not_exists(os.path.join(new_folder_path, sub_folder_path))
                create_folder_if_not_exists(os.path.join(new_folder_path, sub_folder_path, event_name))
                folder_path=os.path.join(new_folder_path, sub_folder_path, event_name)
                #folder_path=os.path.join(folder_path, event_name)
                print(folder_path)
                lines = file_content.split('\n')

                # Extract the URLs
                urls = []
                for line in lines:
                    if line.startswith('https://x') or line.startswith('https://twitter'):
                        modified_url = line.replace("https://x", "https://twitter").replace("?s=20", "")
                        urls.append(modified_url)

                distinct_users = set()        
                pattern = r'https://twitter\.com/\w+'        
                for url in urls:
                    print(url)
                    get_tweet_replies(url, driver,folder_path,event_name)
                    # likes_tweet(url, driver,folder_path,event_name)
                    # retweets_tweet(url, driver,folder_path,event_name)
                    # match = re.search(pattern, url)
                    # if match:
                    #     username = match.group()
                    #     distinct_users.add(username)

                # distinct_users_list = list(distinct_users)

                # # Print the distinct usernames
                # print("Distinct Users:")
                # for user_url in distinct_users_list:
                #     get_user(user_url, driver,folder_path, event_name)
                # print(f"###### END OF EVENT {file_path}#########")
                driver.quit()


                # find all csv files
                csv_pattern = '*.csv'


                # find all csv files
                csv_files = glob.glob(os.path.join(folder_path, '**', csv_pattern), recursive=True)
                print(csv_files)
                for csv_file in csv_files:
                    df=pd.read_csv(csv_file, dtype=str, encoding="utf-8")
                    df.to_excel(os.path.join(folder_path,remove_csv_word(csv_file)+".xlsx"), index=False)
                    
                break
            break

                
