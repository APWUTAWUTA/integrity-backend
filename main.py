from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow Chrome extension
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class AnalyzeRequest(BaseModel):
    text: str

@app.get("/")
def root():
    return {"status": "ok"}

@app.post("/analyze")
def analyze(req: AnalyzeRequest):
    text = req.text.strip()
    length = len(text)

    # SIMPLE similarity proxy (placeholder logic)
    similarity = min(round(length / 500, 2), 1.0)

    if similarity >= 0.75:
        confidence = "High"
        explanation = "Text is very similar to known patterns."
    elif similarity >= 0.4:
        confidence = "Medium"
        explanation = "Text shows partial similarity."
    else:
        confidence = "Low"
        explanation = "Text appears mostly original."

    return {
        "similarity": similarity,
        "confidence": confidence,
        "explanation": explanation
    }
