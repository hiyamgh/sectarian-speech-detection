import pandas as pd
from googletrans import Translator
import time
from tqdm import tqdm
import os

file_name = input('Please enter the name of the dataset to be translated: ')
folder_name = 'Output-Raw/{}/'.format(file_name[:11])
if not os.path.isfile(os.path.join(folder_name, file_name)):
    raise ValueError('The specified file does not exist!!')

df = pd.read_excel(os.path.join(folder_name, file_name)) # Fatima, please enter the path to the archive dataset needed for translations.

translator = Translator()
comments_langs, translated_comments = [], []

for i, row in tqdm(df.iterrows(), total=df.shape[0]):
    comment = str(row['Comment']).strip()
    if comment != '':
        lang = translator.detect(comment).lang

        if lang == 'ar':
            comments_langs.append(lang)
            translated_comments.append('')
        else:
            comments_langs.append(lang)
            translated_comments.append(translator.translate(comment, dest='ar').text)
            time.sleep(2)

    else:
        comments_langs.append('')
        translated_comments.append('')


df['Oringinal Language'] = comments_langs
df['Translated Comment'] = translated_comments

df.to_excel(os.path.join(folder_name, file_name[:-5]+'_translated.xlsx'), index=False)  # Fatima, please enter the path to the archive dataset needed for translations.