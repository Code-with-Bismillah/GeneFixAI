import torch
import torch.nn as nn

class CorrectionTransformer(nn.Module):
    def __init__(self):
        super().__init__()
        self.embedding = nn.Embedding(num_embeddings=5, embedding_dim=64)
        self.transformer = nn.Transformer(d_model=64, nhead=8)
        self.fc = nn.Linear(64, 5)
        
    def forward(self, src, tgt):
        src_emb = self.embedding(src).permute(1, 0, 2)
        tgt_emb = self.embedding(tgt).permute(1, 0, 2)
        output = self.transformer(src_emb, tgt_emb)
        return self.fc(output.permute(1, 0, 2))