import numpy as np
from sklearn.preprocessing import OneHotEncoder

class SequenceCleaner:
    def __init__(self):
        # Use 'sparse_output' for scikit-learn >=1.2, else 'sparse'
        try:
            self.encoder = OneHotEncoder(categories=[['A', 'T', 'C', 'G']], handle_unknown='ignore', sparse_output=False)
        except TypeError:
            self.encoder = OneHotEncoder(categories=[['A', 'T', 'C', 'G']], handle_unknown='ignore', sparse=False)
        self.encoder.fit(np.array(['A', 'T', 'C', 'G']).reshape(-1, 1))
        
    def preprocess_sequence(self, sequence):
        valid_chars = {'A', 'T', 'C', 'G'}
        cleaned = ''.join([c for c in sequence if c in valid_chars])
        encoded = self.encoder.transform(
            np.array(list(cleaned)).reshape(-1, 1)
        )
        # Return shape: (seq_len, 4) -> transpose for (4, seq_len)
        return encoded.T