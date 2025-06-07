from .mutation_detection import router as mutation_detection
from .mutation_correction import router as mutation_correction
from fastapi import APIRouter
from app.crisper.cas9_interface import Cas9Interface

router = APIRouter()
cas9 = Cas9Interface()

@router.post("/simulate_cas9")
async def simulate_cas9(sequence: str, guide: str):
    before = sequence
    after = cas9.cut(sequence, guide)
    efficiency = 0.9
    specificity = 0.95
    return {
        "before": before,
        "after": after,
        "efficiency": efficiency,
        "specificity": specificity
    }
