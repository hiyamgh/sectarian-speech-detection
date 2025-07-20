import pandas as pd
import os
import pickle
from googletrans import Translator
from tqdm import tqdm

category2english = {
        # 'عنصري': 'racist',
        'فساد': 'corruption',
        'جندري': 'gender',
        'جنساني': 'sexuality',
        # 'جنسي': 'sexuality',
        'ديني': 'religion',
        'سياسة وأمن': 'politics and security',
        'لجوء': 'refugee'
}


def translate_event_descriptions(df_2023):
    translator = Translator()
    event_desc_ar2en = {}
    for i, row in tqdm(df_2023.iterrows(), total=len(df_2023)):
        if str(row["day"]) in ["", "nan"]:
            continue

        day = str(row["day"]).replace(".0", "")
        if len(day) < 2:
            day = "0" + day
        month = str(row["month"]).replace(".0", "")
        if len(month) < 2:
            month = "0" + month
        year = str(row["year"]).replace(".0", "")
        event_id = "E" + day + "-" + month + "-" + year
        event_category = category2english[str(row["النوع"])]
        row_num = i
        desc_ar = str(row["العنوان"])
        desc_en = translator.translate(desc_ar, src='ar', dest='en').text
        print(f"Translated {desc_ar} into {desc_en}")

        event_identifier = event_id + "_" + event_category + f"_row{row_num+2}"
        event_desc_ar2en[event_identifier] = desc_en

    with open('event_description_translations.pkl', 'wb') as f:
        pickle.dump(event_desc_ar2en, f)
    print("saved translations into event_description_translations.pkl")


def add_event_description_translations(df_2023, translation_dict):
    col_translations, event_identifiers_rowwise = [], []
    for i, row in df_2023.iterrows():
        if str(row["day"]) in ["", "nan"]:
            continue

        day = str(row["day"]).replace(".0", "")
        if len(day) < 2:
            day = "0" + day
        month = str(row["month"]).replace(".0", "")
        if len(month) < 2:
            month = "0" + month
        year = str(row["year"]).replace(".0", "")
        event_id = "E" + day + "-" + month + "-" + year
        event_category = category2english[str(row["النوع"])]
        row_num = i
        event_identifier = event_id + "_" + event_category + f"_row{row_num+2}"
        col_translations.append(translation_dict[event_identifier])
        event_identifiers_rowwise.append(event_identifier)

    latest_len = len(col_translations)
    col_translations.extend(["" for _ in range(len(df_2023) - latest_len)])
    event_identifiers_rowwise.extend(["" for _ in range(len(df_2023) - latest_len)])
    df_2023["EventDescriptionEN"] = col_translations
    df_2023["EventIDRowwise"] = event_identifiers_rowwise

    return df_2023


# def add_event_statuses(df_2023, translations, VOLUME_EVENTS, SERVING_ANNOTATED_EVENTS):
#     event_statuses = []
#     for i, row in df_2023.iterrows():
#         if str(row["day"]) in ["", "nan"]:
#             event_statuses.append("")
#             continue
#         for key in translations:
#             if f"row{i}" in key:
#                 event_unique_identifier = key
#
#         status = ""
#         if eid in VOLUME_EVENTS:
#             status += "volume"
#         if eid in SERVING_ANNOTATED_EVENTS:
#             status += "+annotated"
#         event_statuses.append(status)


# Hiyam: what did we do in volumne, with events that fall in the same day, and they have the same typeeeeeeeeee
if __name__ == '__main__':
    df = pd.read_excel("2023-edited-hiyam-2025.xlsx")
    df_annotated = pd.read_excel("MultiLabel-Annotated.xlsx")
    df_united = pd.read_excel("df_united_final.xlsx")

    VOLUME_EVENTS = set()
    for subdir, dirs, files in os.walk('Volumesssss/'):
        for file in files:
            VOLUME_EVENTS.add(file[:11])

    SERVING_ANNOTATED_EVENTS = set()
    for i, row in df_united.iterrows():
        SERVING_ANNOTATED_EVENTS.add(str(row["EventID"]))

    # print(f"Number of UNIQUE (Volume-Only) events: {len(UNIQUE_EVENTS)}")
    # translate_event_descriptions(df_2023=df) # will save translations of العنوان (event description) into event_description_translations.pkl
    with open('event_description_translations.pkl', 'rb') as f:
        translations = pickle.load(f)

    df_upd = add_event_description_translations(df_2023=df, translation_dict=translations)
    all_cols = list(df_upd.columns)
    # df_upd = df_upd[all_cols[:1] + ["EventIDRowwise"] + all_cols[1:5] + ["EventDescriptionEN"] + all_cols[5:-2]] # just re-ordering columns in the data
    df_upd = df_upd[all_cols[:1] + ["EventIDRowwise"] + all_cols[1:5] + ["EventDescriptionEN"] + all_cols[5:-3]]
    df_upd.to_excel("2023-edited-hiyam-2025-eventdescen-added.xlsx", index=False)