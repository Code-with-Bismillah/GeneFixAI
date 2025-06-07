from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from api.routes import mutation_detection, mutation_correction
from api.routes.simulate_cas9 import router as simulate_cas9_router
from app.crisper.guide_rna import GuideRNA
from app.data_pipeline.genome_parser import GenomeParser
from pydantic import BaseModel
import requests
import os

app = FastAPI()
app.include_router(mutation_detection, prefix="/mutation_detection")
app.include_router(mutation_correction, prefix="/mutation_correction")
app.include_router(simulate_cas9_router, prefix="/crispr")

guide_designer = GuideRNA("")

class GuideRequest(BaseModel):
    target_sequence: str

@app.post("/design_guides")
async def design_guides(request: GuideRequest):
    return {"guides": guide_designer.design(request.target_sequence)}

@app.get("/")
def serve_index():
    return FileResponse("./index.html")

@app.post("/upload_fasta")
async def upload_fasta(file: UploadFile = File(...)):
    if not file.filename.endswith(('.fasta', '.fa')):
        raise HTTPException(status_code=400, detail="Only FASTA files are supported.")
    contents = await file.read()
    save_path = f"data/raw/{file.filename}"
    with open(save_path, "wb") as f:
        f.write(contents)
    # Optionally parse and return sequence info
    parser = GenomeParser()
    seqs = parser.parse(save_path)
    return {"filename": file.filename, "num_sequences": len(seqs)}

@app.get("/fetch_ncbi_fasta")
def fetch_ncbi_fasta(ncbi_id: str):
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    params = {"db": "nuccore", "id": ncbi_id, "rettype": "fasta", "retmode": "text"}
    r = requests.get(url, params=params)
    if r.status_code != 200:
        raise HTTPException(status_code=404, detail="NCBI record not found")
    fasta_path = f"data/raw/{ncbi_id}.fasta"
    with open(fasta_path, "w") as f:
        f.write(r.text)
    return FileResponse(fasta_path, media_type="text/plain")

@app.get("/fetch_ensembl_variant")
def fetch_ensembl_variant(variant_id: str):
    url = f"https://rest.ensembl.org/variation/human/{variant_id}?"
    headers = {"Content-Type": "application/json"}
    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        raise HTTPException(status_code=404, detail="Variant not found in Ensembl")
    return JSONResponse(content=r.json())