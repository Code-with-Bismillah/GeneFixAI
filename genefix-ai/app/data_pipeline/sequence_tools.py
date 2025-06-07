from Bio.Seq import Seq
from Bio.SeqUtils import gc_fraction

# GC Content Calculator
def gc_content(seq):
    return round(gc_fraction(seq) * 100, 2)

# Reverse Complement Generator
def reverse_complement(seq):
    return str(Seq(seq).reverse_complement())

# Transcription (DNA -> mRNA)
def transcribe(seq):
    return str(Seq(seq).transcribe())

# Translation (mRNA -> Protein)
def translate(seq):
    return str(Seq(seq).translate(to_stop=True))

# ORF Finder (returns list of (start, end, protein) for all ORFs)
def find_orfs(seq, min_protein_length=30):
    seq_obj = Seq(seq)
    orfs = []
    for strand, nuc in [(+1, seq_obj), (-1, seq_obj.reverse_complement())]:
        for frame in range(3):
            trans = str(nuc[frame:].translate(to_stop=False))
            aa_start = 0
            while aa_start < len(trans):
                aa_start = trans.find('M', aa_start)
                if aa_start == -1:
                    break
                aa_end = trans.find('*', aa_start)
                if aa_end == -1:
                    break
                if (aa_end - aa_start) >= min_protein_length:
                    start = frame + aa_start*3 if strand == 1 else len(seq) - frame - aa_end*3
                    end = frame + aa_end*3 if strand == 1 else len(seq) - frame - aa_start*3
                    orfs.append((start, end, trans[aa_start:aa_end]))
                aa_start = aa_end + 1
    return orfs
