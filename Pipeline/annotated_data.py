import os
import glob
import pandas as pd 
import re
import string

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
    arabic_pattern = re.compile(r"[\u0600-\u06FF]+", re.UNICODE)

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
    filename = input_string.split("/")
    filename = os.path.splitext(filename[-1])[0]
    return filename

if __name__ == '__main__':

    # annotated by the team
    xlsx_pattern = '*.xlsx'
    current_directory = os.getcwd()
    annotation_directory= os.path.join(current_directory, "3تفنيد الداتا")
    annotations = glob.glob(os.path.join(annotation_directory, '**', xlsx_pattern), recursive=True)
    annotated_data = pd.DataFrame()
    for exl_file in annotations:
        if "Timeline" in exl_file:
            continue
        df = pd.read_excel(exl_file,dtype=str)
        df['theme']=exl_file.split("/")[6]
        df['EventID']= exl_file.split("/")[7]
        annotated_data = annotated_data.append(df, ignore_index=True)
    annotated_data['EventID']=annotated_data['EventID']
    stopwords= read_stopwords("stop_list_1177.txt")
    annotated_data['text']=annotated_data['Comment'].astype(str)
    annotated_data['cleaned_text']=annotated_data['text'].apply(lambda x: clean_text(x,stopwords))
    
 
    annotated_data = annotated_data.dropna(subset=['Annotator I', 'Annotator II', 'Annotator III'], how='all')
    annotated_data= annotated_data[['EventID','text','cleaned_text','Annotator I', 'Annotator II', 'Annotator III','theme']]
    annotated_data['Final_label'] = annotated_data['Annotator I'].fillna(annotated_data['Annotator II']).fillna(annotated_data['Annotator III'])
    label_mapping = {
    'سخرية-تهكم': 'sarcasm',
    'موضوعي': 'none',
    'تجريح': 'offensive', 
    'تحريض': 'incitement',
    'كراهية': 'offensive',
    'تخوين': 'accusation', 
    'اتهام': 'accusation',
    'محاسبة': 'none',
    'طائفية': 'offensive', 
    'خوف من الآخر': 'fearful',
    'حزبي': 'offensive', 
    'قمع': 'incitement',
    'تلاعب': 'offensive',
    'ملامة': 'accusation', 
    'طائفي': 'offensive'}
    annotated_data['Final_label'] = annotated_data['Final_label'].map(label_mapping)
    label_mapping = {
    'سخرية-تهكم': 'سخرية-تهكم',
    'موضوعي': 'موضوعي',
    'تجريح': 'تجريح', 
    'تحريض': 'تحريض',
    'كراهية': 'تجريح',
    'تخوين': 'تخوين', 
    'اتهام': 'تخوين',
    'محاسبة': 'موضوعي',
    'طائفية': 'تجريح', 
    'خوف من الآخر': 'خوف من الآخر',
    'حزبي': 'تجريح', 
    'قمع': 'تحريض',
    'تلاعب': 'تجريح',
    'ملامة': 'تخوين', 
    'طائفي': 'تجريح'}

    annotated_data['Collapsed_label Annotator I']= annotated_data['Annotator I'].map(label_mapping)
    annotated_data['Collapsed_label Annotator II']= annotated_data['Annotator II'].map(label_mapping)
    annotated_data['Collapsed_label Annotator III']= annotated_data['Annotator III'].map(label_mapping)

    annotated_data.to_excel("Annotated.xlsx", index=False)
    grouped_data = annotated_data.groupby(['theme', 'Final_label']).size().reset_index(name='count')
    # Save the result to an Excel file
    grouped_data.to_excel('theme_label_counts.xlsx', index=False)