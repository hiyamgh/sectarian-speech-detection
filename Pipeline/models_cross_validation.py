from numpy import array
from keras.preprocessing.text import one_hot
from keras.models import Sequential
from keras.layers.core import Dropout, Dense
from keras.layers import  LSTM
from keras.layers import Embedding
from sklearn.model_selection import train_test_split
from keras.preprocessing.text import Tokenizer
from keras.layers import Input
from keras.layers import Concatenate
from keras.layers import Dense, Embedding, GlobalMaxPool1D, Dropout, Conv1D,GRU, Bidirectional, LSTM, Dense
from sklearn.metrics import confusion_matrix, classification_report, fbeta_score
from sklearn.metrics import jaccard_score, label_ranking_average_precision_score, hamming_loss,multilabel_confusion_matrix, f1_score
import numpy as np
import tensorflow as tf
from tensorflow.keras.callbacks import EarlyStopping
import fasttext
import tensorflow as tf
import seaborn as sns
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split
import pandas as pd
from keras.preprocessing.text import Tokenizer
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import matplotlib.pyplot as plt
from keras import backend as K
from sklearn.model_selection import StratifiedKFold



def recall_metric(y_true, y_pred):
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
    recall = true_positives / (possible_positives + K.epsilon())
    return recall

def precision_metric(y_true, y_pred):
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
    precision = true_positives / (predicted_positives + K.epsilon())
    return precision

def f1_metric(y_true, y_pred):
    precision = precision_metric(y_true, y_pred)
    recall = recall_metric(y_true, y_pred)
    return 2 * ((precision * recall) / (precision + recall + K.epsilon()))


def save_classification_report(y_true_categorical, y_pred_categorical, experiment_folder, test_acc, fold, model_name='cnn'):
    classes=['offensive', 'accusation', 'incitement', 'none']
    # predictions=pd.DataFrame(y_pred_categorical)
    report = classification_report(y_true_categorical, y_pred_categorical,target_names=classes, output_dict=True)
    f2_scores = fbeta_score(y_true_categorical, y_pred_categorical, beta=2, average=None)

    class_report_dict = dict()
    for idx, label in enumerate(classes):
        if label not in class_report_dict:
            class_report_dict[label] = dict()
        class_report_dict[label]['f2_score'] = f2_scores[idx]

    report=classification_report(y_true_categorical, y_pred_categorical, target_names=classes, output_dict=True)
    macro_f2 = fbeta_score(y_true_categorical, y_pred_categorical, beta=2, average='macro')
    weighted_f2 = fbeta_score(y_true_categorical, y_pred_categorical, beta=2, average='weighted')

    class_report_dict['macro_f2'] = macro_f2
    class_report_dict['weighted_f2'] = weighted_f2
    precion_avg= label_ranking_average_precision_score(y_true_categorical, y_pred_categorical)
    hamming= hamming_loss(y_true_categorical, y_pred_categorical)
    j_score= jaccard_score(y_true_categorical, y_pred_categorical, average='samples')
    f_score= f1_score(y_true_categorical, y_pred_categorical, average='micro')
    class_report_file_path = os.path.join(experiment_folder, f'classification_report_{model_name}_{fold}.txt')
    with open(class_report_file_path, 'w') as file:
        file.write(classification_report(y_true_categorical, y_pred_categorical, target_names=classes))
        for label, metrics in class_report_dict.items():
            file.write(f'{label}: {metrics}\n')
        file.write("\n")
        file.write(f"Accuracy: {test_acc}\n")
        file.write("\n")
        file.write(f"Label ranking average precision score: {precion_avg}\n")
        file.write("\n")
        file.write(f"Hamming loss:  {hamming}\n")
        file.write("\n")
        file.write(f"Jaccard Score: {j_score}\n")
    return class_report_dict, precion_avg, hamming, j_score,macro_f2,weighted_f2,f_score


def cnn_model_with_cv(max_words, max_sequence_length, tokenizer, x, y, x_test, y_test, embedding_matrix, experiment="experiment0", n_splits=10):
    model_name = "cnn"
    classes=['offensive', 'accusation', 'incitement', 'none']
    experiment_folder = f'model_results/{experiment}/cross_validation/{model_name}'

    if not os.path.exists(experiment_folder):
        os.makedirs(experiment_folder)
    skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)
    all_macro_f2=[]
    all_weighted_f2=[]
    all_precision_avg = []
    all_hamming = []
    all_j_score = []
    all_accuracy=[]
    all_f_score=[]

    for fold, (train_index, test_index) in enumerate(skf.split(x, y.argmax(axis=1))):
        x_train_fold, x_val_fold = x[train_index], x[test_index]
        y_train_fold, y_val_fold = y[train_index], y[test_index]

        es_callback = EarlyStopping(monitor='val_loss', patience=2, restore_best_weights=True)

        model = tf.keras.models.Sequential([
            tf.keras.layers.Embedding(input_dim=max_words, output_dim=300, input_length=max_sequence_length, weights=[embedding_matrix], trainable=False),
            tf.keras.layers.Conv1D(300, 3, padding='valid', activation='relu', strides=1),
            tf.keras.layers.GlobalMaxPooling1D(),
            tf.keras.layers.Dropout(0.32640003830073017),
            tf.keras.layers.Dense(4, activation='sigmoid')
        ])

        epochs = 20
        batch_size = 32
        learning_rate = 0.001
        learning_decay = 0.0001407591818315349
        model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=learning_rate, decay=learning_decay),
                      loss='binary_crossentropy', metrics=['accuracy', f1_metric, precision_metric, recall_metric])

        history = model.fit(x_train_fold, y_train_fold, validation_data=(x_val_fold, y_val_fold), epochs=epochs, batch_size=batch_size, callbacks=[es_callback])

        test_loss, test_acc, f1_m, precision_m, recall_m = model.evaluate(x_test, y_test)
        print(f'Fold {fold + 1} - Test Accuracy, F1, Precision, Recall: {test_acc, f1_m, precision_m, recall_m}')

        predictions = model.predict(x_test)
        threshold = 0.5
        y_pred = (predictions > threshold).astype(int)

        report, precion_avg, hamming, j_score, macro_f2, weighted_f2,f_score = save_classification_report(y_test, y_pred, experiment_folder, test_acc, fold, model_name)

        all_macro_f2.append(macro_f2)
        all_weighted_f2.append(weighted_f2)

        # all_class_reports.append(class_report_dict)
        all_precision_avg.append(precion_avg)
        all_hamming.append(hamming)
        all_j_score.append(j_score)
        all_accuracy.append(test_acc)
        all_f_score.append(f_score)
        model.reset_states()

    mean_precision_avg = np.mean(all_precision_avg)
    mean_hamming = np.mean(all_hamming)
    mean_j_score = np.mean(all_j_score)
    mean_acc = np.mean(all_accuracy)
    mean_f1 = np.mean(all_f_score)
    mean_macro_f2= np.mean(all_macro_f2)
    mean_weighted_f2= np.mean(all_weighted_f2)
    class_report_file_path = os.path.join(experiment_folder, f'mean_report.txt')
    with open(class_report_file_path, 'w') as file:
        file.write(f'Mean Precision Avg across folds: {mean_precision_avg}\n')
        file.write(f'Mean Hamming across folds: {mean_hamming}\n')
        file.write(f'Mean Jaccard Score across folds: {mean_j_score}\n')
        file.write(f'Mean Accuracy Score across folds: {mean_acc}\n')
        file.write(f'Mean F1 Score across folds: {mean_f1}\n')
        file.write(f'Mean Macro F2 Score across folds: {mean_macro_f2}\n')
        file.write(f'Mean Weighted F2 Score across folds: {mean_weighted_f2}\n')

def bilstm_model_with_cv(max_words, max_sequence_length, tokenizer, x, y, x_test, y_test, embedding_matrix, experiment="experiment0", n_splits=10):
    model_name = "bilstm"
    classes=['offensive', 'accusation', 'incitement', 'none']
    experiment_folder = f'model_results/{experiment}/cross_validation/{model_name}'

    if not os.path.exists(experiment_folder):
        os.makedirs(experiment_folder)
    skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)
    all_macro_f2=[]
    all_weighted_f2=[]
    all_precision_avg = []
    all_hamming = []
    all_j_score = []
    all_accuracy=[]
    all_f_score=[]

    for fold, (train_index, test_index) in enumerate(skf.split(x, y.argmax(axis=1))):
        x_train_fold, x_val_fold = x[train_index], x[test_index]
        y_train_fold, y_val_fold = y[train_index], y[test_index]

        es_callback = EarlyStopping(monitor='val_loss', patience=2, restore_best_weights=True)
        model = Sequential()
        model.add(Embedding(input_dim=max_words, output_dim=300, input_length=max_sequence_length, weights=[embedding_matrix],trainable=False))
        model.add(Bidirectional(LSTM(192)))
        model.add(Dropout(0.6806640838065117))
        model.add(Dropout(0.6806640838065117))
        model.add(Dense(64, activation='relu'))
        model.add(Dense(4, activation='sigmoid'))    
            
        epochs = 20
        batch_size = 32
        learning_rate = 0.004094472675776185
        learning_decay=0.005756885196509222
        # model.compile(ooptimizer=tf.keras.optimizers.Adam(learning_rate=learning_rate), loss='categorical_crossentropy', metrics=['accuracy', f1_metric, precision_metric, recall_metric])
        model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=learning_rate, decay=learning_decay), loss='binary_crossentropy', metrics=['accuracy', f1_metric, precision_metric, recall_metric])
        history = model.fit(x_train_fold, y_train_fold, validation_data=(x_val_fold, y_val_fold), epochs=epochs, batch_size=batch_size, callbacks=[es_callback])
        test_loss, test_acc, f1_m, precision_m, recall_m = model.evaluate(x_test, y_test)
        print(f'Fold {fold + 1} - Test Accuracy, F1, Precision, Recall: {test_acc, f1_m, precision_m, recall_m}')

        predictions = model.predict(x_test)
        threshold = 0.5
        y_pred = (predictions > threshold).astype(int)

        report, precion_avg, hamming, j_score, macro_f2, weighted_f2,f_score = save_classification_report(y_test, y_pred, experiment_folder, test_acc, fold, model_name)

        all_macro_f2.append(macro_f2)
        all_weighted_f2.append(weighted_f2)

        # all_class_reports.append(class_report_dict)
        all_precision_avg.append(precion_avg)
        all_hamming.append(hamming)
        all_j_score.append(j_score)
        all_accuracy.append(test_acc)
        all_f_score.append(f_score)
        model.reset_states()

    mean_precision_avg = np.mean(all_precision_avg)
    mean_hamming = np.mean(all_hamming)
    mean_j_score = np.mean(all_j_score)
    mean_acc = np.mean(all_accuracy)
    mean_f1 = np.mean(all_f_score)
    mean_macro_f2= np.mean(all_macro_f2)
    mean_weighted_f2= np.mean(all_weighted_f2)
    class_report_file_path = os.path.join(experiment_folder, f'mean_report.txt')
    with open(class_report_file_path, 'w') as file:
        file.write(f'Mean Precision Avg across folds: {mean_precision_avg}\n')
        file.write(f'Mean Hamming across folds: {mean_hamming}\n')
        file.write(f'Mean Jaccard Score across folds: {mean_j_score}\n')
        file.write(f'Mean Accuracy Score across folds: {mean_acc}\n')
        file.write(f'Mean F1 Score across folds: {mean_f1}\n')
        file.write(f'Mean Macro F2 Score across folds: {mean_macro_f2}\n')
        file.write(f'Mean Weighted F2 Score across folds: {mean_weighted_f2}\n')


def gru_model_with_cv(max_words, max_sequence_length, tokenizer, x, y, x_test, y_test, embedding_matrix, experiment="experiment0", n_splits=10):
    model_name = "gru"
    classes=['offensive', 'accusation', 'incitement', 'none']
    experiment_folder = f'model_results/{experiment}/cross_validation/{model_name}'

    if not os.path.exists(experiment_folder):
        os.makedirs(experiment_folder)
    skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)
    all_macro_f2=[]
    all_weighted_f2=[]
    all_precision_avg = []
    all_hamming = []
    all_j_score = []
    all_accuracy=[]
    all_f_score=[]

    for fold, (train_index, test_index) in enumerate(skf.split(x, y.argmax(axis=1))):
        x_train_fold, x_val_fold = x[train_index], x[test_index]
        y_train_fold, y_val_fold = y[train_index], y[test_index]

        es_callback = EarlyStopping(monitor='val_loss', patience=2, restore_best_weights=True)

        model = Sequential()
        model.add(Embedding(input_dim=max_words, output_dim=300, input_length=max_sequence_length, weights=[embedding_matrix],trainable=False))
        model.add(GRU(192))
        model.add(Dense(64, activation='relu'))
        model.add(Dropout(0.6774177281216083))
        model.add(Dense(64, activation='relu'))
        model.add(Dropout(0.6774177281216083))
        model.add(Dense(64, activation='relu'))
        model.add(Dense(4, activation='sigmoid'))

        epochs = 20
        batch_size = 32
        learning_rate = 0.003214389089277288
        learning_decay= 5.578343165082492e-05

        model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=learning_rate, decay=learning_decay),
                      loss='binary_crossentropy', metrics=['accuracy', f1_metric, precision_metric, recall_metric])

        history = model.fit(x_train_fold, y_train_fold, validation_data=(x_val_fold, y_val_fold), epochs=epochs, batch_size=batch_size, callbacks=[es_callback])

        test_loss, test_acc, f1_m, precision_m, recall_m = model.evaluate(x_test, y_test)
        print(f'Fold {fold + 1} - Test Accuracy, F1, Precision, Recall: {test_acc, f1_m, precision_m, recall_m}')

        predictions = model.predict(x_test)
        threshold = 0.5
        y_pred = (predictions > threshold).astype(int)

        report, precion_avg, hamming, j_score, macro_f2, weighted_f2,f_score = save_classification_report(y_test, y_pred, experiment_folder, test_acc, fold, model_name)

        all_macro_f2.append(macro_f2)
        all_weighted_f2.append(weighted_f2)

        # all_class_reports.append(class_report_dict)
        all_precision_avg.append(precion_avg)
        all_hamming.append(hamming)
        all_j_score.append(j_score)
        all_accuracy.append(test_acc)
        all_f_score.append(f_score)
        model.reset_states()

    mean_precision_avg = np.mean(all_precision_avg)
    mean_hamming = np.mean(all_hamming)
    mean_j_score = np.mean(all_j_score)
    mean_acc = np.mean(all_accuracy)
    mean_f1 = np.mean(all_f_score)
    mean_macro_f2= np.mean(all_macro_f2)
    mean_weighted_f2= np.mean(all_weighted_f2)
    class_report_file_path = os.path.join(experiment_folder, f'mean_report.txt')
    with open(class_report_file_path, 'w') as file:
        file.write(f'Mean Precision Avg across folds: {mean_precision_avg}\n')
        file.write(f'Mean Hamming across folds: {mean_hamming}\n')
        file.write(f'Mean Jaccard Score across folds: {mean_j_score}\n')
        file.write(f'Mean Accuracy Score across folds: {mean_acc}\n')
        file.write(f'Mean F1 Score across folds: {mean_f1}\n')
        file.write(f'Mean Macro F2 Score across folds: {mean_macro_f2}\n')
        file.write(f'Mean Weighted F2 Score across folds: {mean_weighted_f2}\n')



def read_data(experiments_folder):
    x_train = pd.read_excel(os.path.join(experiments_folder, 'x_train.xlsx'))
    x_val = pd.read_excel(os.path.join(experiments_folder, 'x_val.xlsx'))
    x_test = pd.read_excel(os.path.join(experiments_folder, 'x_test.xlsx'))

    y_train = pd.read_excel(os.path.join(experiments_folder, 'y_train.xlsx'))
    y_test = pd.read_excel(os.path.join(experiments_folder, 'y_test.xlsx'))
    y_val = pd.read_excel(os.path.join(experiments_folder, 'y_val.xlsx'))

    return x_train, x_val, x_test, y_train, y_val, y_test

def preprocess_data(x_train, x_val, x_test, max_words=1000000):
    tokenizer = Tokenizer(num_words=max_words)

    tokenizer.fit_on_texts(x_train['cleaned_text'].astype(str))
    
    sequences_train = tokenizer.texts_to_sequences(x_train['cleaned_text'].astype(str))
    sequences_test = tokenizer.texts_to_sequences(x_test['cleaned_text'].astype(str))
    sequences_val = tokenizer.texts_to_sequences(x_val['cleaned_text'].astype(str))

    max_sequence_length = max(
        max(len(seq) for seq in sequences_train),
        max(len(seq) for seq in sequences_test),
        max(len(seq) for seq in sequences_val)
    )

    ft = fasttext.load_model('cc.ar.300.bin')

    embedding_matrix = np.zeros((max_words, 300))

    for word, i in tokenizer.word_index.items():
        if i < max_words:
            embedding_vector = ft.get_word_vector(word)
            if embedding_vector is not None:
                embedding_matrix[i] = embedding_vector

    print("Vocabulary Size:", len(tokenizer.word_index))
    print("Embedding Matrix Shape:", embedding_matrix.shape)
    

    padded_sequences_train = pad_sequences(sequences_train, maxlen=max_sequence_length)
    padded_sequences_test = pad_sequences(sequences_test, maxlen=max_sequence_length)
    padded_sequences_val = pad_sequences(sequences_val, maxlen=max_sequence_length)

    return tokenizer, max_sequence_length, padded_sequences_train, padded_sequences_test, padded_sequences_val,embedding_matrix


def run_experiment(experiments_folder, max_words=10000):
    x_train, x_val, x_test, y_train, y_val, y_test = read_data(experiments_folder)

    tokenizer, max_sequence_length, padded_sequences_train, padded_sequences_test, padded_sequences_val,embedding_matrix = preprocess_data(
        x_train, x_val, x_test,max_words
    )

    x = np.concatenate((padded_sequences_train, padded_sequences_val), axis=0)
    y = np.concatenate((y_train, y_val), axis=0)
    cnn_model_with_cv(
        max_words, max_sequence_length, tokenizer,
        x, y,
        padded_sequences_test, y_test,
        embedding_matrix,
        experiment=experiments_folder
    )
    bilstm_model_with_cv(
        max_words, max_sequence_length, tokenizer,
        x, y,
        padded_sequences_test, y_test,
        embedding_matrix,
        experiment=experiments_folder
    )
    gru_model_with_cv(
        max_words, max_sequence_length, tokenizer,
        x, y,
        padded_sequences_test, y_test,
        embedding_matrix,
        experiment=experiments_folder
    )


if __name__ == '__main__':
    annotators = ['annotator3']
    experiment_types = ['experiment_annotated']
    model_path = 'cc.ar.300.bin'

    if not os.path.exists(model_path):
        fasttext.util.download_model('ar', if_exists='ignore')
    else:
        print(f"The Fasttext embedding model '{model_path}' already exists.")
    for annotator in annotators:
        for experiment_type in experiment_types:
            current_experiment_folder = f'experiments/{annotator}/{experiment_type}'
            run_experiment(current_experiment_folder)
