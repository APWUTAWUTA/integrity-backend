from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TextPayload(BaseModel):
    text: str


def interpret_score(score: float):
    if score >= 0.75:
        return {"confidence": "High", "explanation": "Strong similarity detected."}
    elif score >= 0.40:
        return {"confidence": "Medium", "explanation": "Partial similarity detected."}
    else:
        return {"confidence": "Low", "explanation": "Mostly original content."}


@app.post("/analyze")
def analyze_text(payload: TextPayload):
    score = min(len(payload.text) / 500, 1.0)
    interpretation = interpret_score(score)

    return {
        "score": round(score, 2),
        "confidence": interpretation["confidence"],
        "explanation": interpretation["explanation"]
    }


@app.get("/")
def root():
    return {"status": "API is running"}
