from .mutation_detection import router as mutation_detection
from .mutation_correction import router as mutation_correction
from . import simulate_cas9
from fastapi import APIRouter, Body
from app.crisper.cas9_interface import Cas9Interface
from app.data_pipeline.sequence_tools import gc_content, reverse_complement, transcribe, translate, find_orfs

router = APIRouter()
cas9 = Cas9Interface()


@router.post("/simulate_cas9")
async def simulate_cas9(sequence: str, guide: str):
    before = sequence
    after = cas9.cut(sequence, guide)
    # Dummy efficiency/specificity (replace with real logic)
    efficiency = 0.9
    specificity = 0.95
    return {
        "before": before,
        "after": after,
        "efficiency": efficiency,
        "specificity": specificity,
    }


@router.post("/sequence_tools/gc_content")
def gc_content_endpoint(data: dict = Body(...)):
    seq = data.get("sequence", "")
    return {"gc_content": gc_content(seq)}


@router.post("/sequence_tools/reverse_complement")
def reverse_complement_endpoint(data: dict = Body(...)):
    seq = data.get("sequence", "")
    return {"reverse_complement": reverse_complement(seq)}


@router.post("/sequence_tools/transcribe")
def transcribe_endpoint(data: dict = Body(...)):
    seq = data.get("sequence", "")
    return {"mRNA": transcribe(seq)}


@router.post("/sequence_tools/translate")
def translate_endpoint(data: dict = Body(...)):
    seq = data.get("sequence", "")
    return {"protein": translate(seq)}


@router.post("/sequence_tools/orf_finder")
def orf_finder_endpoint(data: dict = Body(...)):
    seq = data.get("sequence", "")
    min_len = int(data.get("min_protein_length", 30))
    orfs = find_orfs(seq, min_protein_length=min_len)
    return {"orfs": orfs}
