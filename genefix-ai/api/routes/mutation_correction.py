from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.models.correction_model import CorrectionTransformer
from app.crisper.guide_rna import GuideRNA
from app.crisper.cas9_interface import Cas9Interface
import torch

router = APIRouter()
model = CorrectionTransformer()
cas9 = Cas9Interface()

class CorrectionRequest(BaseModel):
    src: list
    tgt: list

class SuggestCorrectionRequest(BaseModel):
    sequence: str
    mutation_pos: int

@router.post("/correct")
async def correct_mutations(request: CorrectionRequest):
    src = torch.tensor(request.src, dtype=torch.long)
    tgt = torch.tensor(request.tgt, dtype=torch.long)
    output = model(src, tgt)
    return {"corrected": output.argmax(dim=-1).tolist()}

@router.post("/suggest_correction")
async def suggest_correction(request: SuggestCorrectionRequest):
    sequence = request.sequence
    mutation_pos = request.mutation_pos
    guide_designer = GuideRNA("")
    guides = guide_designer.design(sequence)
    if not guides:
        raise HTTPException(status_code=404, detail="No valid guides found.")
    corrected_seq = cas9.cut(sequence, guides[0])
    on_target_score = 0.95
    off_target_score = 0.05
    return {
        "mutation_pos": mutation_pos,
        "suggested_guide": guides[0],
        "on_target_score": on_target_score,
        "off_target_score": off_target_score,
        "corrected_sequence": corrected_seq
    }
