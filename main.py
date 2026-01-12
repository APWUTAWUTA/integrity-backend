from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class AnalyzeRequest(BaseModel):
    text: str

@app.post("/analyze")
def analyze(req: AnalyzeRequest):
    text = req.text.strip()
    length = len(text)

    # --- TEMP similarity logic (placeholder) ---
    similarity_ratio = min(length / 500, 1.0)
    similarity_percent = int(similarity_ratio * 100)

    if similarity_percent >= 75:
        confidence = "High"
        explanation = "High similarity detected with existing content."
    elif similarity_percent >= 40:
        confidence = "Medium"
        explanation = "Partial similarity detected."
    else:
        confidence = "Low"
        explanation = "Text appears mostly original."

    # --- MOCK SOURCES (next phase will make real) ---
    sources = []
    if similarity_percent >= 40:
        sources = [
            {
                "title": "Example Article",
                "url": "https://example.com/article",
                "match_percent": similarity_percent
            }
        ]

    return {
        "similarity_percent": similarity_percent,
        "confidence": confidence,
        "explanation": explanation,
        "sources": sources
    }
