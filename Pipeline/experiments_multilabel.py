import pandas as pd
from sklearn.model_selection import train_test_split
import os
import re
import string
import numpy as np

def split_data_experiments_annotated_multilabel():

    labels=['offensive','accusation', 'incitement','none' ]
    
    experiments_folder = 'experiments/annotator3/experiment_annotated'

    if not os.path.exists(experiments_folder):
        os.makedirs(experiments_folder)
    current_directory = os.getcwd()

    df_annotated=pd.read_excel("MultiLabel-Annotated.xlsx", dtype=str)
    ################################ ANNOTATOR III DATA ################################
    df=df_annotated
    df = df.dropna(subset=['Annotator III collapsed'])
    df = df.dropna(subset=['cleaned_text'])

    df['cleaned_text']=df['cleaned_text'].astype(str)
    y=df[labels]

    # Perform the train-test split only if the folder is created
    x_train, x_test, y_train, y_test = train_test_split(df, y, test_size=0.2, shuffle=True, stratify=y)
    x_train, x_val, y_train, y_val = train_test_split(x_train, y_train,
                                                  test_size=0.25, shuffle=True)


    x_train['cleaned_text'].to_excel(os.path.join(current_directory, experiments_folder, 'x_train.xlsx'), index=False)
    x_test['cleaned_text'].to_excel(os.path.join(current_directory,experiments_folder, 'x_test.xlsx'), index=False)
    x_val['cleaned_text'].to_excel(os.path.join(current_directory, experiments_folder, 'x_val.xlsx'), index=False)


    y_train.to_excel(os.path.join(current_directory, experiments_folder, 'y_train.xlsx'), index=False)
    y_test.to_excel(os.path.join(current_directory, experiments_folder, 'y_test.xlsx'), index=False)
    y_val.to_excel(os.path.join(current_directory, experiments_folder, 'y_val.xlsx'), index=False)



if __name__ == '__main__':
    split_data_experiments_annotated_multilabel()
