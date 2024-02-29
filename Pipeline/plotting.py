import os
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt


all_dates = []
all_categories = []
dates2comments = {}

ALL_CATEGORIES = ['Corruption', 'Gender', 'Onsori', 'politics', 'Relegious', 'Sexist']
allowed = []
for cat in ALL_CATEGORIES:
    ans = input('Do you want to include {} in the analysis [y, n]: '.format(cat))
    if ans.lower() == 'y':
        allowed.append(cat)
print('Including the following categories in the analysis: {}\n'.format(allowed))

for root, dirnames, fnames in os.walk("Data"):
    for fname in fnames:
        if 'Twitter' in fname and '.xlsx' in fname:
            print(root)

            date = root.split('\\')[-1][1:11]
            category = root.split('\\')[-3]

            if category in allowed:
                if category not in dates2comments:
                    dates2comments[category] = {}

                all_dates.append(date)
                all_categories.append(category)

                df = pd.read_excel(os.path.join(root, fname))
                for i, row in df.iterrows():
                    commentdate = str(row['CommentDate'])
                    commentdate = commentdate[:10]
                    commentdate = datetime.strptime(commentdate, '%Y-%m-%d').date()

                    try:
                        totalcommets = int(str(row['#Total Comments']))
                    except:
                        try:
                            totalcommets = int(float(str(row['#Total Comments'])))
                        except:
                            totalcommets = 0

                    if commentdate not in dates2comments:
                        dates2comments[category][commentdate] = totalcommets
                    else:
                        dates2comments[category][commentdate] += totalcommets
                print(date)
                print(category)
                print(os.path.join(root, fname))
                print('========================')

print(dates2comments)

writer = pd.ExcelWriter('Plotting.xlsx', engine='xlsxwriter')
years = []
# df = pd.DataFrame(columns=['Category', 'Comment Date', 'Total Comments'])
years_months = []
data = {}
for category in dates2comments:
    df = pd.DataFrame(columns=['Category', 'Comment Date', 'Total Comments'])
    data[category] = {}

    for dt in dates2comments[category]:
        df = df.append({
            'Category': category,
            'Comment Date': dt,
            'Total Comments': dates2comments[category][dt]
        }, ignore_index=True)

    df['Comment Date'] = pd.to_datetime(df['Comment Date'], format='%Y-%m-%d')
    df['Week_Number'] = df['Comment Date'].dt.strftime('%U')
    df['Year-Week'] = df['Comment Date'].dt.strftime('%Y-%U')
    df['Year-Month'] = df['Comment Date'].dt.strftime('%Y-%m')
    df['Year'] = df['Comment Date'].dt.strftime('%Y')
    df = df.sort_values(by='Comment Date')
    df = df[['Category', 'Comment Date', 'Week_Number', 'Year-Week', 'Year-Month', 'Year', 'Total Comments']]
    df.to_excel(writer, sheet_name='{}'.format(category), index=False)

    years.extend(list(df['Year']))
    years_months = list(df['Year-Month'])

    for i, row in df.iterrows():
        if years_months[i] not in data[category]:
            data[category][years_months[i]] = int(str(row['Total Comments']))
        else:
            data[category][years_months[i]] += int(str(row['Total Comments']))

writer.close()

years_unique = list(set(years))
markers = ['o', 'v', 's', 'x', 'D', 'p']
for y in years_unique:
    years_months_unique = pd.date_range('{}-01-01'.format(y), '{}-12-31'.format(y), freq='MS').strftime("%Y-%m").tolist()
    i = 0
    for category in data:
        if len(set(data[category].keys()).intersection(set(years_months_unique))) > 0:
            values = []
            for ymu in years_months_unique:
                if ymu in data[category]:
                    values.append(data[category][ymu])
                else:
                    values.append(None)
            plt.plot(years_months_unique, values, marker=markers[i], label=category)

        i += 1

    for day in list(set(all_dates)):
        d = day.split('-')
        dmod = d[2] + '-' + d[1]
        if dmod in years_months_unique:
            plt.axvline(x=years_months_unique.index(dmod), label=dmod)

    plt.legend()
    fig = plt.gcf()
    fig.set_size_inches(12, 6)
    plt.tick_params(axis='x', rotation=45)
    plt.tight_layout()
    plt.savefig('{}.png'.format(y), dpi=300)
    plt.close()

# overall_dates = []
# for category in dates2comments:
#     xvals = list(dates2comments[category].keys())
#     overall_dates.extend(xvals)
#
# # sorteddates = [datetime.strftime(ts, "%Y-%m-%d") for ts in overall_dates]
# overall_dates.sort()
# sorteddates = [datetime.strftime(ts, "%Y-%m-%d") for ts in overall_dates]
# sorteddates_unique = []
# for d in sorteddates:
#     if d not in sorteddates_unique:
#         sorteddates_unique.append(d)
# print()

    # sorteddates = [datetime.strftime(ts, "%Y-%m-%d") for ts in xvals]
    #
    # yvals = list(dates2comments[category].values())
    #
    # plt.plot(sorteddates, yvals, label=category)
    # plt.tick_params(axis='x', rotation=45)
    #
    # plt.legend()
    #
    # fig = plt.gcf()
    # fig.set_size_inches(12, 6)
    #
    # plt.savefig('{}.png'.format(category))
    # plt.close()





