import torch
import torch.nn as nn
# from models import lstm_model, classifier
from torch.nn import LSTM, Linear, ReLU, BatchNorm1d
import torch.nn.functional as F

from torch.utils.data import Dataset, DataLoader, TensorDataset


class lstm_model(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers, batch_first=True, drop_prob=0.5):
        super(lstm_model, self).__init__()
        self.hidden_size = hidden_size
        self.rnn = LSTM(input_size=input_size, 
                        hidden_size=hidden_size, 
                        num_layers=num_layers, 
                        batch_first=batch_first, 
                        dropout=drop_prob)
        self.dense = Linear(hidden_size, 1)

    def forward(self, x):
        # hidden and cell state default to 0
        outputs, (ht, ct) = self.rnn(x)
#         print(outputs.size())
        out = outputs[:,-1,:]
#         print('out:', out.size())
        out = self.dense(out)
        return out

class classifier(nn.Module):
    def __init__(self, input_size, num_classes):
        super(classifier, self).__init__()
        self.fc1 = Linear(input_size, 512)
        self.bn1 = BatchNorm1d(512)
        self.r1 = ReLU()
        self.d1 = Dropout(p=0.5)
        self.m1 = MaxPool1d(3,stride = 1)
        
        self.fc2 = Linear(512, 128)
        self.bn2 = BatchNorm1d(128)
        self.r2 = ReLU()
        self.d2 = Dropout(p=0.5)
        self.m2 = MaxPool1d(3,stride = 1)
        
        self.fc3 = Linear(128, 32)
#         self.d3 = Dropout(p=0.5)
        self.r3 = ReLU()
        self.fc4 = Linear(32,num_classes)

    def forward(self, x):
        x = self.d1 ( self.r1( self.bn1 ( self.fc1(x) ) ) )
#         x = self.m1(x)
        x = self.d2 ( self.r2( self.bn2 ( self.fc2(x) ) ) )
#         x = self.m2(x)
        
        x = self.r3(self.fc3(x))
        out = self.fc4(x)
        return out

class Transformer:
        pass