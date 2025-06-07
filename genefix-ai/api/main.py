from fastapi import FastAPI
from fastapi.responses import FileResponse
from api.routes import mutation_detection, mutation_correction
from app.crisper.guide_rna import GuideRNA
from pydantic import BaseModel

app = FastAPI()
app.include_router(mutation_detection, prefix="/mutation_detection")
app.include_router(mutation_correction, prefix="/mutation_correction")

guide_designer = GuideRNA("")

class GuideRequest(BaseModel):
    target_sequence: str

@app.post("/design_guides")
async def design_guides(request: GuideRequest):
    return {"guides": guide_designer.design(request.target_sequence)}

@app.get("/")
def serve_index():
    return FileResponse("index.html")