import pandas as pd

df = pd.read_excel("2023-edited-hiyam-2025-eventdescen-added.xlsx")
# rows2evenddesc = dict(zip(df["EventIDRowwise"], df["EventDescriptionEN"]))

for i, row in df.iterrows():
    if str(row["day"]) in ["", "nan"]:
        continue
    rownum = str(row["EventIDRowwise"]).split("_")[-1]
    event_type = str(row["EventTypeEN"])
    day = str(row["day"]).replace(".0", "")
    if len(day) < 2:
        day = "0" + day
    month = str(row["month"]).replace(".0", "")
    if len(month) < 2:
        month = "0" + month
    year = str(row["year"]).replace(".0", "")
    date = day + "-" + month + "-" + year
    desc = str(row["EventDescriptionEN"])
    print("\\textbf{Row \#}: %s - \\textbf{Date:} %s - \\textbf{Event Type:} %s - \\textbf{Event Description:} %s" % (i+1, date, event_type, desc))
    print("\n\\noindent\\rule{\\textwidth}{0.4pt}")