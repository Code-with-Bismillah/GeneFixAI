from fastapi import APIRouter
from pydantic import BaseModel
from app.models.correction_model import CorrectionTransformer
import torch

router = APIRouter()
model = CorrectionTransformer()

class CorrectionRequest(BaseModel):
    src: list
    tgt: list

@router.post("/correct")
async def correct_mutations(request: CorrectionRequest):
    src = torch.tensor(request.src, dtype=torch.long)
    tgt = torch.tensor(request.tgt, dtype=torch.long)
    output = model(src, tgt)
    return {"corrected": output.argmax(dim=-1).tolist()}
