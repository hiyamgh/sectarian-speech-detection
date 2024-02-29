import re
import glob
import string
import pandas as pd
import os

""" Normalization and Data Cleaning Checklist:
*   Removing non arabic words and digits: this will also include english and arabizi and emojis
*   Remove links
*   Remove mentions
*   Remove punctuations (arabic+english)
*   Remove only #hashtag symbol and keep the words
*   Remove diacratics
*   Remove arabic stop words : https://github.com/alaa-a-a/multi-dialect-arabic-stop-words/tree/main
*   Remove one letter words
*   Normalize repeating characters
*   Replace ة  with ه
*   Replace [إأآا with ا
*   Replace ى with ي
*   Remove duplicates """ 

def create_folder_if_not_exists(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Folder '{folder_path}' created successfully.")
    else:
        print(f"Folder '{folder_path}' already exists.")


def remove_integers(text):
    return re.sub("[^a-zA-Z]", " ", str(text))

# Function to read stop words from a text file
def read_stopwords(stopwords_file):
    with open(stopwords_file, 'r', encoding='utf-8') as file:
        stopwords = [line.strip() for line in file]
    return stopwords

# Define a function to remove stop words from a text
def remove_stopwords(text):
    words = text.split()  # Tokenize the text by splitting into words
    filtered_words = [word for word in words if word.lower() not in stopwords]
    return ' '.join(filtered_words)

def remove_links(text):
    return re.sub('((www\.[^\s]+)|(https?://[^\s]+))', ' ', text)

def remove_non_arabic_words(text):
    # Define a regular expression pattern to match Arabic words
    arabic_pattern = re.compile(r'[\u0600-\u06FF]+', re.UNICODE)

    # Find all Arabic words in the text and join them to form a cleaned text
    arabic_words = re.findall(arabic_pattern, text)
    cleaned_text = ' '.join(arabic_words)

    return cleaned_text

def remove_arabic_one_letter_words(text):
    # Define a regular expression pattern to match one-letter Arabic words
    pattern = r'\b[\u0621-\u064A]\b'

    # Use re.sub to replace one-letter Arabic words with an empty string
    text = re.sub(pattern, '', text)

    return text

arabic_diacritics = re.compile("""
    ّ    | # Tashdid
    َ    | # Fatha
    ً    | # Tanwin Fath
    ُ    | # Damma
    ٌ    | # Tanwin Damm
    ِ    | # Kasra
    ٍ    | # Tanwin Kasr
    ْ    | # Sukun
    ـ     # Tatwil/Kashida
""", re.VERBOSE)

def remove_diacritics(text):
    text = re.sub(arabic_diacritics, '', text)
    return text

def remove_repeating_char(text):
    return re.sub(r'(.)\1+', r'\1\1', text)

def remove_punctuations(text):
    arabic_punctuations = '''`÷×؛<>_()*&^%][ـ،/:"؟.,'{}~¦+|!”…“–ـ'''
    english_punctuations = string.punctuation
    punctuations_pattern = "[" + re.escape(arabic_punctuations + english_punctuations) + "]"
    return re.sub(punctuations_pattern, ' ', text)

def normalize_arabic(text):
    text = re.sub("[إأآا]", "ا", text)
    text = re.sub("ى", "ي", text)
    text = re.sub("ة", "ه", text)
    text = re.sub("گ", "ك", text)
    return text

def clean_white_space(text):
    return re.sub(r'\s+', ' ', text).strip()

def clean_text(text, stopwords):

    text = remove_arabic_one_letter_words(text)
    text = remove_diacritics(text)
    text = remove_repeating_char(text)
    text = remove_links(text)
    text = normalize_arabic(text)
    text = remove_stopwords(text)
    text = remove_punctuations(text)
    text = remove_non_arabic_words(text)
    text = clean_white_space(text)
    return text

def remove_csv_word(input_string):
    filename = input_string.split("\\")
    filename = os.path.splitext(filename[-1])[0]
    return filename


if __name__ == '__main__':


    current_directory = os.getcwd()
    os.chdir(current_directory)

    # Assuming 'df' and 'full_text' column exist
    stopwords= read_stopwords("stop_list_1177.txt")

    output_clean = "Output-Clean"
    

    create_folder_if_not_exists(os.path.join(current_directory, output_clean))
    new_folder_path = os.path.join(current_directory, output_clean)
    # Event name prompt
    file_name = input("Enter the name of the event: ")
    subdirectory_prefix = file_name

    # find all csv files
    csv_pattern = '*.csv'

    # search for events twitter subfolder
    base_directory= os.path.join(current_directory, "Output-Raw")
    subdirectory_path = os.path.join(base_directory, subdirectory_prefix, subdirectory_prefix+'-Twitter' + '*')

    create_folder_if_not_exists(os.path.join(new_folder_path, subdirectory_prefix))
    create_folder_if_not_exists(os.path.join(new_folder_path, subdirectory_prefix, subdirectory_prefix+'-Twitter' ))
    folder_path=os.path.join(new_folder_path, subdirectory_prefix,subdirectory_prefix+'-Twitter' )
    print(folder_path)
    # find all csv files
    csv_files = glob.glob(os.path.join(subdirectory_path, '**', csv_pattern), recursive=True)

    for csv_file in csv_files:
        if("_Comments" in csv_file):
            print(folder_path)
            df=pd.read_csv(csv_file, dtype=str, encoding="utf-8")
            missing_values = df['Comment'].isnull()
            df = df[~missing_values]
            df['Comment'] = df['Comment'].astype(str)
            df['Comment_Clean']= df['Comment'].apply(lambda x: clean_text(x,stopwords))
            print(remove_csv_word(csv_file))
            print(os.path.join(folder_path,remove_csv_word(csv_file)+".xlsx"))
            df.to_excel(os.path.join(folder_path,remove_csv_word(csv_file)+".xlsx"), index=False)
        else: 
            df=pd.read_csv(csv_file, dtype=str, encoding="utf-8")
            df.to_excel(os.path.join(folder_path,remove_csv_word(csv_file)+".xlsx"), index=False)
