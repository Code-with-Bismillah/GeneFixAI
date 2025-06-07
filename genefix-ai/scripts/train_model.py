# Example: research-level training script
from app.models.detection_model import MutationDetectionModel
from app.data_pipeline.sequence_cleaner import SequenceCleaner
import torch
import torch.optim as optim
import torch.nn as nn

# Dummy data for demonstration
sequences = ['ATCGATCGATCGATCG', 'TGCATGCATGCATGCA']
labels = [0, 1]

cleaner = SequenceCleaner()
model = MutationDetectionModel()
optimizer = optim.Adam(model.parameters(), lr=0.001)
criterion = nn.CrossEntropyLoss()

for epoch in range(2):  # Short demo
    for seq, label in zip(sequences, labels):
        processed = cleaner.preprocess_sequence(seq)
        tensor = torch.tensor(processed, dtype=torch.float32).unsqueeze(0)
        output = model(tensor)
        loss = criterion(output, torch.tensor([label]))
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        print(f"Epoch {epoch}, Loss: {loss.item()}")
