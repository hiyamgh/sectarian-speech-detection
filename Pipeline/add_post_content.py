import pickle
import pandas as pd

links2contents = {}
with open('Facebook_links2content_.pickle', 'rb') as handle:
    b = pickle.load(handle)
    for link in b:
        print(link)
        if b[link].strip() != "":
            s = b[link]
            try:
                print(s[:s.index("\n")] + s[s.index("Comments")+len("Comments"):])
                links2contents[link] = s[:s.index("\n")] + s[s.index("Comments")+len("Comments"):]
            except:
                try:
                    print(s[:s.index("\n")] + s[s.index("·") + 1:])
                    links2contents[link] = s[:s.index("\n")] + s[s.index("·") + 1:]
                except:
                    pass
        print("====================================================")

with open('Twitter_links2content_.pickle', 'rb') as handle:
    b = pickle.load(handle)
    for link in b:
        print(link)
        print(b[link])
        links2contents[link] = b[link]
        print("====================================================")

with open('YouTube_links2content_.pickle', 'rb') as handle:
    b = pickle.load(handle)
    for link in b:
        print(link)
        print(b[link])
        links2contents[link] = b[link]
        print("====================================================")


df_united_final = pd.read_excel("df_united_final.xlsx")
post_content = ["" for _ in range(len(df_united_final))]
for i, row in df_united_final.iterrows():
    link = row["Link"].replace("\n", "")
    if link in links2contents:
        post_content[i] = links2contents[link]
df_united_final["PostContent"] = post_content
df_united_final = df_united_final[['EventID', 'EventDescription', 'EventTypeEN', 'EventTypeAR',
       'Event Window of Date', 'Link', 'PostContent', 'Comment', 'Platform', 'cleaned_text',
       'offensive', 'accusation', 'incitement', 'none', 'Annotated_Served']]
df_united_final.to_excel("df_united_final_post_content_added.xlsx", index=False)
