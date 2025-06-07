import torch
from app.models.detection_model import MutationDetectionModel
from app.data_pipeline.sequence_cleaner import SequenceCleaner

def test_mutation_detection():
    model = MutationDetectionModel()
    cleaner = SequenceCleaner()
    # Example: sequence of 30 bases
    sequence = 'ATCG' * 7 + 'AATC'
    processed = cleaner.preprocess_sequence(sequence)
    tensor = torch.tensor(processed, dtype=torch.float32).unsqueeze(0)  # (1, 4, seq_len)
    output = model(tensor)
    assert output.shape[-1] == 2

def test_sequence_cleaner():
    cleaner = SequenceCleaner()
    sequence = 'ATCGXYZ'
    processed = cleaner.preprocess_sequence(sequence)
    assert processed.shape[0] == 4
    assert processed.sum() == 4
