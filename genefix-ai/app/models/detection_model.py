import torch
import torch.nn as nn

class MutationDetectionModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1d = nn.Conv1d(in_channels=4, out_channels=32, kernel_size=3)
        self.lstm = nn.LSTM(input_size=32, hidden_size=64, batch_first=True)
        self.fc = nn.Linear(64, 2)
        
    def forward(self, x):
        # x shape: (batch, 4, seq_len)
        x = torch.relu(self.conv1d(x))
        x = x.permute(0, 2, 1)  # (batch, seq_len, features)
        _, (h_n, _) = self.lstm(x)
        return self.fc(h_n.squeeze(0))