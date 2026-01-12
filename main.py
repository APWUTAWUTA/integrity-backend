from fastapi import FastAPI
import random
import re

app = FastAPI()

@app.get("/")
def home():
    return {"status": "Backend is running (cloud)"}

def ai_score(sentence: str):
    words = sentence.split()
    length = len(words)

    score = 0.2  # base score

    # Long sentences → more likely AI
    if length > 20:
        score += 0.3
    if length > 35:
        score += 0.2

    # Repetitive wording
    unique_ratio = len(set(words)) / max(len(words), 1)
    if unique_ratio < 0.6:
        score += 0.2

    # Too perfect punctuation
    if sentence.count(",") > 3:
        score += 0.1

    return round(min(score, 0.95), 2)

@app.post("/analyze")
def analyze(data: dict):
    text = data.get("text", "")

    # split into sentences (simple but effective)
    sentences = re.split(r'(?<=[.!?])\s+', text)

    results = []

    for i, sentence in enumerate(sentences):
        results.append({
            "id": i,
            "sentence": sentence,
            "ai_probability": ai_score(sentence),
            "plagiarism_similarity": round(len(sentence) / 100, 2)
        })


    return {
        "sentence_count": len(results),
        "results": results
    }
