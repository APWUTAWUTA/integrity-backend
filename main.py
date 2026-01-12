from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from sentence_transformers import SentenceTransformer, util
import numpy as np

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class AnalyzeRequest(BaseModel):
    text: str

# Load model once
model = SentenceTransformer('all-MiniLM-L6-v2')

# Example corpus (replace later with real sources)
CORPUS = [
    {"title": "Article 1", "url": "https://example.com/1", "text": "Public relations is..."},
    {"title": "Article 2", "url": "https://example.com/2", "text": "Chicken Republic productivity..."},
]

CORPUS_EMB = model.encode([c['text'] for c in CORPUS], convert_to_tensor=True)

@app.post("/analyze")
def analyze(req: AnalyzeRequest):
    text = req.text.strip()
    if not text:
        return {"similarity_percent": 0, "confidence": "Low", "explanation": "No text provided", "sources": []}

    query_emb = model.encode(text, convert_to_tensor=True)
    scores = util.cos_sim(query_emb, CORPUS_EMB)[0].cpu().numpy()

    best_idx = np.argmax(scores)
    similarity_percent = int(scores[best_idx] * 100)

    if similarity_percent >= 75:
        confidence = "High"
        explanation = "High similarity detected."
    elif similarity_percent >= 40:
        confidence = "Medium"
        explanation = "Partial similarity detected."
    else:
        confidence = "Low"
        explanation = "Text appears mostly original."

    sources = []
    if similarity_percent >= 40:
        best_match = CORPUS[best_idx]
        sources.append({
            "title": best_match['title'],
            "url": best_match['url'],
            "match_percent": similarity_percent
        })

    return {
        "similarity_percent": similarity_percent,
        "confidence": confidence,
        "explanation": explanation,
        "sources": sources
    }
