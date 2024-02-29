import pandas as pd
from sklearn.model_selection import train_test_split
import os
import re
import string


def remove_integers(text):
    return re.sub("[^a-zA-Z]", " ", str(text))

# Function to read stop words from a text file
def read_stopwords(stopwords_file):
    with open(stopwords_file, 'r', encoding='utf-8') as file:
        stopwords = [line.strip() for line in file]
    return stopwords

# Define a function to remove stop words from a text
def remove_stopwords(text,stopwords):
    words = text.split()  # Tokenize the text by splitting into words
    filtered_words = [word for word in words if word not in stopwords]
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



def remove_diacritics(text):
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
    text = re.sub(arabic_diacritics, '', text)
    return text

def remove_repeating_char(text):
    return re.sub(r'(.)\1+', r'\1\1', text)

arabic_punctuations = '''`÷×؛<>_()*&^%][ـ،/:"؟.,'{}~¦+|!”…“–ـ'''
english_punctuations = string.punctuation
punctuations_pattern = "[" + re.escape(arabic_punctuations + english_punctuations) + "]"

def remove_punctuations(text):
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
    text = remove_stopwords(text,stopwords)
    text = remove_punctuations(text)
    text = remove_non_arabic_words(text)
    text = clean_white_space(text)
    return text

def split_data_experiments_annotated():
    experiments_folder = 'experiments/annotator1/experiment_annotated'
    # Check if the experiment folder exists
    if not os.path.exists(experiments_folder):
        os.makedirs(experiments_folder)
    current_directory = os.getcwd()
    df_annotated=pd.read_excel("Annotated.xlsx", dtype=str)
    ################################ ANNOTATOR I DATA ################################
    df=df_annotated
    df = df.dropna(subset=['Annotator I'])
    df['cleaned_text'] = df['cleaned_text'].replace('', pd.NA)
    df['Final_label']=df['Annotator I']
    
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
    df['Final_label'] = df['Final_label'].map(label_mapping)

    df = pd.get_dummies(df, columns=['Final_label'])
    df['cleaned_text']=df['cleaned_text'].astype(str)
    y=df[['Final_label_accusation','Final_label_incitement', 'Final_label_none', 'Final_label_offensive']]

    # Perform the train-test split only if the folder is created
    x_train, x_test, y_train, y_test = train_test_split(df, y, test_size=0.2, shuffle=True, stratify=y)
    x_train, x_val, y_train, y_val = train_test_split(x_train, y_train,
                                                  test_size=0.25, shuffle=True)


    x_train['cleaned_text'].to_excel(os.path.join(experiments_folder, 'x_train.xlsx'), index=False)
    x_test['cleaned_text'].to_excel(os.path.join(experiments_folder, 'x_test.xlsx'), index=False)
    x_val['cleaned_text'].to_excel(os.path.join(experiments_folder, 'x_val.xlsx'), index=False)


    y_train.to_excel(os.path.join(experiments_folder, 'y_train.xlsx'), index=False)
    y_test.to_excel(os.path.join(experiments_folder, 'y_test.xlsx'), index=False)
    y_val.to_excel(os.path.join(experiments_folder, 'y_val.xlsx'), index=False)

    # ################################ ANNOTATOR II DATA ################################
    df_annotated=pd.read_excel("Annotated.xlsx", dtype=str)
    df=df_annotated
    experiments_folder = 'experiments/annotator2/experiment_annotated'
    if not os.path.exists(experiments_folder):
        os.makedirs(experiments_folder)
        df=df_annotated
    df['Final_label']=df['Annotator II']
    df = df.dropna(subset=['Annotator II'])
    
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
    df['Final_label'] = df['Final_label'].map(label_mapping)

    df = pd.get_dummies(df, columns=['Final_label'])
    df['cleaned_text']=df['cleaned_text'].astype(str)
    y=df[['Final_label_accusation','Final_label_incitement', 'Final_label_none', 'Final_label_offensive']]

    # Perform the train-test split only if the folder is created
    x_train, x_test, y_train, y_test = train_test_split(df, y, test_size=0.2, shuffle=True, stratify=y)
    x_train, x_val, y_train, y_val = train_test_split(x_train, y_train,
                                                  test_size=0.25, shuffle=True)


    x_train['cleaned_text'].to_excel(os.path.join(experiments_folder, 'x_train.xlsx'), index=False)
    x_test['cleaned_text'].to_excel(os.path.join(experiments_folder, 'x_test.xlsx'), index=False)
    x_val['cleaned_text'].to_excel(os.path.join(experiments_folder, 'x_val.xlsx'), index=False)


    y_train.to_excel(os.path.join(experiments_folder, 'y_train.xlsx'), index=False)
    y_test.to_excel(os.path.join(experiments_folder, 'y_test.xlsx'), index=False)
    y_val.to_excel(os.path.join(experiments_folder, 'y_val.xlsx'), index=False)


def split_data_experiments_combined():
    experiments_folder = 'experiments/annotator1/experiment_combined'
    # Check if the experiment folder exists
    if not os.path.exists(experiments_folder):
        os.makedirs(experiments_folder)
    current_directory = os.getcwd()
    df_annotated=pd.read_excel("Annotated.xlsx", dtype=str)
    ################################ ANNOTATOR I DATA ################################
    df=df_annotated
    df['Final_label']=df['Annotator I']
    df = df.dropna(subset=['Annotator I'])
    df['cleaned_text'] = df['cleaned_text'].replace('', pd.NA)
    df = df.dropna(subset=['cleaned_text'])
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
    df['Final_label'] = df['Final_label'].map(label_mapping)

    df_train_annotated, df_test_annotated = train_test_split(df, test_size=0.4, stratify=df['Final_label'], shuffle=True)
    # # get misogynistic data
    letmi_directory= os.path.join(current_directory, "Let-Mi","let-mi_train_part.csv" )
    df_letmi= pd.read_csv(letmi_directory,dtype=str, encoding="utf-8")
    label_mapping = {
    'damning': 'accusation',
    'derailing': 'offensive',
    'discredit': 'accusation',
    'dominance': 'offensive',
    'stereotyping & objectification': 'offensive',
    'sexual harassment': 'offensive',
    'threat of violence': 'incitement', 
    'none':'none'}

    df_letmi['Final_label'] = df_letmi['category'].map(label_mapping)
    columns_to_drop = ['category', 'misogyny', 'target' ]
    df_letmi = df_letmi.drop(columns=columns_to_drop)
    stopwords= read_stopwords("stop_list_1177.txt")
    df_letmi['cleaned_text'] = df_letmi['text'].apply(lambda x: clean_text(x,stopwords))
    

    # combine for train and val
    df_train = df_letmi.append(df_train_annotated[['cleaned_text','Final_label']], ignore_index=True)
    # df_train.to_excel(os.path.join(experiments_folder, 'training_data.xlsx'), index=False)
    
    df_train = pd.get_dummies(df_train, columns=['Final_label'])

    # # test data
    df_test=pd.get_dummies(df_test_annotated, columns=['Final_label'])
    # df_test.to_excel(os.path.join(experiments_folder, 'testing_data.xlsx'), index=False)

    y=df_train[['Final_label_accusation','Final_label_incitement', 'Final_label_none', 'Final_label_offensive']]

    # # # Perform the train-test split only if the folder is created
    x_train, x_val, y_train, y_val = train_test_split(df_train, y, test_size=0.2, shuffle=True, stratify=y)

    x_test=df_test['cleaned_text']
    y_test=df_test[['Final_label_accusation','Final_label_incitement', 'Final_label_none', 'Final_label_offensive']]

    x_train['cleaned_text'].to_excel(os.path.join(experiments_folder, 'x_train.xlsx'), index=False)
    x_test.to_excel(os.path.join(experiments_folder, 'x_test.xlsx'), index=False)
    x_val['cleaned_text'].to_excel(os.path.join(experiments_folder, 'x_val.xlsx'), index=False)


    y_train.to_excel(os.path.join(experiments_folder, 'y_train.xlsx'), index=False)
    y_test.to_excel(os.path.join(experiments_folder, 'y_test.xlsx'), index=False)
    y_val.to_excel(os.path.join(experiments_folder, 'y_val.xlsx'), index=False)

    # ################################ ANNOTATOR II DATA ################################

    experiments_folder = 'experiments/annotator2/experiment_combined'
    # Check if the experiment folder exists
    if not os.path.exists(experiments_folder):
        os.makedirs(experiments_folder)
    current_directory = os.getcwd()
    df_annotated=pd.read_excel("Annotated.xlsx", dtype=str)
    df=df_annotated
    df['Final_label']=df['Annotator II']
    df = df.dropna(subset=['Annotator II'])
    df['cleaned_text'] = df['cleaned_text'].replace('', pd.NA)
    df = df.dropna(subset=['cleaned_text'])
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
    df['Final_label'] = df['Final_label'].map(label_mapping)

    df_train_annotated, df_test_annotated = train_test_split(df, test_size=0.4, stratify=df['Final_label'], shuffle=True)
    # # get misogynistic data
    letmi_directory= os.path.join(current_directory, "Let-Mi","let-mi_train_part.csv" )
    df_letmi= pd.read_csv(letmi_directory,dtype=str, encoding="utf-8")
    label_mapping = {
    'damning': 'accusation',
    'derailing': 'offensive',
    'discredit': 'accusation',
    'dominance': 'offensive',
    'stereotyping & objectification': 'offensive',
    'sexual harassment': 'offensive',
    'threat of violence': 'incitement', 
    'none':'none'}

    df_letmi['Final_label'] = df_letmi['category'].map(label_mapping)
    columns_to_drop = ['category', 'misogyny', 'target' ]
    df_letmi = df_letmi.drop(columns=columns_to_drop)
    stopwords= read_stopwords("stop_list_1177.txt")
    df_letmi['cleaned_text'] = df_letmi['text'].apply(lambda x: clean_text(x,stopwords))
    

    # combine for train and val
    df_train = df_letmi.append(df_train_annotated[['cleaned_text','Final_label']], ignore_index=True)
    df_train.to_excel(os.path.join(experiments_folder, 'training_data.xlsx'), index=False)
    
    df_train = pd.get_dummies(df_train, columns=['Final_label'])

    # # test data
    df_test=pd.get_dummies(df_test_annotated, columns=['Final_label'])
    df_test.to_excel(os.path.join(experiments_folder, 'testing_data.xlsx'), index=False)

    y=df_train[['Final_label_accusation','Final_label_incitement', 'Final_label_none', 'Final_label_offensive']]

    # # # Perform the train-test split only if the folder is created
    x_train, x_val, y_train, y_val = train_test_split(df_train, y, test_size=0.2, shuffle=True, stratify=y)

    x_test=df_test['cleaned_text']
    y_test=df_test[['Final_label_accusation','Final_label_incitement', 'Final_label_none', 'Final_label_offensive']]

    x_train['cleaned_text'].to_excel(os.path.join(experiments_folder, 'x_train.xlsx'), index=False)
    x_test.to_excel(os.path.join(experiments_folder, 'x_test.xlsx'), index=False)
    x_val['cleaned_text'].to_excel(os.path.join(experiments_folder, 'x_val.xlsx'), index=False)


    y_train.to_excel(os.path.join(experiments_folder, 'y_train.xlsx'), index=False)
    y_test.to_excel(os.path.join(experiments_folder, 'y_test.xlsx'), index=False)
    y_val.to_excel(os.path.join(experiments_folder, 'y_val.xlsx'), index=False)



if __name__ == '__main__':
    split_data_experiments_annotated()
    split_data_experiments_combined()
