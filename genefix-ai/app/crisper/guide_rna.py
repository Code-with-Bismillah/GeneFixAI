from Bio.Seq import Seq

class GuideRNA:
    def __init__(self, sequence):
        self.sequence = Seq(sequence)
        
    def design(self, target_sequence):
        # PAM sequence identification (NGG)
        guides = []
        for i in range(20, len(target_sequence)-2):
            pam = target_sequence[i:i+3]
            if pam[1:] == 'GG':  # N-GG
                guides.append(target_sequence[i-20:i])
        return guides