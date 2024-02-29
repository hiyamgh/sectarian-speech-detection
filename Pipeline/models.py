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
from sklearn.metrics import jaccard_score, label_ranking_average_precision_score, hamming_loss,multilabel_confusion_matrix
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


def plot_learning_curve(history, experiment_name, model_name=''):
    plt.figure(figsize=(10, 6))
    # Plot training & validation accuracy values
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('Model loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend(['Train', 'Validation'], loc='upper left')
    plt.grid(True)
    experiment_folder = f'plots/{experiment_name}'
    if not os.path.exists(experiment_folder):
        os.makedirs(experiment_folder)
    figure_path = os.path.join(experiment_folder, f'learning_curve_{model_name}.png')
    plt.savefig(figure_path, dpi=600)
    print(f'Learning curve saved at: {figure_path}')

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


def save_classification_report(y_true_categorical, y_pred_categorical, experiment_folder, test_acc, model_name='cnn'):
    classes=['offensive', 'accusation', 'incitement', 'none']
    predictions=pd.DataFrame(y_pred_categorical)
    predictions.to_excel(f"{experiment_folder}/predicted_{model_name}.xlsx", index=False)
    report = classification_report(y_true_categorical, y_pred_categorical,target_names=classes, output_dict=True)
    f2_scores = fbeta_score(y_true_categorical, y_pred_categorical, beta=2, average=None)

    class_report_dict = dict()
    for idx, label in enumerate(classes):
        if label not in class_report_dict:
            class_report_dict[label] = dict()
        class_report_dict[label]['f2_score'] = f2_scores[idx]


    macro_f2 = fbeta_score(y_true_categorical, y_pred_categorical, beta=2, average='macro')
    weighted_f2 = fbeta_score(y_true_categorical, y_pred_categorical, beta=2, average='weighted')

    class_report_dict['macro_f2'] = macro_f2
    class_report_dict['weighted_f2'] = weighted_f2
    precion_avg= label_ranking_average_precision_score(y_true_categorical, y_pred_categorical)
    hamming= hamming_loss(y_true_categorical, y_pred_categorical)
    j_score= jaccard_score(y_true_categorical, y_pred_categorical, average='samples')

    class_report_file_path = os.path.join(experiment_folder, f'classification_report_{model_name}.txt')
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

def update_serving(model, tokenizer,experiment,model_name,threshold=0.5):
    new_data = pd.read_excel("serving-multilabel.xlsx")
    new_data.dropna(subset=['cleaned_text'], inplace=True)
    sequences_new_data= tokenizer.texts_to_sequences(new_data['cleaned_text'].astype(str))
    max_sequence_length =  max(len(seq) for seq in sequences_new_data)
    padded_sequences_new_data = pad_sequences(sequences_new_data, maxlen=max_sequence_length)
    predictions_serving = model.predict(padded_sequences_new_data)
    predictions_serving= (predictions_serving > threshold).astype(int)
    y_pred_categorical = pd.DataFrame(predictions_serving, columns=['offensive', 'accusation', 'incitement', 'none'])
    y_pred_labels = y_pred_categorical.apply(lambda row: ', '.join(row.index[row == 1]), axis=1)
    new_data[f'{model_name}_{experiment}']=y_pred_labels
    new_data.to_excel("serving-multilabel.xlsx", index=False)

def cnn_model(max_words, max_sequence_length, tokenizer, x_train, y_train, x_test, y_test, x_val,y_val,embedding_matrix, experiment="experiment0"):
    model_name="cnn"
    es_callback = EarlyStopping(monitor='val_loss', patience=2,restore_best_weights=True)

    model = tf.keras.models.Sequential([
        tf.keras.layers.Embedding(input_dim=max_words, output_dim=300, input_length=max_sequence_length, weights=[embedding_matrix],trainable=False),
        tf.keras.layers.Conv1D(300, 3, padding='valid', activation='relu', strides=1),
        tf.keras.layers.GlobalMaxPooling1D(),
        tf.keras.layers.Dropout(0.32640003830073017),
        tf.keras.layers.Dense(4, activation='sigmoid')
    ])

    epochs = 20
    batch_size = 32
    learning_rate = 0.001
    learning_decay=0.0001407591818315349
    # model.compile(ooptimizer=tf.keras.optimizers.Adam(learning_rate=learning_rate), loss='categorical_crossentropy', metrics=['accuracy', f1_metric, precision_metric, recall_metric])
    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=learning_rate, decay=learning_decay), loss='binary_crossentropy', metrics=['accuracy', f1_metric, precision_metric, recall_metric])

    history=model.fit(x_train, y_train, epochs=epochs, validation_data=(x_val, y_val), batch_size=batch_size, callbacks=[es_callback])

    test_loss, test_acc, f1_m, precision_m, recall_m = model.evaluate(x_test, y_test)
    print(f'Test Accuracy , "F1", "Precision", "Recall": {test_acc,f1_m, precision_m, recall_m}')

    predictions = model.predict(x_test)
    threshold = 0.5
    y_pred = (predictions > threshold).astype(int)

    experiment_folder = f'model_results/{experiment}'
    
    if not os.path.exists(experiment_folder):
        os.makedirs(experiment_folder)
    save_classification_report(y_test, y_pred, experiment_folder,test_acc, model_name)
    plot_learning_curve(history, f'{experiment}', model_name)
    # update_serving(model, tokenizer,experiment,model_name,threshold=0.5)




def bilstm_model(max_words, max_sequence_length, tokenizer, x_train, y_train, x_test, y_test, x_val,y_val, embedding_matrix,experiment="experiment0"):
    model_name="bilstm"
    es_callback = EarlyStopping(monitor='val_loss', patience=2,restore_best_weights=True)
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

    history=model.fit(x_train, y_train, epochs=epochs, validation_data=(x_val, y_val), batch_size=batch_size, callbacks=[es_callback])

    test_loss, test_acc, f1_m, precision_m, recall_m = model.evaluate(x_test, y_test)

    print(f'Test Accuracy , "F1", "Precision", "Recall": {test_acc,f1_m, precision_m, recall_m}')

    predictions = model.predict(x_test)
    threshold = 0.5
    y_pred = (predictions > threshold).astype(int)

    experiment_folder = f'model_results/{experiment}'
    
    if not os.path.exists(experiment_folder):
        os.makedirs(experiment_folder)
    save_classification_report(y_test, y_pred, experiment_folder, test_acc, model_name)
    plot_learning_curve(history, f'{experiment}', model_name)
    # update_serving(model, tokenizer,experiment,model_name,threshold=0.5)

def gru_model(max_words, max_sequence_length, tokenizer, x_train, y_train, x_test, y_test, x_val, y_val,embedding_matrix, experiment="experiment0"):
    model_name="gru"
    es_callback = EarlyStopping(monitor='val_loss', patience=2,restore_best_weights=True)

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

    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=learning_rate, decay=learning_decay), loss='binary_crossentropy', metrics=['accuracy', f1_metric, precision_metric, recall_metric])

    history=model.fit(x_train, y_train, epochs=epochs, validation_data=(x_val, y_val), batch_size=batch_size, callbacks=[es_callback])

    test_loss, test_acc, f1_m, precision_m, recall_m = model.evaluate(x_test, y_test)
    print(f'Test Accuracy , "F1", "Precision", "Recall": {test_acc,f1_m, precision_m, recall_m}')

    predictions = model.predict(x_test)
    threshold = 0.5
    y_pred = (predictions > threshold).astype(int)

    experiment_folder = f'model_results/{experiment}'
    
    if not os.path.exists(experiment_folder):
        os.makedirs(experiment_folder)
    save_classification_report(y_test, y_pred, experiment_folder, test_acc, model_name)
    plot_learning_curve(history, f'{experiment}', model_name)
    # update_serving(model, tokenizer,experiment,model_name,threshold=0.5)

def plot(values, experiment, title):
    # values = pd.get_dummies(values).idxmax(axis=1)
    
    labels_histogram = values.sum()

    plt.figure(figsize=(10, 6))  # Adjust the figsize as needed
    ax = labels_histogram.plot(kind='bar', color='skyblue')

    plt.title(title)
    plt.xlabel('Labels')
    plt.ylabel('Count')

    # Adjust the layout and rotation of x-axis labels
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, horizontalalignment='right')
    plt.tight_layout()
    figure_folder = "plots/" + experiment
    if not os.path.exists(figure_folder):
        os.makedirs(figure_folder)

    figure_path = os.path.join(figure_folder, f'{title}_histogram.png')
    plt.savefig(figure_path, dpi=600)  # Adjust the dpi as needed
    # plt.show()

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

def plot_labels_distribution(y_train, y_test, y_val, experiments_folder):
    plot(y_train, experiments_folder, "Train Labels Distribution")
    plot(y_test, experiments_folder, "Test Labels Distribution")
    plot(y_val, experiments_folder, "Validation Labels Distribution")

# Assuming you have a cnn_model function defined
def run_experiment(experiments_folder, max_words=10000):
    x_train, x_val, x_test, y_train, y_val, y_test = read_data(experiments_folder)

    tokenizer, max_sequence_length, padded_sequences_train, padded_sequences_test, padded_sequences_val,embedding_matrix = preprocess_data(
        x_train, x_val, x_test,max_words
    )

    plot_labels_distribution(y_train, y_test, y_val, experiments_folder)
    cnn_model(
        max_words, max_sequence_length, tokenizer,
        padded_sequences_train, y_train,
        padded_sequences_test, y_test,
        padded_sequences_val, y_val,
        embedding_matrix,
        experiment=experiments_folder
    )
    bilstm_model(
        max_words, max_sequence_length, tokenizer,
        padded_sequences_train, y_train,
        padded_sequences_test, y_test,
        padded_sequences_val, y_val,
        embedding_matrix,
        experiment=experiments_folder
    )
    gru_model(
        max_words, max_sequence_length,  tokenizer,
        padded_sequences_train, y_train,
        padded_sequences_test, y_test,
        padded_sequences_val, y_val,
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
