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
en2ar = {v: k for k, v in ar2en.items()}

# df = pd.read_excel('experiments/serving.xlsx')
# for category in list(set(list(df['theme']))):
#
#     for event in list(set(list(df['EventID']))):
#
#         df_sub = df[df['theme'] == category]
#         df_sub = df_sub[df_sub['EventID'] == event]
#
#         if len(df_sub) == 0:
#             continue
#
#         # Calculate the sum of labels for each Final_label
#         label_sums = df_sub['Final_label'].value_counts()
#
#         # Convert the Series to a DataFrame
#         label_sums_df = pd.DataFrame({'Final_label': label_sums.index, 'Count': label_sums.values})
#
#         # Set up the plot
#         fig, ax = plt.subplots(figsize=(10, 6))
#
#         # Define colors for each Final_label
#         colors = sns.color_palette('husl', n_colors=len(label_sums))
#
#         # Create a bar plot
#         bars = ax.bar(label_sums_df['Final_label'], label_sums_df['Count'], color=colors)
#
#         # Set labels and title
#         ax.set_xlabel('Final_label')
#         # ax.set_ylabel('Count')
#         ax.set_title('Barplot of Final_label Sums across all Events')
#
#         # Adjust x-axis ticks
#         ax.set_xticklabels(label_sums.index, rotation=45, ha='right')
#
#         # Set common y-axis label
#         fig.text(0.04, 0.5,
#                  'Cumulative Class Distribution | {}'.format(get_display(arabic_reshaper.reshape('تصنيف الخطاب'))),
#                  va='center', rotation='vertical', fontsize='medium')
#
#         # Create legend
#         legend_labels = label_sums_df['Final_label'].to_list()
#         legend_handles = [plt.Rectangle((0, 0), 1, 1, color=colors[i]) for i in range(len(legend_labels))]
#         ax.legend(legend_handles, legend_labels, loc='upper right')
#
#         # Show the plot
#         plt.savefig('serving_plots_events/{}-{}.png'.format(ar2en[category], event))
#         plt.close()


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

dictionary = dict(zip(dates_new, names))

# df = pd.read_excel('serving.xlsx')
# df = pd.read_excel('serving_collapsed.xlsx')
file_location = input("Please enter the name of the serving file [this assumes its in the same directory] ")
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

color_palette = sns.color_palette('husl', n_colors=len(df_orig['Final_label'].unique()))
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


# ################################################### Serving percentages as requested by Dr. Fatima ###################################################
with open('statistics.txt', 'w', encoding='utf-8') as f:
    final_labels_unique = list(set(list(df_orig['Final_label'])))
    for category in tqdm(list(set(list(df_orig['theme'])))):

        df_sub = df_orig[df_orig['theme'] == f'{category}']
        category_en = ar2en[category]

        f.write('CATEGORY: {} ###################################################### \n\n'.format(category_en))

        df_sub_annotated = df_sub[df_sub['Annotated-Served'] == 'annotated']
        total_annotated = len(df_sub_annotated)

        df_sub_served = df_sub[df_sub['Annotated-Served'] == 'served']
        total_served = len(df_sub_served)

        f.write('Annotated \t\t Served\nTOTAL COMMENTS: {} \t\t {}\n'.format(total_annotated, total_served))
        for label in final_labels_unique:
            df_label_annotated = df_sub_annotated[df_sub_annotated['Final_label'] == label]
            total_label_annotated = len(df_label_annotated)
            total_label_annotated_p = len(df_label_annotated)/total_annotated * 100

            df_label_served = df_sub_served[df_sub_served['Final_label'] == label]
            total_label_served = len(df_label_served)
            total_label_served_p = len(df_label_served) / total_served * 100

            f.write('{}: {:.2f}% - {}\t\t {:.2f}% - {}\n'.format(label, total_label_annotated_p, total_label_annotated, total_label_served_p, total_label_served))
        f.write('\n\n')
f.close()

# ##################################################### Serving percentages as requested by Dr. Fatima ###################################################


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
            fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(8, 8),
                                     gridspec_kw={'top': 0.85, 'bottom': 0.1, 'hspace': 0.5})

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

                # label_counts = subset_df['Final_label'].value_counts()
                # print(label_counts)
                # print('len of df_sub: {}'.format(len(df_sub)))
                #
                # labels = list(label_counts.index)
                # counts = list(label_counts.values)
                #
                # print(labels, counts)

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
                                         fontweight='bold', pad=15,
                                         y=1.02)  # Adjust the pad parameter for title spacing
                # axes[row, col].set_ylabel('Count')

                # Adjust x-axis ticks
                axes[row, col].set_xticks(labels)
                axes[row, col].set_xticklabels(labels, rotation=45, fontsize='small')

                max_y_value = max(max_y_value, max(counts))


            fig.text(0.02, 0.5, 'Class Distribution under {} | {}'.format(category_en, get_display(
                arabic_reshaper.reshape('تصنيف الخطاب تحت خانة ال{}'.format(category_ar)))), ha='center', va='center',
                     rotation='vertical', fontsize='medium')

            print(plt.get_fignums())

            # print(df['Final_label'].unique())

            colors = [color_palette[j] for j, _ in enumerate(labels_original)]

            # labels_curr = ['{} | {}'.format(l, get_display(arabic_reshaper.reshape(labels2ar[l]))) for l in labels_original]
            labels_curr = ['{} | {}'.format(l, labels_original_ar[l]) for l in labels_original]
            legend_handles = [
                plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=color, markersize=10, label=f'{labels_curr[i]}')
                for i, color in enumerate(colors)
            ]

            plt.subplots_adjust(top=0.75)
            fig.legend(handles=legend_handles, loc='upper center',
                       bbox_to_anchor=(0.5, 0.95),
                       ncol=4)
            plt.tight_layout()

            # fig = plt.gcf()
            # fig.set_size_inches(8, 6)

            fig = plt.gcf()
            fig.set_size_inches(16, 16)

            # Adjust layout with more space between subplots
            hspace_factor = 0.3  # Adjust this factor as needed
            plt.subplots_adjust(hspace=hspace_factor / nrows, wspace=0.3, top=3.5)
            # plt.subplots_adjust(hspace=1.01, top=0.9, bottom=0.15)  # Increase the top parameter

            # save_dir2 = '../paper_plots/serving_barplots/'

            save_dir = 'Volume_Results_latest_latest/Volume/{}/Total-KD/'.format(category_en)
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)
            # if not os.path.exists(save_dir2):
            #     os.makedirs(save_dir2)

            plt.savefig(os.path.join(save_dir, 'BarPlotServing_{}_{}.png'.format(category_en, LABEL)), dpi=300)
            # plt.savefig(os.path.join(save_dir2, '{}_{}.png'.format(category_en, LABEL)), dpi=600)
            # plt.savefig('Volume_Results/Volume/{}/Total-KD/BarPlotServing_{}_{}.png'.format(category_en, category_en, LABEL), dpi=300)
            plt.close()

with open('statistics_detailed.txt', 'w', encoding='utf-8') as f:
    for LABEL in stats:
        f.write('=========================================================== {} ===========================================================\n\n'.format(LABEL))
        for category in stats[LABEL]:
            f.write('UNDER {} ////////////////////////////////////////////////////////\n\n'.format(category))
            for event in stats[LABEL][category]:
                f.write('EVENT {}\n'.format(event))
                for label, count in stats[LABEL][category][event].items():
                    f.write('{} - {}\n'.format(label, count))
                f.write('\n\n')
            f.write('////////////////////////////////////////////////////////\n\n'.format(category))
        f.write('======================================================================================================================\n\n'.format(LABEL))
f.close()