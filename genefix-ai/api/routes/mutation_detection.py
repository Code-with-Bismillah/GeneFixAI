from fastapi import APIRouter
from pydantic import BaseModel
from app.models.detection_model import MutationDetectionModel
from app.data_pipeline.sequence_cleaner import SequenceCleaner
import torch

router = APIRouter()
model = MutationDetectionModel()

class SequenceRequest(BaseModel):
    sequence: str

@router.post("/detect")
async def detect_mutations(request: SequenceRequest):
    processed = SequenceCleaner().preprocess_sequence(request.sequence)
    tensor = torch.tensor(processed, dtype=torch.float32).unsqueeze(0)
    predictions = model(tensor)
    return {"mutations": predictions.argmax(dim=1).tolist()}
