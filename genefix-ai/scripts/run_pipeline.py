# Example: research-level pipeline script
from app.data_pipeline.sequence_cleaner import SequenceCleaner
from app.models.detection_model import MutationDetectionModel
import torch

def run_pipeline(sequence):
    cleaner = SequenceCleaner()
    model = MutationDetectionModel()
    processed = cleaner.preprocess_sequence(sequence)
    tensor = torch.tensor(processed, dtype=torch.float32).unsqueeze(0)
    output = model(tensor)
    return output.argmax(dim=1).tolist()

if __name__ == "__main__":
    seq = "ATCGATCGATCGATCGATCGATCGATCGATCG"
    print("Detected mutations:", run_pipeline(seq))
