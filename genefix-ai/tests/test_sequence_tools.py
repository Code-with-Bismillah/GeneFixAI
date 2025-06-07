from app.data_pipeline.sequence_tools import gc_content, reverse_complement, transcribe, translate, find_orfs

def test_gc_content():
    assert gc_content('ATGC') == 50.0
    assert gc_content('GGGGCCCC') == 100.0
    assert gc_content('ATATATAT') == 0.0

def test_reverse_complement():
    assert reverse_complement('ATGC') == 'GCAT'
    assert reverse_complement('AAGCTT') == 'AAGCTT'[::-1].translate(str.maketrans('ATGC','TACG'))

def test_transcribe():
    assert transcribe('ATGC') == 'AUGC'

def test_translate():
    assert translate('ATGGCCATTGTAATGGGCCGCTGAAAGGGTGCCCGATAG') == 'MAIVMGR*KGAR*'[:8]  # To stop

def test_find_orfs():
    # Simple test: one ORF
    seq = 'ATGAAATAG'  # ATG (M), AAA (K), TAG (stop)
    orfs = find_orfs(seq, min_protein_length=1)
    assert any('MK' in o[2] for o in orfs)
