import sys
import os
import argparse
from artifact_extraction.data_utils import *
import torch
import torch.nn as nn
from artifact_extraction.models import lstm_model, classifier
from torch.nn import LSTM, Linear, ReLU, BatchNorm1d, Dropout, MaxPool1d
import torch.nn.functional as F
from sklearn.model_selection import train_test_split
from torch.utils.data import Dataset, DataLoader, TensorDataset

class Trainer:
    def __init__(self, params=None):
        self.batch_size = 64
        self.hidden_size = 128
        self.num_layers = 2
        self.device = 'cuda'
        self.epochs = 100
        self.print_every = 100
        self.clip = 5
        self.valid_loss_min = np.Inf
    
    def split_and_create_loaders(self, data, Y):
        self.input_size = data.shape[1]
        self.num_classes = len(label_dict)
        X_train, X_test, y_train, y_test = train_test_split(data, Y, test_size=0.33, random_state=42)
        train_dataset = TensorDataset(torch.Tensor(X_train), torch.Tensor(y_train)) 
        test_dataset = TensorDataset(torch.Tensor(X_test), torch.Tensor(y_test))

        self.trainloader = torch.utils.data.DataLoader(dataset=train_dataset,
                                                            batch_size=self.batch_size, 
                                                            shuffle=True)
                    
        self.testloader = torch.utils.data.DataLoader(dataset=test_dataset,
                                                            batch_size=self.batch_size, 
                                                            shuffle=False)
    
    def train_nway(self):
        use_cuda = torch.cuda.is_available()
        device = torch.device("cuda" if use_cuda else "cpu")
        clf = classifier(self.input_size, self.num_classes).to(device)
        lr = 0.001
        criterion = nn.CrossEntropyLoss()
        optimizer = torch.optim.Adam(clf.parameters(), lr=lr)

        clf.train()
        train_loss_total = []
        val_loss_total = []
        for e in range(self.epochs):
            running_epoch_loss = 0
            correct = 0
            for data, target in self.trainloader:
                data, target = data.to(device).float(), target.to(device).long()
                clf.zero_grad()
                output = clf(data)
                loss = criterion(output, target)
                running_epoch_loss+=loss.item()
                loss.backward()
                # nn.utils.clip_grad_norm_(clf.parameters(), clip) # need this??
                optimizer.step()
        #     print('correct first: ', correct.item())
            clf.eval()
            running_val_loss = 0
            correct = 0
            for data, target in self.testloader:
                data, target = data.to(device), target.to(device).long()
                output = clf(data)
                correct+=torch.sum(torch.argmax(output, dim=1)==target)
                val_loss = criterion(output, target)
                running_val_loss+=val_loss.item()
            train_loss_total.append(running_epoch_loss/len(self.trainloader))
            val_loss_total.append(running_val_loss/len(self.testloader))
            clf.train()
            print('[EPOCHS:{}] epoch_loss:{}, val loss:{}, correct: {}'.format(e, train_loss_total[-1], val_loss_total[-1], correct))
        plot_current_loss_profile(train_loss_total, val_loss_total)
        torch.save(clf.state_dict(), 'classifier_nway.pth')