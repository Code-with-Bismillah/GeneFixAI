import torch
import torch.nn as nn

class AwesomeMutationModel(nn.Module):
    """
    Hybrid model: CNN + BiLSTM + Transformer encoder for mutation detection.
    Input: (batch, 4, seq_len) one-hot encoded DNA
    Output: (batch, seq_len, num_classes) per-base mutation classification
    """
    def __init__(self, seq_len=100, num_classes=3, d_model=64, nhead=4, num_layers=2):
        super().__init__()
        self.conv1 = nn.Conv1d(4, 32, kernel_size=5, padding=2)
        self.conv2 = nn.Conv1d(32, d_model, kernel_size=3, padding=1)
        self.bilstm = nn.LSTM(d_model, d_model, batch_first=True, bidirectional=True)
        encoder_layer = nn.TransformerEncoderLayer(d_model=d_model*2, nhead=nhead, batch_first=True)
        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers=num_layers)
        self.fc = nn.Linear(d_model*2, num_classes)

    def forward(self, x):
        # x: (batch, 4, seq_len)
        x = torch.relu(self.conv1(x))
        x = torch.relu(self.conv2(x))  # (batch, d_model, seq_len)
        x = x.permute(0, 2, 1)  # (batch, seq_len, d_model)
        x, _ = self.bilstm(x)   # (batch, seq_len, d_model*2)
        x = self.transformer(x) # (batch, seq_len, d_model*2)
        out = self.fc(x)        # (batch, seq_len, num_classes)
        return out
