import pandas as pd
import matplotlib.pyplot as plt
import math
import arabic_reshaper
from bidi.algorithm import get_display
import seaborn as sns
from datetime import datetime
from tqdm import tqdm
import os
import matplotlib.patches as mpatches
import re

font_family = "Arial"  # Change this to "Helvetica" if you prefer Helvetica
plt.rcParams['font.family'] = font_family
plt.rcParams['font.size'] = 8  # Set the desired default font size (change 12 to your preferred size)
plt.rcParams['text.antialiased'] = False
plt.rcParams['text.hinting'] = False
plt.rcParams['lines.dash_capstyle'] = 'butt'  # or 'round'
plt.rcParams['legend.fontsize'] = 8  # Set the legend font size

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

ar2en = {
        # 'عنصري': 'racist',
        'فساد': 'corruption',
        'جندري': 'gender',
        'جنساني': 'sexuality',
        # 'جنسي': 'sexuality',
        'ديني': 'religion',
        'سياسة وأمن': 'politics and security',
        'لجوء': 'refugee'
    }

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

en2ar = {v: k for k, v in ar2en.items()}

df_selected = pd.read_excel('2023-Selected.xlsx')

dates = list(df_selected['التاريخ'])[:35]
dates_new = []
for d in dates:
    d = str(d)
    try:
        date_dt = datetime.strptime(d[:10], '%Y-%m-%d').strftime('%d-%m-%Y')
    except:

        date_dt = datetime.strptime(d[:10], '%Y-%d-%m').strftime('%d-%m-%Y')

    dates_new.append('E{}'.format(date_dt))

names = list(df_selected['كلمات مفتاحية'])[:35]
names = [n.replace("\"", '') for n in names]
names_new = []
for n in names:
    names_mod = n.replace("\"", '')
    names_mod = re.sub(' +', ' ', names_mod)
    if names_mod in evenetnames2shorteventnames:
        print(f'{names_mod} replaced with {evenetnames2shorteventnames[names_mod]}')
        names_mod = evenetnames2shorteventnames[names_mod]

    names_mod = ' '.join(unique_list(names_mod.split()))
    names_new.append(names_mod)

# names = names_new


dictionary = dict(zip(dates_new, names_new))

# df = pd.read_excel('serving.xlsx')
# df = pd.read_excel('serving_collapsed.xlsx')
file_location = input("Please enter the name of the serving file [this assumes its in the same directory] ")
# language_legend = input("Please enter the language used in the legend: ")
df = pd.read_excel('{}'.format(file_location))

df_orig = df.replace({'Final_label_offensive': 'offensive',
                 'Final_label_accusation': 'accusation',
                 'Final_label_incitement': 'incitement',
                 'Final_label_none': 'none'})

# EXTRA
df_orig = df_orig[df_orig['Final_label'].notna()]
# END OF EXTRA

# EXTRA - Does not make sense to have none and another label
labels_updated = []
for i, row in df_orig.iterrows():
    l = str(row['Final_label']).strip()
    if 'none,' in l:
        lnew = l.replace('none,', '')
        labels_updated.append(lnew)
    elif 'none, ' in l:
        lnew = l.replace('none, ', '')
        labels_updated.append(lnew)

    elif ',none' in l:
        lnew = l.replace(',none', '')
        labels_updated.append(lnew)
    elif ', none' in l:
        lnew = l.replace(', none', '')
        labels_updated.append(lnew)

    else:
        labels_updated.append(l)

df_orig['Final_label'] = labels_updated
# END OF EXTRA

# color_palette = sns.color_palette('husl', n_colors=len(df_orig['Final_label'].unique()))
color_palette = sns.color_palette("colorblind", n_colors=len(df_orig['Final_label'].unique()))

# labels_original = ['offensive', 'none', 'incitement', 'accusation']
labels_original = list(df_orig['Final_label'].unique())
colors = [color_palette[j] for j, _ in enumerate(labels_original)]
label2color = {}
for z, label in enumerate(labels_original):
    label2color[label] = colors[z]

labels2ar = {
        'offensive': 'تجريح وكراهية',
        'accusation': 'تخوين واتهام',
        'incitement': 'تحريض',
        'none': 'لا شيء مما سبق'
    }

# extra
labels_original_ar = {}
for l in labels_original:
    lsub = l.strip().split(',')
    lsub = [s.strip() for s in lsub]
    s = ''
    for lsubsub in lsub:
        ld = get_display(arabic_reshaper.reshape(labels2ar[lsubsub]))
        if s != '':
            s += ', {}'.format(ld)
        else:
            s += '{}'.format(ld)
    labels_original_ar[l] = s
#  end of extra


stats = {}

for LABEL in ['annotated', 'served']:
    df_annserv = df_orig[df_orig['Annotated-Served'] == f'{LABEL}']

    stats[LABEL] = {}

    for category in tqdm(list(set(list(df_annserv['theme'])))):
            j = 1

            print(category)
            category_en = ar2en[category]
            category_ar = category

            stats[LABEL][category_en] = {}

            # for event in list(set(list(df['EventID']))):
            df_sub = df_annserv[df_annserv['theme'] == category]
            # df_sub = df_sub[df_sub['EventID'] == event]

            if len(df_sub) == 0:
                continue

            # Get unique EventIDs
            event_ids = df_sub['EventID'].unique()

            # Calculate the number of rows and columns
            n_subplots = len(event_ids)
            nrows = int(math.sqrt(n_subplots))
            ncols = math.ceil(n_subplots / nrows)

            # Set up subplots
            # fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(8, 8),
            #                          gridspec_kw={'top': 0.85, 'bottom': 0.1, 'hspace': 0.5})

            fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(5, 5),
                                     gridspec_kw={'top': 0.9, 'bottom': 0.01, 'hspace': 0.9})

            if len(axes.shape) == 1:
                axes = axes.reshape(1, -1)
            k = 0
            for i in range(nrows):
                for j in range(ncols):
                    if k >= n_subplots:
                        axes[i, j].set_visible(False)  # Turn off visibility for the specific subplot
                    k += 1

            # color_palette = sns.color_palette('husl', n_colors=len(df['Final_label'].unique()))
            # legend_patches = [mpatches.Patch(color=color, label=label) for label, color in
            #                   zip(df['Final_label'].unique(), color_palette)]

            max_y_value = 0

            legend_labels = []  # Store legend labels

            # Loop through each event and create a grouped barplot
            for i, event_id in enumerate(event_ids):
                # if event_id == 'E05-10-2023' and category == 'فساد':
                #     print()
                row, col = divmod(i, ncols)  # Calculate the row and column index
                print('row: {}, col: {}'.format(row, col))
                subset_df = df_sub[df_sub['EventID'] == event_id]

                labels2counts = {}
                for z, rowz in subset_df.iterrows():
                    # final_labels = str(rowz['Final_label']).strip().split(',')
                    final_labels = str(rowz['Final_label']).strip()
                    # final_labels = [l.strip() for l in final_labels]
                    # for label in final_labels:
                    if final_labels not in labels2counts:
                        labels2counts[final_labels] = 1
                    else:
                        labels2counts[final_labels] += 1

                labels = list(labels2counts.keys())
                counts = list(labels2counts.values())

                stats[LABEL][category_en][dictionary[event_id]] = labels2counts

                # Assign different colors to bars
                # colors = [color_palette[j] for j, _ in enumerate(labels)]
                try:
                    colors = [label2color[l] for l in labels if l in label2color]
                except:
                    print(label2color)
                bars = axes[row, col].bar(labels, counts, color=colors)
                print(bars)
                legend_labels.append(bars[0])  # Add the first bar of each plot to the legend labels
                # axes[row, col].bar(labels, counts, color=colors)
                axes[row, col].set_title(f'{get_display(arabic_reshaper.reshape(dictionary[event_id]))}',
                                         fontsize='small',
                                         fontweight='bold',
                                         # pad=15,
                                         y=1.0001)  # Adjust the pad parameter for title spacing
                # axes[row, col].set_ylabel('Count')

                # # Adjust x-axis ticks
                # axes[row, col].set_xticks(labels)
                # axes[row, col].set_xticklabels(labels, rotation=45, fontsize='small')
                axes[row, col].set_xticks([])
                axes[row, col].set_xticklabels([])  # Clear the x-axis labels

                max_y_value = max(max_y_value, max(counts))


            # fig.text(0.02, 0.5, 'Class Distribution under {} | {}'.format(category_en, get_display(
            #     arabic_reshaper.reshape('تصنيف الخطاب تحت خانة ال{}'.format(category_ar)))), ha='center', va='center',
            #          rotation='vertical', fontsize='medium')

            print(plt.get_fignums())

            # print(df['Final_label'].unique())

            colors = [color_palette[j] for j, _ in enumerate(labels_original)]

            # labels_curr = ['{} | {}'.format(l, get_display(arabic_reshaper.reshape(labels2ar[l]))) for l in labels_original]

            # labels_curr = ['{} | {}'.format(l, labels_original_ar[l]) for l in labels_original]
            # if language_legend == "english":
            #     labels_curr = ['{}'.format(l) for l in labels_original]
            # else:
            #     labels_curr = ['{}'.format(labels_original_ar[l]) for l in labels_original]
            #
            # legend_handles = [
            #     plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=color,
            #                markersize=5,
            #                label=f'{labels_curr[i]}')
            #     for i, color in enumerate(colors)
            # ]


            # plt.subplots_adjust(top=0.75)
            # fig.legend(handles=legend_handles, loc='upper center',
            #            bbox_to_anchor=(0.5, 0.98),
            #            fontsize='x-small',
            #            ncol=4)

            # # plt.subplots_adjust(top=0.92)
            # fig.legend(handles=legend_handles, loc='upper center',
            #            bbox_to_anchor=(0.5, -0.05),
            #            fontsize='x-small',
            #            ncol=4)

            plt.tight_layout()

            # fig = plt.gcf()
            # fig.set_size_inches(8, 6)

            fig = plt.gcf()
            fig.set_size_inches(fig_width_inches, fig_height_inches)

            # Adjust layout with more space between subplots
            hspace_factor = 0.38  # Adjust this factor as needed
            if category_en in ['religion']:
                plt.subplots_adjust(hspace=hspace_factor / nrows, wspace=0.95, top=6)
            elif category_en in ['corruption']:
                plt.subplots_adjust(hspace=hspace_factor / nrows, wspace=1.1, top=6)
            else:
                plt.subplots_adjust(hspace=hspace_factor / nrows, wspace=0.6, top=6)
            # plt.subplots_adjust(hspace=1.01, top=0.9, bottom=0.15)  # Increase the top parameter

            save_dir2 = '../paper_plots/serving_barplots/'
            if not os.path.exists(save_dir2):
                os.makedirs(save_dir2)

            plt.savefig(os.path.join(save_dir2, '{}_{}.png'.format(category_en, LABEL)), dpi=600)
            plt.close()


            for lang in ["english", "arabic"]:
                if lang == "english":
                    labels_curr = ['{}'.format(l) for l in labels_original]
                else:
                    labels_curr = ['{}'.format(labels_original_ar[l]) for l in labels_original]

                legend_handles = [
                    plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=color,
                               markersize=5,
                               label=f'{labels_curr[i]}')
                    for i, color in enumerate(colors)
                ]

                # Create an empty plot
                fig_legend, ax_legend = plt.subplots()

                # Add a legend
                ax_legend.legend(handles=legend_handles, loc='upper center', bbox_to_anchor=(0.5, 1.15), ncol=2)
                ax_legend.axis('off')

                fig_legend.set_size_inches(fig_width_inches, fig_height_inches / 3)

                # Display the plot
                plt.savefig(os.path.join(save_dir2, '{}_{}_{}_legend.png'.format(category_en, LABEL, lang)), dpi=600)
                plt.close()