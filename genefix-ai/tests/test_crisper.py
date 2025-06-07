from app.crisper.guide_rna import GuideRNA

def test_guide_rna_design():
    guide = GuideRNA("")
    seq = "A"*20 + "TGG" + "C"*10
    guides = guide.design(seq)
    assert len(guides) == 1
    assert guides[0] == "A"*20

# Example: research-level CRISPR test
def test_guide_design():
    designer = GuideRNA("")
    seq = "A"*20 + "TGG" + "C"*10
    guides = designer.design(seq)
    assert isinstance(guides, list)
    print("Designed guides:", guides)

def test_cas9_interface():
    # Placeholder for Cas9 interface logic
    pass
