import sys
import os
import argparse
from rfc_cc import *
from tfidf import *
from topic_model import *
from artifactExtractor_mod import *
from data_utils import *
from models import *

input_size = big_mat.shape[2]
batch_size = 64
hidden_size = 128
num_layers = 2
device = 'cuda'
epochs = 1200
counter = 0
print_every = 100
clip = 5
valid_loss_min = np.Inf

lstm_model = lstm_model(input_size, hidden_size, num_layers).to(device)
lr = 0.001
criterion = nn.BCEWithLogitsLoss()
optimizer = torch.optim.Adam(lstm_model.parameters(), lr=lr)

class Trainer:
    def __init__(self, seq=True):
        lstm_model.train()
        train_loss_total = []
        val_loss_total = []
        for e in range(epochs):
            running_epoch_loss = 0
            for data, target in train_loader:
                counter+=1
                data, target = data.to(device), target.to(device)
                lstm_model.zero_grad()
                output = lstm_model(data)
        #         print(output.size(), target.size())
                loss = criterion(output, target)
                running_epoch_loss+=loss.item()
                loss.backward()
                # nn.utils.clip_grad_norm_(lstm_model.parameters(), clip) # need this??
                optimizer.step()
            
            lstm_model.eval()
            running_val_loss = 0
            for data, target in test_loader:
                data, target = data.to(device), target.to(device)
                output = lstm_model(data)
                val_loss = criterion(output, target)
                running_val_loss+=val_loss.item()
            train_loss_total.append(running_epoch_loss/len(train_loader))
            val_loss_total.append(running_val_loss/len(test_loader))
            lstm_model.train()
            print('[EPOCHS:{}] epoch_loss:{}, val loss:{}'.format(e, train_loss_total[-1], val_loss_total[-1]))
        plot_current_loss_profile(train_loss_total, val_loss_total)
        torch.save(lstm_model.state_dict(), 'lstm_model.pth')