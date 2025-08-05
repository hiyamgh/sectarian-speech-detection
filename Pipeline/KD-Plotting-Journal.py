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
import re
import pickle

font_family = "Arial"  # Change this to "Helvetica" if you prefer Helvetica
plt.rcParams['font.family'] = font_family
plt.rcParams['font.size'] = 8  # Set the desired default font size (change 12 to your preferred size)
plt.rcParams['text.antialiased'] = False
plt.rcParams['text.hinting'] = False
plt.rcParams['lines.dash_capstyle'] = 'butt'  # or 'round'
# plt.rcParams['legend.fontsize'] = 7  # Set the legend font size


# Set the journal type ('large' or 'small')
journal_type = 'small'  # Change this to 'small' as needed

# Define the figure dimensions based on the journal type
if journal_type == 'large':
    # For double-column text areas
    fig_width_mm = 84
    fig_height_mm = 234
elif journal_type == 'small':
    # For small-sized journals
    fig_width_mm = 119
    fig_height_mm = 59
else:
    raise ValueError("Invalid journal type. Use 'large' or 'small'.")

# Convert mm to inches for Matplotlib
fig_width_inches = fig_width_mm / 25.4
fig_height_inches = fig_height_mm / 25.4


def mkdir(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

def unique_list(l):
    ulist = []
    [ulist.append(x) for x in l if x not in ulist]
    return ulist


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


def plot_volume(categories2volumes, add_slabs=False, add_regions=False, plot_in_arabic=True):
    weeks_temp = list(categories2volumes['corruption'].keys())
    legend_handles = []
    legend_labels = []

    if add_slabs:
        # fig_height_inches_temp = 100 / 25.4
        i = 0
        for category in categories:


            weeks = list(categories2volumes[category].keys())
            values = list(categories2volumes[category].values())

            events_list = [''] * len(weeks)

            category_en = category
            category_ar = get_display(arabic_reshaper.reshape(categories2arabic[category]))
            plt.plot(weeks, values, label='{} | {}'.format(category_en, category_ar), color=categories2colors[category])

            j = 1
            y_max_curr = max(values)
            for yw in selected[category]:
                w = int(yw.split('-')[1])

                if w in weeks:
                    # try:
                    plt.vlines(x=[weeks.index(w)+1], ymin=-10, ymax=y_max_curr,
                               linestyle='-.',
                               color='grey',
                               )

                    num_markers = 1  # Adjust the number of markers as needed
                    for x in [weeks.index(w)+1]:
                        events = selected[category][yw]
                        if len(events) > 1:
                            y_values = np.linspace(y_max_curr/20, y_max_curr - y_max_curr/20, len(events)) # Distribute markers evenly from ymin to ymax
                            for k, y in enumerate(y_values):

                                if plot_in_arabic:
                                    thescatter = plt.scatter(x, y, color='red', marker=f'${j}$',
                                                s=20,
                                                linewidths=0.5,
                                                label=get_display(arabic_reshaper.reshape(
                                                    selected[category][yw][k].replace("\"", "").strip())),
                                                zorder=3)
                                    # LEGEND_ONLY_LABELS.append(thescatter)

                                    j += 1
                                    events_list[weeks.index(w)] += selected[category][yw][k].replace("\"", "").strip() + ";\n"
                                else:
                                    thescatter = plt.scatter(x, y, color='red', marker=f'${j}$',
                                                             s=20,
                                                             linewidths=0.5,
                                                             label=selected[category][yw][k].replace("\"", "").strip(),
                                                             zorder=3)
                                    # LEGEND_ONLY_LABELS.append(thescatter)

                                    j += 1
                                    events_list[weeks.index(w)] += selected[category][yw][k].replace("\"", "").strip() + ";\n"

                        else:
                            # y_values = np.linspace(-10, y_max,
                            #                        num_markers)
                            # plt.scatter(np.full_like(y_values, x), y_values, color='red', marker=markers[j])


                            if plot_in_arabic:
                                plt.scatter(x, y_max_curr / 2, color='red', marker=f'${j}$',
                                            s = 20,
                                            linewidths=0.5,
                                            label=get_display(arabic_reshaper.reshape(selected[category][yw][0].replace("\"", "").strip())),
                                            zorder=3)

                                j += 1

                                events_list[weeks.index(w)] = selected[category][yw][0].replace("\"", "").strip()
                            else:
                                try:
                                    plt.scatter(x, y_max_curr / 2, color='red', marker=f'${j}$',
                                                s=20,
                                                linewidths=0.5,
                                                label=selected[category][yw][0].replace("\"", "").strip(),
                                                zorder=3)
                                except:
                                    print()

                                j += 1

                                events_list[weeks.index(w)] = selected[category][yw][0].replace("\"", "").strip()

                            # Collect handles and labels for scatter plots in this category
                            handles, labels = plt.gca().get_legend_handles_labels()
                            legend_handles = handles
                            legend_labels = labels

                        if add_regions:
                            plt.axvspan(x, x+2, facecolor='red', alpha=.2)

            plt.ylim([-10, y_max_curr + 10])

            # if category in ['corruption', 'sexuality']:
            #     plt.legend(loc='upper center',
            #                bbox_to_anchor=(0, 1, 1, 0.6),
            #                ncol=5,
            #                fontsize='xx-small',
            #                fancybox=True, shadow=True, mode="expand")
            # else:
            #     plt.legend(loc='upper center',
            #                bbox_to_anchor=(0, 1, 1, 0.6),
            #                ncol=4,
            #                fontsize='xx-small',
            #                fancybox=True, shadow=True, mode="expand")


            # plt.xticks(range(1, len(weeks) + 1), fontsize=7, rotation=45)
            plt.xticks(rotation=45)

            fig = plt.gcf()
            # fig.set_size_inches(fig_width_inches, fig_height_inches_temp)
            fig.set_size_inches(fig_width_inches, fig_height_inches)

            plt.tight_layout()
            if add_regions:
                plt.savefig(os.path.join(save_dirs2, '{}.png'.format(category)), dpi=600, bbox_inches='tight', pad_inches=0.1)
            else:
                plt.savefig(os.path.join(save_dirs2, '{}.png'.format(category)), dpi=600, bbox_inches='tight', pad_inches=0.1)
            plt.close()

            i += 1


            # Create an empty plot
            fig_legend, ax_legend = plt.subplots()

            def wrap_text(text, max_words=4):
                words = text.split()
                return '\n'.join([' '.join(words[i:i + max_words]) for i in range(0, len(words), max_words)])

            legend_labels = [wrap_text(label, max_words=3) for label in legend_labels]
            # Add a legend
            # if category in ['corruption', 'sexuality']:
            #     ax_legend.legend(legend_handles, legend_labels, loc='upper center', bbox_to_anchor=(0, 0, 1, 1), ncol=3, columnspacing=0.2, fontsize='small')
            # else:
            #     ax_legend.legend(legend_handles, legend_labels, loc='upper center', bbox_to_anchor=(0.5, 1.15), ncol=2, fontsize='small')
            # if category in ['corruption', 'sexuality', 'gender']:
            # ax_legend.legend(
            #         legend_handles,
            #         legend_labels,
            #         loc='upper center',
            #         bbox_to_anchor=(0, 0.15, 1, 1),  # 👈 move legend up slightly
            #         ncol=3,
            #         columnspacing=0.3,
            #         fontsize='xx-small',
            #         mode='expand'  # 👈 force stretching horizontally
            #     )
            if category == 'corruption':
                legend_labels = [wrap_text(label, max_words=2) for label in legend_labels]
                ax_legend.legend(
                    legend_handles,
                    legend_labels,
                    loc='upper center',
                    bbox_to_anchor=(0, 0.15, 1, 1),  # full width
                    ncol=5,
                    columnspacing=1,
                    fontsize='xx-small',
                    mode='expand'
                )
            else:
                ax_legend.legend(
                    legend_handles,
                    legend_labels,
                    loc='upper center',
                    bbox_to_anchor=(0, 0.1, 1, 1),  # full width
                    ncol=3,
                    columnspacing=0.3,
                    fontsize='xx-small',
                    mode='expand'
                )

            # else:
            #     ax_legend.legend(
            #         legend_handles,
            #         legend_labels,
            #         loc='upper center',
            #         bbox_to_anchor=(0, 0.15, 1, 1),  # 👈 adjusted for all
            #         ncol=2,
            #         fontsize='x-small',
            #         mode='expand'  # 👈 stretch legend across full width
            #     )


            ax_legend.axis('off')

            fig_legend.set_size_inches(fig_width_inches, fig_height_inches)

            # Display the plot
            plt.savefig(os.path.join(save_dirs2, '{}_legend.png'.format(category)), dpi=600)
            plt.close()


    else:
        if len(categories2volumes.keys()) > 1:

            fig, axs = plt.subplots(len(categories2volumes.keys()), 1, figsize=(fig_width_inches, fig_height_inches), gridspec_kw={'height_ratios': [1]*len(categories2volumes)})

            z = 0

            for ax in axs.ravel():
                # try:

                category = list(categories2volumes.keys())[z]
                weeks = list(categories2volumes[category].keys())
                values = list(categories2volumes[category].values())
                category_en = category
                category_ar = get_display(arabic_reshaper.reshape(categories2arabic[category]))
                ax.plot(weeks, values, color=colors[z], label='{} | {}'.format(categories2names[category_en], category_ar), linewidth=1.0)

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

                # ax.set_ylim([-10, y_max + 10])
                ax.set_ylim([-100, y_max + 100])

                z += 1

            # plt.xticks(range(1, 53), fontsize=7, rotation=45)
            plt.xticks(rotation=45)

            # Display legend for each subplot
            for ax in axs:
                ax.legend(fontsize='xx-small')

            fig.set_size_inches(fig_width_inches, fig_height_inches)
            fig.tight_layout()

            fig.subplots_adjust(hspace=0)

            plt.savefig(os.path.join(save_dirs2, 'Final.png'), dpi=600)
            plt.savefig(os.path.join(save_dirs2, 'Final.pdf'), dpi=600)
            plt.close()


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
                    plt.savefig('Final_selected.png', dpi=600)
                else:
                    plt.savefig('Final.png', dpi=600)
                plt.close()


def add_translation(df_2023):
    from googletrans import Translator
    translator = Translator()

    event_descriptions_ar2en = {}
    for i, row in df_2023.iterrows():
        event_desc_ar = str(row['كلمات مفتاحية']).strip()
        if event_desc_ar in ["", "nan"]:
            continue
        event_desc_en = translator.translate(event_desc_ar, src='ar', dest='en').text
        event_descriptions_ar2en[event_desc_ar] = event_desc_en

    return event_descriptions_ar2en


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

    selected = {}

    # added by Dr. Fatima
    selected['gender'] = {}
    # selected['gender']['2023-01'] = ['منصور لبكي']
    selected['gender']['2023-01'] = ['Mansour Labaki']

    # file_name_events = input("Please enter the name of the events dataset: ")
    # df_events = pd.read_excel(file_name_events)

    df_events = pd.read_excel("2023-edited-hiyam-2025-eventdescen-added.xlsx")

    # with open('event_translations.pkl', 'rb') as f:
    #     translations = pickle.load(f)

    for i, row in df_events.iterrows():
        # date_str = str(row['التاريخ'])
        date_str = str(row["date"])

        if '2023' not in date_str:
            continue

        # keywords_text = str(row['كلمات مفتاحية']).strip()
        # if keywords_text in ["", "nan"]:
        #     continue
        #
        # names_mod = keywords_text.replace("\"", '')
        # names_mod = re.sub(' +', ' ', names_mod)
        # if names_mod in evenetnames2shorteventnames:
        #     names_mod = evenetnames2shorteventnames[names_mod]
        #
        # names_mod = ' '.join(unique_list(names_mod.split()))
        row_num = str(row["EventIDRowwise"]).split("_")[-1]
        names_mod = str(row["KeywordEventDescriptionEN"]) + f" ({row_num})"


        # category = category2english[str(row['النوع'])]
        category = str(row["EventTypeEN"])
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
            # selected[category][year_week].append(str(row['كلمات مفتاحية']).strip())
            selected[category][year_week].append(names_mod)
        else:
            # selected[category][year_week] = [str(row['كلمات مفتاحية']).strip()]
            selected[category][year_week] = [names_mod]

    # file_name_events = input("Please enter the name of the events dataset: ")
    # df_events = pd.read_excel(file_name_events)

    # added by Dr. Fatima
    # selected['gender']['2023-01'] = ['منصور لبكي']

    categories2events = {}
    for i, row in tqdm(df_events.iterrows(), total=len(df_events)):

        # time_after = row['التاريخ']
        time_after = row['date']

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

        # category = str(row['النوع'])
        # category_en = category2english[category]  # get the english equivalent of the category
        category = str(row['EventTypeAR'])
        category_en = str(row["EventTypeEN"])  # get the english equivalent of the category

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
    # for subdir, dirs, files in os.walk('Volume-FACEBOOK-UPDATEDD/'):
    for subdir, dirs, files in os.walk('Volumesssss/Volume-FACEBOOK-Updated/'):
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
    for subdir, dirs, files in os.walk('Volumesssss/Volume-New (5)/'):
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


    # Calculate the total number of colors needed
    total_colors = sum([len(categories2volumes[cat]) for cat in categories2volumes])

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

    colors = sns.color_palette("colorblind", n_colors=total_colors)

    categories2volumesordered = {k: categories2volumes[k] for k in categories2names}
    categories2colors = {cat: colors[i] for i, cat in enumerate(cats_ordered)}

    # save_dirs2 = '../paper_plots/volume_slab_plots/'
    save_dirs2 = '../paper_plots_stephanie/volume_slab_plots/'
    mkdir(save_dirs2)
    mkdir(save_dirs2)

    plot_volume(categories2volumes=categories2volumesordered, add_slabs=False, plot_in_arabic=False)
    plot_volume(categories2volumes=categories2volumesordered, add_slabs=True, add_regions=False, plot_in_arabic=False)
    # plot_volume(categories2volumes=categories2volumesordered, add_slabs=True, add_regions=True)

    ################
    ########################################################### BAR PLTOS...............................................

    import matplotlib.pyplot as plt

    save_dirs3 = '../paper_plots_stephanie/volume_bar_plots/'
    mkdir(save_dirs3)
    events2names = dict(zip(df_events["EventIDRowwise"], df_events["KeywordEventDescriptionEN"]))
    del events2names[np.nan]
    categories2events2volumes = {}
    for subdir, dirs, files in os.walk('Volumesssss/Volume-FACEBOOK-Updated/'):
    # for subdir, dirs, files in os.walk('Volume-New/'):
        if '-KD' in subdir:
            for file in files:
                if 'E' in file and '2023' in file:
                    df = pd.read_excel(os.path.join(subdir, file), sheet_name='original')
                    print(file)
                    # category = subdir.split('\\')[0].split('/')[1]
                    category = subdir.split('\\')[0].split('/')[-1]
                    if category not in categories2events2volumes:
                        categories2events2volumes[category] = {}
                    comment_cols = [col for col in df.columns if "Comments" in col]
                    total_sum = 0
                    for col in comment_cols:
                        total_sum += df[col].fillna(0).sum()
                    print(total_sum)

                    splitted = file.replace(".xlsx", "").split("-")
                    actual_file_name = "E" + splitted[2] + "-" + splitted[1] + "-" + splitted[0].replace("E", "") + "_" + category
                    print()
                    for k in events2names:
                        if actual_file_name in k:
                            event_name = k
                            break
                    try:
                        rownum = event_name.split("_")[-1]
                        enamedisplay = events2names[event_name] + f"({rownum})"
                        if enamedisplay in categories2events2volumes[category]:
                            categories2events2volumes[category][enamedisplay] += total_sum
                        else:
                            categories2events2volumes[category][enamedisplay] = total_sum
                    except:
                        print(f"{file}")
    for subdir, dirs, files in os.walk('Volumesssss/Volume-New (5)/'):
    # for subdir, dirs, files in os.walk('Volume-New/'):
        if '-KD' in subdir:
            for file in files:
                if 'E' in file and '2023' in file:
                    df = pd.read_excel(os.path.join(subdir, file), sheet_name='weekly')

                    # category = subdir.split('\\')[0].split('/')[1]
                    category = subdir.split('\\')[0].split('/')[-1]
                    if category not in categories2events2volumes:
                        categories2events2volumes[category] = {}
                    comment_cols = [col for col in df.columns if "Comments" in col]
                    total_sum = 0
                    for col in comment_cols:
                        total_sum += df[col].fillna(0).sum()
                    print(total_sum)

                    splitted = file.replace(".xlsx", "").split("-")
                    actual_file_name = "E" + splitted[2] + "-" + splitted[1] + "-" + splitted[0].replace("E", "") + "_" + category
                    print()
                    for k in events2names:
                        if actual_file_name in k:
                            event_name = k
                            break
                    try:
                        rownum = event_name.split("_")[-1]
                        enamedisplay = events2names[event_name] + f"({rownum})"
                        if enamedisplay in categories2events2volumes[category]:
                            categories2events2volumes[category][enamedisplay] += total_sum
                        else:
                            categories2events2volumes[category][enamedisplay] = total_sum
                    except:
                        print(f"{file}")


    # HIYAMMMMMMMMMMM
    for k in events2names:
        category = k.split("_")[1]
        rownum = k.split("_")[-1]
        if str(events2names[k]) in ["nan", ""]:
            continue
        val = str(events2names[k]) + f"({rownum})"
        if val not in categories2events2volumes[category]:
            categories2events2volumes[category][str(val)] = 0

    for category in categories2events2volumes:

        event2comments = categories2events2volumes[category]
        # Sort by total comments
        sorted_events = sorted(event2comments.items(), key=lambda x: x[1], reverse=True)

        event_names = [get_display(arabic_reshaper.reshape(event)) for event, _ in sorted_events]
        comment_counts = [count for _, count in sorted_events]

        # Arabic reshaped + sorted labels
        event_names = [get_display(arabic_reshaper.reshape(event)) for event, _ in sorted_events]
        comment_counts = [count for _, count in sorted_events]

        # Set plot size dynamically
        fig_width = max(8, len(event_names) * 0.3)
        plt.figure(figsize=(fig_width, 6))

        # Plot vertical bars
        plt.bar(event_names, comment_counts, color='skyblue')

        plt.xticks(rotation=90, ha='center')  # Rotate Arabic labels for readability
        plt.ylabel("Total number of comments", fontweight='bold')  # Arabic-friendly label
        # plt.title(get_display(arabic_reshaper.reshape(f"عدد التعليقات لكل حدث - {categories2arabic[category]}")),
        #           fontweight='bold')
        plt.tight_layout()

        # Save
        plt.savefig(os.path.join(save_dirs3, f'{category}.png'), dpi=600)
        plt.close()



        #
        # # Adjust figure size based on number of events
        # fig_height = max(2, len(event_names) * 0.3)
        # plt.figure(figsize=(8, fig_height))
        # plt.barh(event_names, comment_counts, color='steelblue')
        # plt.xlabel("Total Number of Comments", fontweight='bold')
        # title_ar = get_display(arabic_reshaper.reshape(categories2arabic[category]))
        # plt.title(f"Total Comments per Event | {category.capitalize()} | {title_ar}", fontweight='bold')
        # plt.tight_layout()
        # plt.gca().invert_yaxis()
        #
        # plt.savefig(os.path.join(save_dirs3, f'total_comments_per_event_{category}.png'), dpi=600)
        # plt.close()
