import pandas as pd
import os
from datetime import datetime
from dateutil.relativedelta import relativedelta
import xlrd
import random
import logging


logger = logging.getLogger('My_app')

events2volumes = {}
# for subdir, dirs, files in os.walk('Volume-New (5)/'):
for subdir, dirs, files in os.walk('Volume-New/'):
# for subdir, dirs, files in os.walk('Volume-TikTok/'):
    for file in files:
        if 'Accounts' not in file and 'Total-KD' in subdir and ('Twitter' in file or 'YouTube' in file or 'Facebook-Comments' in file or 'Instagram' in file or 'TikTok-Comments' in file):

            print('PROCESSING FILE: {} ==========================================================='.format(file))
            print(os.path.join(subdir, file))

            xls = xlrd.open_workbook(os.path.join(subdir, file), on_demand=True)
            sheets = xls.sheet_names()

            events2sheets = {}
            for s in sheets:
                event_id = s[:11]
                if event_id not in events2sheets:
                    events2sheets[event_id] = []
                events2sheets[event_id].append(s)

            for event_name in events2sheets:
                df_all = pd.concat([pd.read_excel(os.path.join(subdir, file), sheet_name) for sheet_name in events2sheets[event_name]]).reset_index(drop=True)
                logger.warning('before dropping duplicate link: {}\nafter dropping duplicate links: {}'.format(len(df_all), len(df_all.drop_duplicates(subset=['Link']))))
                df_all = df_all.drop_duplicates(subset=['Link'])
                # df_all = df_all.drop_duplicates()
                events2sheets[event_name] = df_all

            category = subdir.split('\\')[0].split('/')[-1]

            if 'Accounts' in subdir:
                withaccount = 'KD-Accounts'
            else:
                withaccount = 'KD'

            comments_volume_updated = []
            for event_name in events2sheets:

                if event_name != 'E2023-02-17':
                    continue
                else:
                    print()
                df = events2sheets[event_name]

                if 'Facebook-Comments' in file:
                    days_str = [str(event_name[1:11]) for _ in range(len(df))]
                    df['Day'] = days_str

                if 'Twitter' in file:
                    days_str = [str(d)[:10] for d in list(df['Day'])]
                    df['Day'] = days_str

                if 'Instagram' in file:
                    days_str = [str(d)[:10] for d in list(df['Day'])]
                    df['Day'] = days_str

                if 'YouTube' in file:
                    to_del = []
                    new_dates = []
                    print(df)
                    for i, d in enumerate(list(df['Day'])):
                        if str(d).strip() == 'nan':
                            new_dates.append('')
                            continue
                        d = str(d)
                        d = d.replace('Premiered', '')
                        d = d.replace('on', '')
                        d = d.strip()
                        print(d)
                        # print(d)
                        try:
                            dnew = datetime.strptime(d, '%d %b %Y').strftime('%Y-%m-%d')
                        except:
                            try:
                                dnew = datetime.strptime(d, '%d %b, %Y').strftime('%Y-%m-%d')
                            except:
                                dform = ' '.join(d.split(' ')[:2]) + ' ' + event_name.split('-')[0][1:]
                                try:
                                    dnew = datetime.strptime(dform, '%d %b %Y').strftime('%Y-%m-%d')
                                except:
                                    try:
                                        dnew = datetime.strptime(dform, '%b %d, %Y').strftime('%Y-%m-%d')
                                    except:
                                        try:
                                            dmodified = d + ' 2023'
                                            dnew = datetime.strptime(dform, '%b %d, %Y').strftime('%Y-%m-%d')
                                        except:

                                            to_del.append(i)
                                            print('d issss: ', d)
                                            dnew = ''
                                        # continue

                        # if dnew is not None:
                        new_dates.append(dnew)

                    df['Day'] = new_dates

                if 'TikTok-Comments' in file and len(df) >= 1:
                    comments_new, dates_new = [], []
                    for i, row in df.iterrows():
                        try:
                            date = row['Day'].split('\n')[2]
                            date = datetime.strptime(date, '%Y-%m-%d').strftime('%Y-%m-%d')
                            if 'comments' in row['Comments Volume'].split(' ')[1]:
                                comments = row['Comments Volume'].split(' ')[0]
                                if 'k' in comments or 'K' in comments:
                                    comments = comments.lower()
                                    comments = comments[:comments.index('k')] + '00'
                                    comments = comments.replace('.', '')
                                try:
                                    dates_new.append(date)
                                    comments_new.append(int(float(str(comments))))
                                except:
                                    comments_new.append(0)
                                    dates_new.append('')

                        except:
                            comments_new.append(0)
                            dates_new.append('')

                    df['Day'] = dates_new
                    df['Comments Volume'] = comments_new

                if 'Facebook-Comments' in file and len(df) > 1:
                    comments_new = []
                    for i, c in enumerate(list(df['Comments Volume'])):
                        c = str(c)
                        c_split = c.split(';')
                        for csub in c_split:
                            if 'comment' in csub or 'comments' in csub:
                                num = csub.split(' ')[0]
                                if 'k' in num or 'K' in num:
                                    num = num.lower()
                                    num = num[:num.index('k')] + '00'
                                    num = num.replace('.', '')
                                try:
                                    comments_new.append(int(float(str(num))))
                                except:
                                    comments_new.append(0)
                                    break
                            else:
                                comments_new.append(0)
                                break

                    print('before: {}\nafter: {}'.format(list(df['Comments Volume']), comments_new))

                    try:
                        df['Comments Volume'] = comments_new
                    except:
                        print()

                if 'YouTube' in file:
                    comments_new = []
                    for i, c in enumerate(list(df['Comments Volume'])):
                        if 'Comments' in c:
                            c = c.replace('Comments', '').strip()
                        if 'Comment' in c:
                            c = c.replace('Comment', '').strip()
                        comments_new.append(c)

                    df['Comments Volume'] = comments_new

                days_unique = list(set(list(df['Day'])))
                if len(df) >= 1:
                    print()
                data = []
                for d in days_unique:
                    df_sub = df[df['Day'] == d]
                    volume = 0
                    links = len(df_sub)
                    for i, row in df_sub.iterrows():
                        try:
                            num = str(row['Comments Volume'])
                            num = num.replace(',', '')
                            volume += int(float(num))
                            print(volume)
                        except:
                            volume += 0
                            print(volume)

                    data.append([d, links, volume])

                if 'YouTube' in file:
                    df3 = pd.DataFrame(data, columns=['Day', 'Links-YouTube', 'Comments-Youtube'])
                elif 'Twitter' in file:
                    df3 = pd.DataFrame(data, columns=['Day', 'Links-Twitter', 'Comments-Twitter'])
                elif 'Facebook-Comments' in file:
                    df3 = pd.DataFrame(data, columns=['Day', 'Links-Facebook', 'Comments-Facebook'])
                elif 'Instagram-Comments' in file:
                    df3 = pd.DataFrame(data, columns=['Day', 'Links-Instagram', 'Comments-Instagram'])
                else:
                    df3 = pd.DataFrame(data, columns=['Day', 'Links-TikTok', 'Comments-TikTok'])

                if event_name not in events2volumes:
                    events2volumes[event_name] = {}

                if 'YouTube' in file:
                    if 'YouTube' not in events2volumes[event_name]:
                        events2volumes[event_name]['YouTube'] = [df3]
                    else:
                        events2volumes[event_name]['YouTube'].append(df3)

                elif 'Twitter' in file:
                    if 'Twitter' not in events2volumes[event_name]:
                        events2volumes[event_name]['Twitter'] = [df3]
                    else:
                        events2volumes[event_name]['Twitter'].append(df3)

                elif 'Facebook-Comments' in file:
                    if 'Facebook' not in events2volumes[event_name]:
                        events2volumes[event_name]['Facebook'] = [df3]
                    else:
                        events2volumes[event_name]['Facebook'].append(df3)
                elif 'Instagram' in file:
                    if 'Instagram' not in events2volumes[event_name]:
                        events2volumes[event_name]['Instagram'] = [df3]
                    else:
                        events2volumes[event_name]['Instagram'].append(df3)
                else:
                    if 'TikTok' not in events2volumes[event_name]:
                        events2volumes[event_name]['TikTok'] = [df3]
                    else:
                        events2volumes[event_name]['TikTok'].append(df3)

                events2volumes[event_name]['category'] = category
                events2volumes[event_name]['account'] = withaccount


for e in events2volumes:
    print(e)
    if e == 'E2023-06-01':
        print()
    category = events2volumes[e]['category']
    withaccount = events2volumes[e]['account']

    if 'YouTube' in events2volumes[e]:
        df_youtube = pd.concat(events2volumes[e]['YouTube'], ignore_index=True)
    else:
        df_youtube = pd.DataFrame(columns=['Day', 'Links-YouTube', 'Comments-Youtube'])

    if 'Twitter' in events2volumes[e]:
        df_twitter = pd.concat(events2volumes[e]['Twitter'], ignore_index=True)
    else:
        df_twitter = pd.DataFrame(columns=['Day', 'Links-Twitter', 'Comments-Twitter'])

    if 'Facebook' in events2volumes[e]:
        df_facebook = pd.concat(events2volumes[e]['Facebook'], ignore_index=True)
    else:
        df_facebook = pd.DataFrame(columns=['Day', 'Links-Facebook', 'Comments-Facebook'])

    if 'Instagram' in events2volumes[e]:
        df_instagram = pd.concat(events2volumes[e]['Instagram'], ignore_index=True)
    else:
        df_instagram = pd.DataFrame(columns=['Day', 'Links-Instagram', 'Comments-Instagram'])

    if 'TikTok' in events2volumes[e]:
        df_tiktok = pd.concat(events2volumes[e]['TikTok'], ignore_index=True)
    else:
        df_tiktok = pd.DataFrame(columns=['Day', 'Links-TikTok', 'Comments-TikTok'])

    print(df_youtube)
    print(df_twitter)
    print(df_facebook)
    print(df_instagram)
    print(df_tiktok)

    if len(df_youtube) == 0 and len(df_twitter) == 0 and len(df_facebook) == 0 and len(df_instagram) == 0 and len(df_tiktok) == 0:
        continue

    df_final = df_youtube.merge(df_twitter, how='outer').merge(df_facebook, how='outer').merge(df_instagram, how='outer').merge(df_tiktok, how='outer')

    df_final = df_final.groupby('Day').sum()
    df_final['Day'] = df_final.index
    df_final = df_final[['Day'] + [c for c in df_final.columns if c != 'Day']]

    start_date = datetime.strptime('{}-01-01'.format(e.split('-')[0][1:]), '%Y-%m-%d')
    end_date = datetime.strptime('{}-12-31'.format(e.split('-')[0][1:]), '%Y-%m-%d')
    day = start_date
    weeks2volumes = {}
    off2volumes = {}
    acc2volumes = {}
    inc2volumes = {}
    sacrcasm2volumes = {}
    none2volumes = {}

    # print('df before dropping NaN: {}\ndf after dropping NaN: {}\n'.format(len(df_final), len(df_final.dropna())))
    # df_final = df_final.dropna()
    while day <= end_date:
        current_week = day.strftime('%V')
        weeks2volumes[current_week] = 0
        for i, row in df_final.iterrows():
            try:
                df_week = datetime.strptime(row['Day'], '%Y-%m-%d').strftime('%V')
            except:
                continue
            if df_week == current_week:
                weeks2volumes[current_week] += int(float(str(row['Comments-Youtube']))) if 'Comments-Youtube' in df_final.columns else 0
                weeks2volumes[current_week] += int(float(str(row['Comments-Twitter']))) if 'Comments-Twitter' in df_final.columns else 0
                weeks2volumes[current_week] += int(float(str(row['Comments-Facebook']))) if 'Comments-Facebook' in df_final.columns else 0
                weeks2volumes[current_week] += int(float(str(row['Comments-Instagram']))) if 'Comments-Instagram' in df_final.columns else 0
                weeks2volumes[current_week] += int(float(str(row['Comments-TikTok']))) if 'Comments-TikTok' in df_final.columns else 0

        day = day + relativedelta(days=1)

    for w in weeks2volumes:
        val = weeks2volumes[w]
        offensive = random.randint(0, val)
        accusation = random.randint(0, val - offensive)
        incitement = random.randint(0, val - (offensive + accusation))
        sarcasm = random.randint(0, val - (offensive + accusation + incitement))
        noneoftheabove = random.randint(0, val - (offensive + accusation + incitement + sarcasm))

        off2volumes[w] = offensive
        acc2volumes[w] = accusation
        inc2volumes[w] = incitement
        sacrcasm2volumes[w] = sarcasm
        none2volumes[w] = noneoftheabove

    df_final_weeks = pd.DataFrame()
    df_final_weeks['Week'] = list(weeks2volumes.keys())
    df_final_weeks['Comments'] = list(weeks2volumes.values())
    df_final_weeks['Offensive'] = list(off2volumes.values())
    df_final_weeks['Accusation'] = list(acc2volumes.values())
    df_final_weeks['Incitement'] = list(inc2volumes.values())
    df_final_weeks['Sarcasm'] = list(inc2volumes.values())

    df_final_weeks = df_final_weeks.sort_values(by='Week')

    to_del = []

    with pd.ExcelWriter('Volume-New/{}/Total-{}/{}.xlsx'.format(category, withaccount, e)) as writer:  # doctest: +SKIP
        df_final.to_excel(writer, sheet_name='original', index=False)
        df_final_weeks.to_excel(writer, sheet_name='weekly', index=False)
