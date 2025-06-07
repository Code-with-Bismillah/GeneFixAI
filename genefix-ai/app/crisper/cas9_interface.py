# Placeholder for Cas9 interface logic
class Cas9Interface:
    def __init__(self):
        pass

    def cut(self, sequence, guide):
        # Simulate Cas9 cut: find guide, cut 3 bases after guide (PAM site)
        idx = sequence.find(guide)
        if idx == -1:
            return sequence  # guide not found, return original
        cut_site = idx + len(guide)
        # Remove 3 bases at cut site to simulate DSB
        return sequence[:cut_site] + sequence[cut_site+3:]
