from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
from app.models.detection_model import MutationDetectionModel
from app.data_pipeline.sequence_cleaner import SequenceCleaner
from app.data_pipeline.genome_parser import GenomeParser
import torch
import os

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

@router.post("/detect_from_fasta")
async def detect_from_fasta(file: UploadFile = File(...)):
    if not file.filename.endswith(('.fasta', '.fa')):
        raise HTTPException(status_code=400, detail="Only FASTA files are supported.")
    contents = await file.read()
    save_path = f"data/raw/{file.filename}"
    with open(save_path, "wb") as f:
        f.write(contents)
    parser = GenomeParser()
    seqs = parser.parse(save_path)
    cleaner = SequenceCleaner()
    results = []
    for seq in seqs:
        processed = cleaner.preprocess_sequence(seq)
        tensor = torch.tensor(processed, dtype=torch.float32).unsqueeze(0)
        predictions = model(tensor)
        results.append({"sequence": seq, "mutations": predictions.argmax(dim=1).tolist()})
    return {"results": results}
