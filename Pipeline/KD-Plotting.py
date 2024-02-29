import matplotlib.pyplot as plt
import pandas as pd
# from styleframe import StyleFrame, utils
import numpy as np
import arabic_reshaper
from bidi.algorithm import get_display
import os
from datetime import datetime
from matplotlib.pyplot import cm
import seaborn as sns
import random
from tqdm import tqdm


def plot_volume(categories2volumes, add_slabs=False, add_regions=False):
    stats = {}
    weeks_temp = list(categories2volumes['corruption'].keys())

    if add_slabs:
        i = 0
        for category in categories:
            stats[category] = {}
            # colors = cm.Dark2(np.linspace(0, 1, sum([len(selected[cat]) for cat in categories2volumes])))
            weeks = list(categories2volumes[category].keys())
            values = list(categories2volumes[category].values())

            stats[category]['week'] = weeks_temp
            stats[category]['volumes_{}'.format(category)] = values

            events_list = [''] * len(weeks)

            category_en = category
            category_ar = get_display(arabic_reshaper.reshape(categories2arabic[category]))
            plt.plot(weeks, values, label='{} | {}'.format(category_en, category_ar), color=categories2colors[category])

            # colorslines = sns.color_palette("Set1", n_colors=52)
            # linestyles = ['-', '--', ':', '-.']
            # markers = ['o', 's', '^', 'D', 'H', '3', 'P', 'X', '8']

            j = 1
            y_max_curr = max(values)
            for yw in selected[category]:
                w = int(yw.split('-')[1])

                if w in weeks:
                    # try:
                    plt.vlines(x=[weeks.index(w)+1], ymin=-10, ymax=y_max_curr,
                               linestyle='-.',
                               # linestyle=linestyles[j],
                               # color=colorslines[j],
                               color='grey',
                               # label=get_display(
                               #     arabic_reshaper.reshape(selected[category][yw].replace("\"", "").strip()))
                               )
                    # events_list[weeks.index(w)] = ''

                    num_markers = 1  # Adjust the number of markers as needed
                    for x in [weeks.index(w)+1]:
                        events = selected[category][yw]
                        if len(events) > 1:
                            y_values = np.linspace(y_max_curr/20, y_max_curr - y_max_curr/20, len(events)) # Distribute markers evenly from ymin to ymax
                            for k, y in enumerate(y_values):
                                plt.scatter(x, y, color='blue', marker=f'${j}$',
                                            s=100,
                                            label=get_display(arabic_reshaper.reshape(
                                                selected[category][yw][k].replace("\"", "").strip())))

                                j += 1
                                events_list[weeks.index(w)] += selected[category][yw][k].replace("\"", "").strip() + ";\n"

                        else:
                            # y_values = np.linspace(-10, y_max,
                            #                        num_markers)
                            # plt.scatter(np.full_like(y_values, x), y_values, color='red', marker=markers[j])
                            plt.scatter(x, y_max_curr / 2, color='blue', marker=f'${j}$',
                                        s = 100,
                                        label=get_display(arabic_reshaper.reshape(selected[category][yw][0].replace("\"", "").strip())))

                            j += 1

                            events_list[weeks.index(w)] = selected[category][yw][0].replace("\"", "").strip()

                        if add_regions:
                            plt.axvspan(x, x+2, facecolor='red', alpha=.2)

                        # ax.scatter(xi, yi, marker=f'${txt}$', s=200, color=color_i, label=label_i)

            stats[category]['events_{}'.format(category)] = events_list

            plt.ylim([-10, y_max_curr + 10])
            # plt.legend()
            plt.xlabel('Week # | {}'.format(get_display(arabic_reshaper.reshape('رقم الاسبوع'))), fontweight='bold')
            plt.ylabel('Volume | {}'.format(get_display(arabic_reshaper.reshape('حجم التفاعل'))), fontweight='bold')
            plt.title('Volume of engagement online | {}'.format(
                get_display(arabic_reshaper.reshape('حجم التفاعل عل المنصات'))), fontweight='bold')


            plt.legend(loc='upper center',
                       bbox_to_anchor=(0, 1, 1, 0.4),
                       # bbox_to_anchor=(0, 1.02, 1, 0.2),
                       # bbox_to_anchor=(0.5, 1.02),
                       ncol=6,
                       fontsize='xx-small',
                       fancybox=True, shadow=True)

            plt.xticks(range(1, len(weeks) + 1), fontsize=7, rotation=45)
            fig = plt.gcf()
            fig.set_size_inches(12, 6)
            plt.tight_layout()
            if add_regions:
                plt.savefig(os.path.join(save_dirs[category], 'Final_{}_selected_regions.png'.format(category)), dpi=300)
            else:
                plt.savefig(os.path.join(save_dirs[category], 'Final_{}_selected.png'.format(category)), dpi=300)
            plt.close()

            i += 1

            pd.DataFrame(stats[category]).T.to_excel(os.path.join(save_dirs[category], 'lineplots_statistics_horizontal_{}.xlsx'.format(category)), index=False)

    else:
        if len(categories2volumes.keys()) > 1:

            fig, axs = plt.subplots(len(categories2volumes.keys()), 1, figsize=(18, 7),
                                    gridspec_kw={'height_ratios': [1]*len(categories2volumes)})

            # Create an empty list to store legend handles and labels
            legend_labels = []
            z = 0

            for ax in axs.ravel():
                # try:

                category = list(categories2volumes.keys())[z]
                weeks = list(categories2volumes[category].keys())
                values = list(categories2volumes[category].values())
                category_en = category
                category_ar = get_display(arabic_reshaper.reshape(categories2arabic[category]))
                ax.plot(weeks, values, color=colors[z], linewidth=2)

                xticks_values = []
                for w in weeks:
                    val = ''
                    for e in categories2events[category]:
                        if e[1] == w:
                            if val == '':
                                val += e[0]
                            else:
                                val += '\n' + e[0]
                    if '\n' in val:
                        val = '[' + val + ']'
                    xticks_values.append(val)

                # space_between_ticks = 0.7  # Adjust this value based on your preference
                # modified_ticks = [tick + space_between_ticks * i for i, tick in enumerate(weeks)]
                # ax.set_xticks(modified_ticks)
                # ax.set_xticklabels(xticks_values, rotation=90, ha='right', fontsize='x-small', fontweight='bold')

                # ax.set_xticklabels([])  # Hide original tick labels
                # for i, tick_label in enumerate(xticks_values):
                #     ax.text(weeks[i], -0.15, tick_label, rotation=90, ha='right', va='top', fontsize='x-small',
                #             fontweight='bold')

                # space_between_ticks = 0.7
                # modified_ticks = [tick + space_between_ticks * i for i, tick in enumerate(weeks)]
                # ax.set_xticks(weeks)  # Set original ticks
                # ax.set_xticklabels([])  # Hide original tick labels
                # ax.set_xticks(modified_ticks, minor=True)  # Set modified ticks as minor ticks
                # ax.set_xticklabels(xticks_values, rotation=90, ha='right', fontsize='large', fontweight='bold', minor=True)

                # ax.set_ylim([-10, y_max + 10])
                ax.set_ylim([-100, y_max + 100])
                legend_labels.append('{} | {}'.format(categories2names[category_en], category_ar))
                z += 1

                # except:
                #     pass
                #     z += 1

            # lines_labels = [ax.get_legend_handles_labels() for ax in fig.axes]
            # lines, labels = [sum(lol, []) for lol in zip(*lines_labels)]
            # fig.legend(lines, labels)

            # lines_labels = [ax.get_legend_handles_labels() for ax in fig.axes]
            # lines, labels = [sum(lol, []) for lol in zip(*lines_labels)]
            #
            # # Finally, the legend (that maybe you'll customize differently)
            # # fig.legend(lines, labels, loc='upper center', ncol=4)
            # fig.legend(lines, labels, loc='upper center', ncol=4, bbox_to_anchor=(0.5, 1.15))

            plt.xticks(range(1, 53), fontsize=7, rotation=45)

            fig.legend(legend_labels, loc='upper center', ncol=6, bbox_to_anchor=(0.5, 1.001))

            fig.set_size_inches(18, 9)
            fig.tight_layout()


            # fig.suptitle('Volume of engagement online | {}'.format(get_display(arabic_reshaper.reshape('حجم التفاعل عل المنصات'))), fontweight='bold')

            # fig.text(0.5, 0.001, 'Week # | {}'.format(get_display(arabic_reshaper.reshape('رقم الاسبوع'))), ha='center', fontweight='bold')
            # fig.text(0.04, 0.5, 'Volume | {}'.format(get_display(arabic_reshaper.reshape('حجم التفاعل على المنصات'))), va='center', rotation='vertical', fontweight='bold')

            # fig.subplots_adjust(bottom=0.1, left=0.1, right=0.9, top=0.9, wspace=0.2, hspace=0.9)
            fig.subplots_adjust(bottom=0.1, left=0.1, right=0.9, top=0.9, wspace=0, hspace=0)

            plt.xlabel('Week # | {}'.format(get_display(arabic_reshaper.reshape('رقم الاسبوع'))),
                       ha='center', fontweight='bold')
            # plt.ylabel('Volume | {}'.format(get_display(arabic_reshaper.reshape('حجم التفاعل عل المنصات'))), ha='center', fontweight='bold')

            fig.text(0.01, 0.5,
                     'Volume of engagement online| {}'.format(get_display(arabic_reshaper.reshape('حجم التفاعل عل المنصات'))),
                     va='center', rotation='vertical', fontsize='medium',
                     fontweight='bold')


            # plt.suptitle('Volume of engagement online | {}'.format(get_display(arabic_reshaper.reshape('حجم التفاعل عل المنصات'))), fontweight='bold')
            # fig.tight_layout()

            plt.savefig('Final.png', dpi=300)
            plt.close()

            # lineplots_df = pd.DataFrame(stats)
            # lineplots_df.to_excel('lineplots_statistics.xlsx', index=False)


        else:
            for category in categories2volumes:
                weeks = list(categories2volumes[category].keys())
                values = list(categories2volumes[category].values())
                category_en = category
                category_ar = get_display(arabic_reshaper.reshape(categories2arabic[category].decode('utf8')))
                plt.plot(weeks, values, label='{} | {}'.format(category_en, category_ar))

                plt.legend()

                plt.xlabel('Week #', fontweight='bold')
                plt.ylabel('Volume', fontweight='bold')
                plt.ylim([-10, y_max + 10])
                plt.title('Volume of engagement online | {}'.format(get_display(arabic_reshaper.reshape('حجم التفاعل عل المنصات'))), fontweight='bold')
                plt.tight_layout()
                if add_slabs:
                    plt.savefig('Final_selected.png', dpi=300)
                else:
                    plt.savefig('Final.png', dpi=300)
                plt.close()


if __name__ == '__main__':
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
    categories2arabic = {v: k for k, v in category2english.items()}

    # file_name = input('Please enter the name of the \'selected sheet\' excel file: ')
    # df_selected = pd.read_excel(file_name, sheet_name='selected')
    # df_selected = pd.read_excel(file_name, sheet_name='سياسة وأمن')
    selected = {}
    # selected_names = {}
    # for i, row in df_selected.iterrows():

    # added by Dr. Fatima
    selected['gender'] = {}
    selected['gender']['2023-01'] = ['منصور لبكي']

    file_name_events = input("Please enter the name of the events dataset: ")
    df_events = pd.read_excel(file_name_events)

    for i, row in df_events.iterrows():
        date_str = str(row['التاريخ'])

        if '2023' not in date_str:
            continue

        keywords_text = str(row['كلمات مفتاحية']).strip()
        if keywords_text in ["", "nan"]:
            continue


        category = category2english[str(row['النوع'])]
        # if "عماد عثمان" in str(row['كلمات مفتاحية']):
        #     print()
        try:
            date_dt = datetime.strptime(date_str[:10], '%Y-%m-%d').strftime('%Y-%m-%d')
        except:
            try:
                date_dt = datetime.strptime(date_str[:10], '%Y-%d-%m').strftime('%Y-%m-%d')
            except:
                continue
        week = datetime.strptime(date_str[:10], '%Y-%m-%d').strftime('%V')
        year = datetime.strptime(date_str[:10], '%Y-%m-%d').strftime('%Y')
        year_week = year + '-' + week

        if category not in selected:
            selected[category] = {}

        if year_week in selected[category]:
            print('DUPLICATES: category: {}, year week: {}, old: {}'.format(category, year_week, selected[category][year_week]))
            selected[category][year_week].append(str(row['كلمات مفتاحية']).strip())
        else:
            selected[category][year_week] = [str(row['كلمات مفتاحية']).strip()]
        # print(str(row['كلمات مفتاحية']).strip())
        # print()

        # selected.append(year_week)
        # selected_names[year_week] = str(row['كلمات مفتاحية']).strip()

    # file_name_events = input("Please enter the name of the events dataset: ")
    # df_events = pd.read_excel(file_name_events)


    # added by Dr. Fatima
    # selected['gender']['2023-01'] = ['منصور لبكي']

    categories2events = {}
    for i, row in tqdm(df_events.iterrows(), total=len(df_events)):

        keywords_text = str(row['كلمات مفتاحية']).strip()
        keywords_text_facebook = str(row['كلمات مفتاحية']).strip()

        if keywords_text in ["", "nan"]:
            continue

        time_after = row['التاريخ']

        if '2023' not in str(time_after):  # restricting the years 2023
            continue

        if i == 11:
            print()

        time_after_dt = datetime.strptime(str(time_after)[:10], '%Y-%m-%d').strftime('%m-%d')
        week_nb = datetime.strptime(str(time_after)[:10], '%Y-%m-%d').strftime('%V')
        if week_nb[0] == '0':
            week_nb = int(week_nb[1])
        else:
            week_nb = int(week_nb)

        category = str(row['النوع'])
        category_en = category2english[category]  # get the english equivalent of the category

        if category_en not in categories2events:
            categories2events[category_en] = []

        categories2events[category_en].append((time_after_dt, week_nb))

        # # Mansour Labaki
        # time_after_dt = datetime.strptime(str('2023-01-01'), '%Y-%m-%d').strftime('%m-%d')
        # week_nb = datetime.strptime(str('2023-01-01'), '%Y-%m-%d').strftime('%V')
        # categories2events['gender'].append((time_after_dt, week_nb))
        #
        # # Liwaa Othman
        # time_after_dt = datetime.strptime(str('2023-09-25'), '%Y-%m-%d').strftime('%m-%d')
        # week_nb = datetime.strptime(str('2023-09-25'), '%Y-%m-%d').strftime('%V') # 39
        # categories2events['corruption'].append((time_after_dt, week_nb))

    time_after_dt = datetime.strptime(str('2023-01-02'), '%Y-%m-%d').strftime('%m-%d')
    week_nb = datetime.strptime(str('2023-01-02'), '%Y-%m-%d').strftime('%V')
    categories2events['gender'].append((time_after_dt, int(week_nb)))

    categories = []

    # if add_corruption.lower().strip() == 'y':
    categories.append('corruption')
    # if add_gender.lower().strip() == 'y':
    categories.append('gender')
    # if add_political.lower().strip() == 'y':
    categories.append('politics and security')
    # if add_racist.lower().strip() == 'y':
    categories.append('refugee')
    # if add_religious.lower().strip() == 'y':
    categories.append('religion')
    # if add_sexist.lower().strip() == 'y':
    categories.append('sexuality')

    categories2volumes = {}
    # for subdir, dirs, files in os.walk('Volume-New (5)/'):
    for subdir, dirs, files in os.walk('Volume-FACEBOOK/'):
    # for subdir, dirs, files in os.walk('Volume-New/'):
        if '-KD' in subdir:
            for file in files:
                if 'E' in file and '2023' in file:
                    df = pd.read_excel(os.path.join(subdir, file), sheet_name='weekly')

                    # category = subdir.split('\\')[0].split('/')[1]
                    category = subdir.split('\\')[0].split('/')[-1]
                    if category in categories:
                        if category == 'refugee' and 'E2023-06-01' in file:
                            print()
                        print(category)
                        weeks = list(df['Week'])
                        values = list(df['Comments'])

                        print(weeks)
                        print(values)

                        if category not in categories2volumes:
                            categories2volumes[category] = {}

                        for i, w in enumerate(weeks):
                            if w in categories2volumes[category]:
                                categories2volumes[category][w] += int(float(str(values[i])))
                            else:
                                categories2volumes[category][w] = int(float(str(values[i])))
                        print()

    categories2volumes['gender'][1] += 4000 # Mansour Labaki
    categories2volumes['gender'][2] += 92 # "قانون موحد أحوال شخصية"

    # Zaynab Zeater we are Okay
    categories2volumes['gender'][14] += 194 # سعد الحريري
    categories2volumes['gender'][19] += 1003 # صيدا مايو
    categories2volumes['gender'][36] += 1003  # # لينا ناصر الدين السم الاسيد بلدة البساتين

    categories2volumes['religion'][3] += 1051 # تعلم اللغة الشيعية LBCI قاووق
    categories2volumes['religion'][12] += 546 # حسن مرعب قناة MTV
    ###########################################################################################################################
    # categories2volumes['religion'][28] += 1560 # مي شدياق الكحول REMOVED THIS DUE TO A SPREAD FOUND IN THE PLOT
    categories2volumes['religion'][34] += 90 # جونية Pub رسم المسيح

    categories2volumes['politics and security'][16] += 97 # تأجيل انتخابات البلدية
    # categories2volumes['politics and security'][22] += 339 # ain al helwe  REMOVED THIS DUE TO A SPREAD FOUND IN THE PLOT
    # HIYAM NEWWWWWWW categories2volumes['politics and security'][40] += 10591 # tawafan al aqsa

    # HIYAMMMM NEWWWWW categories2volumes['refugee'][16] += 162 # أطفال بركة سمير قصير

    categories2volumes['corruption'][39] += 400 # al liwaa othman
    # HIYAM NEWWWWWWWW categories2volumes['corruption'][31] += 149 # al mansouri masref lebanan

    values = []
    for cat in categories2volumes:
        for w in categories2volumes[cat]:
            values.append(categories2volumes[cat][w])
    y_max = max(values)

    # colors = ['green', 'pink', 'blue', 'red', 'yellow', 'orange']
    # colors = ['#332288', '#88CCEE', '#44AA99', '#117733', '#999933', '#DDCC77', '#CC6677', '#882255', '#AA4499']

    # colors = cm.Dark2(np.linspace(0, 1, sum([len(selected[cat]) for cat in categories2volumes])))

    # Calculate the total number of colors needed
    total_colors = sum([len(categories2volumes[cat]) for cat in categories2volumes])
    # Choose Dark2 color map with distinct colors
    # colors = cm.Dark2(np.linspace(0, 1, total_colors))

    # Politics and security
    # Religion
    # Gender
    # Sexuality
    # Refugees (rather than Refugee)
    # Corruption

    cats_ordered = ['politics and security', 'religion', 'gender', 'sexuality', 'refugee', 'corruption']
    # cats_ordered = ['corruption', 'politics and security', 'religion', 'gender', 'sexuality', 'refugee']
    categories2names = {
        'politics and security': 'Politics and security',
        'religion': 'Religion',
        'gender': 'Gender',
        'sexuality': 'Sexuality',
        'refugee': 'Refugees',
        'corruption': 'Corruption'
    }

    colors = sns.color_palette("Set2", n_colors=total_colors)

    categories2volumesordered = {k: categories2volumes[k] for k in categories2names}
    categories2colors = {cat: colors[i] for i, cat in enumerate(cats_ordered)}

    save_dirs = {}
    for category in categories2volumes:
        # save_dirs[category] = 'Volume-New (5)/{}/Total-KD/'.format(category)
        save_dirs[category] = 'Volume-FACEBOOK/{}/Total-KD/'.format(category)
        # save_dirs[category] = 'Volume-New/{}/Total-KD/'.format(category)
    plot_volume(categories2volumes=categories2volumesordered, add_slabs=False)
    plot_volume(categories2volumes=categories2volumesordered, add_slabs=True, add_regions=False)
    plot_volume(categories2volumes=categories2volumesordered, add_slabs=True, add_regions=True)