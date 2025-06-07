from fastapi import FastAPI, UploadFile, File, HTTPException, Body
from fastapi.responses import FileResponse, JSONResponse
from api.routes import mutation_detection, mutation_correction
from api.routes.simulate_cas9 import router as simulate_cas9_router
from app.crisper.guide_rna import GuideRNA
from app.data_pipeline.genome_parser import GenomeParser
from pydantic import BaseModel
import requests
import os
from fastapi.staticfiles import StaticFiles
import json
import pandas as pd
from typing import Optional
from fastapi import APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from passlib.hash import bcrypt
from datetime import datetime
import uuid

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

# Serve static files (HTML, CSS, JS) from the current directory
app.mount("/static", StaticFiles(directory="."), name="static")

# Serve HTML files at root (e.g., /index.html, /upload.html, etc.)
@app.get("/{filename}", response_class=FileResponse)
async def serve_html(filename: str):
    if os.path.exists(filename):
        return FileResponse(filename)
    return FileResponse("index.html")

# Serve index.html at root
@app.get("/", response_class=FileResponse)
async def root():
    return FileResponse("index.html")

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

USERS_JSON = "data/processed/users.json"
USERS_XLSX = "data/processed/users.xlsx"

# Helper to load users
def load_users():
    if os.path.exists(USERS_JSON):
        with open(USERS_JSON, "r") as f:
            try:
                content = f.read().strip()
                if not content:
                    return []
                return json.loads(content)
            except Exception:
                return []
    return []

def save_users(users):
    with open(USERS_JSON, "w") as f:
        json.dump(users, f, indent=2)
    df = pd.DataFrame(users)
    df.to_excel(USERS_XLSX, index=False)

@app.post("/auth/signup")
async def signup(data: dict = Body(...)):
    users = load_users()
    if any(u["email"] == data["email"] for u in users):
        return JSONResponse(status_code=400, content={"detail": "Email already registered."})
    if "password" not in data or data["password"] != data.get("confirm_password"):
        return JSONResponse(status_code=400, content={"detail": "Passwords do not match."})
    hashed = bcrypt.hash(data["password"])
    user_id = str(uuid.uuid4())
    signup_date = datetime.utcnow().isoformat()
    # Generate initials if no profile picture is provided
    profile_picture = data.get("profile_picture")
    if not profile_picture:
        full_name = data.get("full_name", "")
        initials = "".join([part[0].upper() for part in full_name.strip().split() if part])[:2]
        profile_picture = initials if initials else None
    # Build profile with all fields
    profile = {
        "user_id": user_id,
        "full_name": data.get("full_name"),
        "username": data.get("username"),
        "email": data["email"],
        "phone": data.get("phone"),
        "gender": data.get("gender"),
        "dob": data.get("dob"),
        "country": data.get("country"),
        "profile_picture": profile_picture,
        "signup_date": signup_date,
        "agreed_terms": data.get("agreed_terms", False)
    }
    # Store hashed password only in backend, not in profile
    user = {**profile, "password": hashed}
    users.append(user)
    save_users(users)
    return {"msg": "Signup successful", "profile": profile}

@app.post("/auth/login")
async def login(data: dict = Body(...)):
    users = load_users()
    user = next((u for u in users if u["email"] == data["email"]), None)
    if not user or not bcrypt.verify(data["password"], user["password"]):
        return JSONResponse(status_code=401, content={"detail": "Invalid credentials."})
    # Defensive: handle legacy users without user_id/signup_date
    user_id = user.get("user_id", None)
    signup_date = user.get("signup_date", None)
    profile = {
        "user_id": user_id,
        "email": user["email"],
        "signup_date": signup_date
    }
    return {"msg": "Login successful", "profile": profile}

@app.get("/profile/{user_id}")
async def get_profile(user_id: str):
    users = load_users()
    user = next((u for u in users if u["user_id"] == user_id), None)
    if not user:
        return JSONResponse(status_code=404, content={"detail": "User not found."})
    # Remove password from profile
    profile = {k: v for k, v in user.items() if k != "password"}
    return profile

@app.patch("/profile/{user_id}")
async def update_profile(user_id: str, data: dict = Body(...)):
    users = load_users()
    user = next((u for u in users if u["user_id"] == user_id), None)
    if not user:
        return JSONResponse(status_code=404, content={"detail": "User not found."})
    # Update allowed fields
    for k in ["username", "full_name", "country", "profile_picture", "about", "github", "linkedin", "twitter", "website"]:
        if k in data:
            user[k] = data[k]
    save_users(users)
    profile = {k: v for k, v in user.items() if k != "password"}
    return profile