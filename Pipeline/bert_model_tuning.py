import numpy as np
import pandas as pd
from transformers import BertTokenizer
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from transformers import BertForSequenceClassification
from torch.optim import Adam
from sklearn.metrics import  confusion_matrix, classification_report, fbeta_score
import matplotlib.pyplot as plt
from tqdm import tqdm
import os
from sklearn.metrics import classification_report, confusion_matrix, multilabel_confusion_matrix, f1_score, accuracy_score
from torch.nn import BCEWithLogitsLoss, BCELoss
from tqdm import tqdm, trange
from sklearn.metrics import jaccard_score, label_ranking_average_precision_score, hamming_loss,multilabel_confusion_matrix
from transformers import BertModel, BertTokenizer, AdamW, get_linear_schedule_with_warmup

import ray
from ray import tune
from ray.tune.schedulers import ASHAScheduler
import os
#os.environ["RAY_AIR_NEW_OUTPUT"] = "0"
class Tweet(Dataset):
  def __init__(self, text, label, tokenizer, max_len):
    self.text = text
    self.label = label
    self.tokenizer = tokenizer
    self.max_len = max_len
  def __len__(self):
    return len(self.text)
  def __getitem__(self, item):
    text = str(self.text[item])
    label = self.label[item]
    encoding = self.tokenizer.encode_plus(
                text,
                add_special_tokens=True,
                max_length=self.max_len,
                return_token_type_ids=False,
                pad_to_max_length=True,
                return_attention_mask=True,
                return_tensors='pt')
    return {
    'tweet_text': text,
      'input_ids': encoding['input_ids'].flatten(),
      'attention_mask': encoding['attention_mask'].flatten(),
      'labels': torch.tensor(label, dtype=torch.long)
    }

def load_data(folder_path, target_list):

    x_train = pd.read_excel(r'C:/Users/am174/Desktop/Twitter/experiments/annotator3/experiment_annotated/x_train.xlsx')
    y_train = pd.read_excel(r'C:/Users/am174/Desktop/Twitter/experiments/annotator3/experiment_annotated/y_train.xlsx')

    x_test = pd.read_excel(r'C:/Users/am174/Desktop/Twitter/experiments/annotator3/experiment_annotated/x_test.xlsx')
    y_test = pd.read_excel(r'C:/Users/am174/Desktop/Twitter/experiments/annotator3/experiment_annotated/y_test.xlsx')

    x_val = pd.read_excel(r'C:/Users/am174/Desktop/Twitter/experiments/annotator3/experiment_annotated/x_val.xlsx')
    y_val = pd.read_excel(r'C:/Users/am174/Desktop/Twitter/experiments/annotator3/experiment_annotated/y_val.xlsx')

    df_train = pd.concat([x_train, y_train], axis=1)
    df_test = pd.concat([x_test, y_test], axis=1)
    df_val = pd.concat([x_val, y_val], axis=1)

    df_train['full_text']=df_train['cleaned_text']
    df_val['full_text']= df_val['cleaned_text']
    df_test['full_text']= df_test['cleaned_text']

    df_train['one_hot_labels'] = list(df_train[target_list].values)
    df_val['one_hot_labels'] = list(df_val[target_list].values)
    df_test['one_hot_labels'] = list(df_test[target_list].values)

    # Return the necessary dataframes
    return df_train, df_val, df_test

def create_data_loader(data, tokenizer, max_len, batch_size):
    # Your existing code for creating data loaders
    ds = Tweet(
        text=data.full_text.to_numpy(),
        label=data.one_hot_labels.to_numpy(),
        tokenizer=tokenizer,
        max_len=max_len)
    return DataLoader(
    ds,
    batch_size=batch_size)

def save_classification_report(y_true_categorical, y_pred_categorical, experiment_folder, model_name='bert'):
    classes=['offensive', 'accusation', 'incitement', 'none']
    predictions=pd.DataFrame(y_pred_categorical)
    predictions.to_excel(f"{experiment_folder}/predicted_{model_name}.xlsx", index=False)
    report = classification_report(y_true_categorical, y_pred_categorical, output_dict=True)
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
        file.write(classification_report(y_true_categorical, y_pred_categorical))
        for label, metrics in class_report_dict.items():
            file.write(f'{label}: {metrics}\n')
        file.write(f"Label ranking average precision score: {precion_avg}\n")
        file.write(f"Hamming loss:  {hamming}\n")
        file.write(f"Jaccard Score: {j_score}\n")

def update_serving(model,tokenizer,MAX_LENGTH, experiment, device, target_list, model_name="bert"):
    new_data = pd.read_excel("serving-multilabel.xlsx")
    new_data.dropna(subset=['cleaned_text'], inplace=True)
    
    predictions=[]
    for text in tqdm(new_data.text):
      encoded_review = tokenizer.encode_plus(text,max_length=MAX_LENGTH,add_special_tokens=True,
                                              return_token_type_ids=False,pad_to_max_length=True,return_attention_mask=True,
                                              return_tensors='pt')
      input_ids = encoded_review['input_ids'].to(device)
      attention_mask = encoded_review['attention_mask'].to(device)
      output = model(input_ids, attention_mask)
      logits = output[0]
      preds = torch.sigmoid(logits)
      pred_label = preds.cpu().detach().numpy()

      pred_bools = (np.where(pred_label > 0.5, 1, 0)).astype(int)
      predictions.append(pred_bools)
    predictions = np.array(predictions).reshape(-1, 4)  # Reshape to 2D array
    y_pred_categorical = pd.DataFrame(predictions, columns=['offensive', 'accusation', 'incitement', 'none'])
    y_pred_labels = y_pred_categorical.apply(lambda row: ', '.join(row.index[row == 1]), axis=1)
    new_data[f'{model_name}_{experiment}'] = y_pred_labels
    new_data.to_excel("serving-multilabel.xlsx", index=False)

def train_epoch(model,data_loader,optimizer,device,target_list):
    model = model.train()
    losses = []
    tr_true_labels, tr_pred_labels=[],[]
    correct_predictions = 0
    for d in data_loader:

        input_ids = d["input_ids"].to(device)
        attention_mask = d["attention_mask"].to(device)
        targets = d["labels"].to(device)
        optimizer.zero_grad()

        outputs = model(input_ids=input_ids,attention_mask=attention_mask)

        logits = outputs[0]
        preds = torch.sigmoid(logits)

        loss_func = BCEWithLogitsLoss()
        loss = loss_func(logits.view(-1,len(target_list)),targets.type_as(logits).view(-1,len(target_list))) #convert labels to float for calculation

        tr_true_labels.append(targets)
        tr_pred_labels.append(preds)

        losses.append(loss.item())
        loss.backward()
        nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
        optimizer.step()
        # scheduler.step()
        


    tr_pred_labels = torch.cat(tr_pred_labels, dim=0)
    tr_true_labels = torch.cat(tr_true_labels, dim=0)

    tr_pred_labels=tr_pred_labels.cpu().detach().numpy()
    tr_true_labels=tr_true_labels.cpu().detach().numpy()

    tr_pred_labels = [item for sublist in tr_pred_labels for item in sublist]
    tr_true_labels = [item for sublist in tr_true_labels for item in sublist]

    threshold = 0.50
    pred_bools = [pl>threshold for pl in tr_pred_labels]
    true_bools = [tl==1 for tl in tr_true_labels]
    tr_f1_accuracy = f1_score(true_bools,pred_bools,average='micro')*100
    tr_flat_accuracy = accuracy_score(true_bools, pred_bools)*100

    print('F1 Training Score: ', tr_f1_accuracy)
    return tr_flat_accuracy, np.mean(losses)

def eval_model(model, data_loader, device, target_list):
    
    model = model.eval()
    losses = []
    correct_predictions = 0
    true_labels, pred_labels=[],[]
    with torch.no_grad():
        for d in data_loader:
            input_ids = d["input_ids"].to(device)
            attention_mask = d["attention_mask"].to(device)
            targets = d["labels"].to(device)
            outputs = model(input_ids=input_ids,attention_mask=attention_mask)

            logits = outputs[0]
            preds = torch.sigmoid(logits)
            pred_label = preds.to('cpu').numpy()
            true_label = d["labels"].to('cpu').numpy()

            loss_func = BCEWithLogitsLoss() 
            loss = loss_func(logits.view(-1,len(target_list)),targets.type_as(logits).view(-1,len(target_list)))
            losses.append(loss.item())

            true_labels.append(true_label)
            pred_labels.append(pred_label)

    pred_labels = [item for sublist in pred_labels for item in sublist]
    true_labels = [item for sublist in true_labels for item in sublist]


    threshold = 0.50
 
    pred_bools = [(pl>threshold).astype(int) for pl in pred_labels]
    true_bools = [tl==1 for tl in true_labels]
    val_f1_accuracy = f1_score(true_bools,pred_bools,average='micro')*100
    val_flat_accuracy = accuracy_score(true_bools, pred_bools)
    print('F1 Validation Score : ', val_f1_accuracy)
    return pred_bools,true_bools,val_flat_accuracy, np.mean(losses)


def plot_learning_curve(train_loss_ls,val_loss_ls, experiment_name, model_name=''):
    plt.figure(figsize=(10, 6))
    # Plot training & validation accuracy values
    plt.plot(train_loss_ls)
    plt.plot(val_loss_ls)
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

def run_experiment(config,folder_path):
    device = torch.device("cuda" if torch.cuda.is_available() else "mps")
    # Extract hyperparameters from the config
    learning_rate = config["learning_rate"]
    batch_size = config["batch_size"]
    epochs = config["epochs"]
    max_length = config["max_length"]
    weight_decay_rate = config["weight_decay_rate"]
    max_length = config["max_length"] 

    target_list = ['offensive', 'accusation', 'incitement', 'none']
    df_train, df_val, df_test = load_data(folder_path, target_list)
    tokenizer = BertTokenizer.from_pretrained('asafaya/bert-base-arabic')

    # Create data loaders
    train_data_loader = create_data_loader(df_train, tokenizer, max_length, batch_size)
    val_data_loader = create_data_loader(df_val, tokenizer, max_length, batch_size)
    test_data_loader = create_data_loader(df_test, tokenizer, max_length, batch_size)

    # Model initialization
    model = BertForSequenceClassification.from_pretrained("asafaya/bert-base-arabic", num_labels=len(target_list))
    model.to(device)


    param_optimizer = list(model.named_parameters())
    no_decay = ['bias', 'gamma', 'beta']
    optimizer_grouped_parameters = [
        {'params': [p for n, p in param_optimizer if not any(nd in n for nd in no_decay)],
         'weight_decay_rate': weight_decay_rate},
        {'params': [p for n, p in param_optimizer if any(nd in n for nd in no_decay)],
         'weight_decay_rate': 0.0}
    ]
    optimizer = AdamW(optimizer_grouped_parameters, lr=learning_rate, correct_bias=True)
    total_steps = len(train_data_loader) * epochs
    scheduler = get_linear_schedule_with_warmup(
        optimizer,
        num_warmup_steps=0,
        num_training_steps=total_steps
    )

    train_acc_ls = []
    train_loss_ls = []
    val_acc_ls = []
    val_loss_ls = []

    for epoch in range(epochs):
        print(f'Epoch {epoch + 1}/{epochs}')
        print('-' * 10)
        train_acc, train_loss = train_epoch(model, train_data_loader, optimizer, device, target_list)
        print(f'Train loss {train_loss} accuracy {train_acc}')
        pred_labels, true_labels, val_acc, val_loss = eval_model(model, val_data_loader, device, target_list)
        print(f'Val   loss {val_loss} accuracy {val_acc}')
        print()
        train_acc_ls.append(train_acc)
        train_loss_ls.append(train_loss)
        val_acc_ls.append(val_acc)
        val_loss_ls.append(val_loss)

        # Update the learning rate with the scheduler
        # scheduler.step()

    #plot_learning_curve(train_loss_ls, val_loss_ls, folder_path, model_name='bert')
    val_acc = val_acc_ls[-1]

    # Return the metric you want to optimize (e.g., validation accuracy)
    return {"val_loss": val_loss}


annotators = ['annotator3']
experiment_types = ['experiment_annotated']

for annotator in annotators:
    for experiment_type in experiment_types:
        ray.init()
        current_experiment_folder = f'experiments/{annotator}/{experiment_type}'
        config_space = {
            "learning_rate": tune.loguniform(1e-6, 1e-4),
            "batch_size": tune.choice([8, 16, 32]),
            "epochs": tune.choice([3, 4, 5]),
            "max_length": tune.choice([80, 100, 120]),
            "weight_decay_rate": tune.loguniform(1e-5, 1e-3),
        }


        # Specify the search algorithm and scheduler
        search_algorithm = tune.choice(["random"])
        scheduler = ASHAScheduler(max_t=10, grace_period=1)

        # Run hyperparameter tuning using Ray Tune
        
        analysis = tune.run(
            tune.with_parameters(run_experiment, folder_path=current_experiment_folder),
            config=config_space,
            #resources_per_trial={"gpu": 1},
            resources_per_trial={"gpu": 1, "cpu":40},
            metric="val_loss",
            mode="min",
            scheduler=scheduler,
            num_samples=10
            #local_dir='C:\\Users\\am174\\Desktop\\Twitter\\bert_parameter_tuning'
        )

        best_config = analysis.get_best_config(metric="val_accuracy", mode="max")
        print("Best Configuration:", best_config)
        ray.shutdown()
