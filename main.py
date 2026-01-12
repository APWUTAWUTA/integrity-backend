from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class TextPayload(BaseModel):
    text: str


def interpret_score(score: float):
    if score >= 0.75:
        return {
            "confidence": "High",
            "explanation": "The text strongly matches known sources or common patterns."
        }
    elif score >= 0.40:
        return {
            "confidence": "Medium",
            "explanation": "The text shows partial similarity and may need review."
        }
    else:
        return {
            "confidence": "Low",
            "explanation": "The text appears mostly original with minimal overlap."
        }


@app.post("/analyze")
def analyze_text(payload: TextPayload):
    text = payload.text

    # Temporary scoring logic (placeholder)
    score = min(len(text) / 500, 1.0)

    interpretation = interpret_score(score)

    return {
        "score": round(score, 2),
        "confidence": interpretation["confidence"],
        "explanation": interpretation["explanation"]
    }


@app.get("/")
def health_check():
    return {"status": "API is running"}
