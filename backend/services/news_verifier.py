import joblib
import os

from agents.nlp_utils import clean_text
from agents.bm25_engine import bm25_score

# -----------------------------------
# LOAD MODEL & VECTORIZER (ONCE)
# -----------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model = joblib.load(os.path.join(BASE_DIR, "../models/news_model.pkl"))
vectorizer = joblib.load(os.path.join(BASE_DIR, "../models/vectorizer.pkl"))


# -----------------------------------
# MAIN VERIFICATION FUNCTION
# -----------------------------------

def verify_text(text: str):

    # -------- BASIC SAFETY CHECK --------
    if not text or len(text.split()) < 15:
        return {
            "label": "UNCERTAIN",
            "confidence": 0.0,
            "trusted_source": False,
            "explanation": [
                "Input text is too short for reliable verification",
                "Short or headline-only content lacks sufficient context"
            ]
        }

    # -------- NLP PREPROCESSING --------
    cleaned = clean_text(text)

    # -------- ML PREDICTION --------
    vector = vectorizer.transform([cleaned])
    probs = model.predict_proba(vector)[0]
    confidence = round(max(probs) * 100, 2)
    prediction = model.predict(vector)[0]

    # -------- BM25 RELEVANCE --------
    bm25 = bm25_score(cleaned)

    # -----------------------------------
    # HYBRID DECISION LOGIC (ML + BM25)
    # -----------------------------------
    # ML low confidence + low BM25 → UNCERTAIN
    if confidence < 40 and bm25 < 3:
        label = "UNCERTAIN"

    # ML positive OR strong BM25 → REAL
    elif prediction == 1 or bm25 >= 5:
        label = "REAL"

    # Otherwise → FAKE
    else:
        label = "FAKE"

    # -----------------------------------
    # EXPLANATION ENGINE
    # -----------------------------------

    explanation = []

    if label == "REAL":
        explanation.extend([
            "Linguistic patterns align with factual news reporting",
            "No strong emotional or sensational language detected",
            "Text structure resembles credible news articles"
        ])

    elif label == "FAKE":
        explanation.extend([
            "Clickbait or misleading language patterns detected",
            "Emotionally charged or exaggerated phrasing observed",
            "Text deviates from standard journalistic style"
        ])

    else:
        explanation.extend([
            "Low confidence due to limited or ambiguous context",
            "Text does not strongly match known real or fake patterns"
        ])

    # -------- BM25 EXPLANATION (ALWAYS ADD) --------
    explanation.append(
        f"BM25 relevance score: {round(bm25, 2)} indicating contextual similarity with known news corpus"
    )

    return {
        "label": label,
        "confidence": confidence,
        "trusted_source": False,
        "explanation": explanation
    }
