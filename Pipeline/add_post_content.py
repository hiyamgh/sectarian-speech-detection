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

df_influencers = pd.read_excel("المؤثرين (3).xlsx", sheet_name="Database")
accounts_twitter = list(df_influencers["Accounts_Twitter"])
handles_twitter = [a.split("/")[-1] if "/" in str(a) else "" for a in accounts_twitter]
handles_names = list(df_influencers["Name"])
affiliation = list(df_influencers["Affiliation"])
# political_party = list(df_influencers["Political Party"])

mps = pd.read_excel("المؤثرين (3).xlsx", sheet_name="Members of Parliament")
handles2MPs = {}
for i, row in mps.iterrows():
    handle = str(row["Twitter Handle"])
    aff_eng = str(row["Affiliation Eng"])
    parliamentary_bloc = str(row["Parliamentary Bloc"])
    eng_name = str(row["Name - English"])
    handles2MPs[handle] = {"affiliation": aff_eng, "parliamentary_bloc": parliamentary_bloc, "eng_name": eng_name}

handles2spokesmen = {}
spk = pd.read_excel("المؤثرين (3).xlsx", sheet_name="Traditional Political Parties S")
for i, row in spk.iterrows():
    if str(row["Twitter Handle"]) not in ["", "nan"]:
        handle = str(row["Twitter Handle"])
        political_party = str(row["Party Affiliation Eng"])
        politician = str(row["Name"])
        handles2spokesmen[handle] = {"eng_name": politician, "political_party": political_party}

handles2primeministers = {}
spk = pd.read_excel("المؤثرين (3).xlsx", sheet_name="Ministers")
for i, row in spk.iterrows():
    if str(row["Twitter Handle"]) not in ["", "nan"]:
        handle = str(row["Twitter Handle"])
        politician = str(row["Name - EN"])
        took_office = str(row["Took Office"])
        left_office = str(row["Left Office"])
        handles2primeministers[handle] = {"eng_name": politician, "took_office": took_office, "left_office": left_office}

handles2politicalparties = {}
pps = pd.read_excel("المؤثرين (3).xlsx", sheet_name="Traditional Political Parties")
for i, row in pps.iterrows():
    if str(row["Twitter Handle"]) not in ["", "nan"]:
        handles = str(row["Twitter Handle"]).split(";")
        for handle in handles:
            party_name = str(row["Political Parties - English"])
            handles2politicalparties[handle] = party_name

tweets2handles = {}
with open('Twitter_links2content_.pickle', 'rb') as handle:
    b = pickle.load(handle)
    for link in b:
        print(link)
        print(b[link])
        try:
            handle = b[link].split("\n")[1].replace("@", "")
        except:
            continue
        if handle in handles_twitter:
            print(f"Affiliation: {affiliation[handles_twitter.index(handle)]}")
            tweets2handles[link] = {
                "eng_name": handles_names[handles_twitter.index(handle)],
                "affiliation": affiliation[handles_twitter.index(handle)]
            }
        if handle in handles2spokesmen:
            if link not in tweets2handles:
                tweets2handles[link] = {"eng_name": handles2spokesmen[handle]["eng_name"]}
            tweets2handles[link]["spokesmen"] = handles2spokesmen[handle]["political_party"]

        if handle in handles2primeministers:
            if link not in tweets2handles:
                tweets2handles[link] = {"eng_name": handles2primeministers[handle]["eng_name"]}
            tweets2handles[link]["prime_minister_took_office"] = handles2primeministers[handle]["took_office"]
            tweets2handles[link]["prime_minister_left_office"] = handles2primeministers[handle]["left_office"]

        if handle in handles2politicalparties:
            if link not in tweets2handles:
                tweets2handles[link] = {"political_party_account": handles2politicalparties[handle]}

        if handle in handles2MPs:
            print(f"MP Affiliation: {handles2MPs[handle]["affiliation"]}")
            print(f"Parliamentary Bloc: {handles2MPs[handle]["parliamentary_bloc"]}")
            if link not in tweets2handles:
                tweets2handles[link] = {"eng_name": handles2MPs[handle]["eng_name"]}
            tweets2handles[link]["mp_affiliation"] = handles2MPs[handle]["affiliation"]
            tweets2handles[link]["parliamentary_bloc"] = handles2MPs[handle]["parliamentary_bloc"]

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
post_owner_info = ["" for _ in range(len(df_united_final))]
for i, row in df_united_final.iterrows():
    link = row["Link"].replace("\n", "")
    if link in links2contents:
        post_content[i] = links2contents[link]
        s = ""
        if link in tweets2handles:
            if "affiliation" in tweets2handles[link]:
                s = f"{tweets2handles[link]["eng_name"]} is an {tweets2handles[link]["affiliation"]}"
                print(s)
            if "spokesmen" in tweets2handles[link]:
                if s is not "":
                    s += f" and is the spokesmen of {tweets2handles[link]["spokesmen"]}"
                else:
                    s += f"{tweets2handles[link]["eng_name"]} is the spokesmen of {tweets2handles[link]["spokesmen"]}"
                print(s)
            if "prime_minister_took_office" in tweets2handles[link]:
                if s is not "":
                    s += f" and was the former Prime Minister of Lebanon and took office between {tweets2handles[link]["prime_minister_took_office"]} and {tweets2handles[link]["prime_minister_left_office"]}"
                else:
                    s += f"{tweets2handles[link]["eng_name"]} was the former Prime Minister of Lebanon and took office between {tweets2handles[link]["prime_minister_took_office"]} and {tweets2handles[link]["prime_minister_left_office"]}"
                print(s)
            if "mp_affiliation" in tweets2handles[link]:
                if tweets2handles[link]["mp_affiliation"] not in ["", "nan"]:
                    if s is not "":
                        s += f" and Member of the Lebanese Parliament affiliated with {tweets2handles[link]["mp_affiliation"]}"
                    else:
                        s += f"{tweets2handles[link]["eng_name"]} is a Member of the Lebanese Parliament affiliated with {tweets2handles[link]["mp_affiliation"]}"
                    print(s)
                if tweets2handles[link]["parliamentary_bloc"] not in ["", "nan"]:
                    s += f" and a member of the {tweets2handles[link]["parliamentary_bloc"]}"
                    print(s)
            if "political_party_account" in tweets2handles[link]:
                s = f"This is the Twitter account for the {tweets2handles[link]["political_party_account"]}"
                print(s)
            post_owner_info[i] = s

df_united_final["PostContent"] = post_content
df_united_final["PostOwnerInfo"] = post_owner_info

df_united_final = df_united_final[['EventID', 'EventDescription', 'EventTypeEN', 'EventTypeAR',
       'Event Window of Date', 'Link', 'PostContent', 'PostOwnerInfo', 'Comment', 'Platform', 'cleaned_text',
       'offensive', 'accusation', 'incitement', 'none', 'Annotated_Served']]
df_united_final.to_excel("df_united_final_post_content_added.xlsx", index=False)
