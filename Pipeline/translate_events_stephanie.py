import pandas as pd
import pickle
from tqdm import tqdm
import re

evenetnames2shorteventnames = {
    "المجلس التأديبي غادة عون طرد تأديبي غادة عون": "المجلس التأديبي غادة عون طرد",
    "توسيع المطار ميقاتي صفقة المطار ميقاتي": "صفقة المطار ميقاتي",
    "رياض سلامة غسيل أموال رياض سلامة غسل الأموال": "رياض سلامة غسيل أموال",
    "بلال عبدالله إعفاء الطوائف الضرائب والرسوم": "بلال عبدالله الضرائب والرسوم",
    "هنري خوري نادي القضاة وزير العدل نادي القضاة": "هنري خوري نادي القضاة",
    "النازحين فتح البحر علي مرتضى النازحين فتح البحر": "علي مرتضى النازحين فتح البحر",
    "وزير التربية لعبة السلم والحية وزير التربية قوس قزح": "وزير التربية لعبة السلم والحية",
    "وزير الداخلية ملاحقة اللواء عماد عثمان": "ملاحقة اللواء عثمان",
    "دمج الطلاب السوريين بالطلاب اللبنانيين": "دمج الطلاب السوريين اللبنانيين",
    "المرتضى مكافحة الترويج للشذوذ الجنسي": "المرتضى مكافحة شذوذ جنسي",
}


def unique_list(l):
    ulist = []
    [ulist.append(x) for x in l if x not in ulist]
    return ulist


def add_translation(df_2023):
    from googletrans import Translator
    translator = Translator()

    event_descriptions_ar2en = {}
    preliminary_translations = []
    for i, row in tqdm(df_2023.iterrows(), total=len(df_2023)):
        event_desc_ar = str(row['كلمات مفتاحية']).strip()
        if event_desc_ar in ["", "nan"]:
            preliminary_translations.append("")
            continue
        names_mod = event_desc_ar.replace("\"", '')
        names_mod = re.sub(' +', ' ', names_mod)
        if names_mod in evenetnames2shorteventnames:
            names_mod = evenetnames2shorteventnames[names_mod]

        names_mod = ' '.join(unique_list(names_mod.split()))
        event_desc_en = translator.translate(names_mod, src='ar', dest='en').text
        preliminary_translations.append(event_desc_en)
        # print(f'Translated {names_mod} to {event_desc_en}')
        # r = input('Do you agree to this translation?')
        # if r.strip() == 'n':
        #     event_desc_en = input('Alternative Translation: ').strip()
        # event_descriptions_ar2en[names_mod] = event_desc_en

    # return event_descriptions_ar2en
    return preliminary_translations


if __name__ == '__main__':
    # df_events = pd.read_excel('2023.xlsx')
    df_events = pd.read_excel('2023-edited-hiyam-2025.xlsx')
    prelim_trans = add_translation(df_2023=df_events)

    df = pd.DataFrame()
    df["العنوان"] = df_events["العنوان"]
    df["كلمات مفتاحية"] = df_events["كلمات مفتاحية"]
    df["preliminary_google_translation"] = prelim_trans
    df.to_excel("preliminary_keyword_translations.xlsx", index=False)

    # print("Translation dictionary saved as 'event_translations.pkl'")
