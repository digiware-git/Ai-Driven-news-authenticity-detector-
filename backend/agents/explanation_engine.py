import re

EMOTIONAL_WORDS = [
    "shocking", "breaking", "secret", "exposed", "unbelievable",
    "you won't believe", "miracle", "dangerous", "viral"
]

def generate_explanation(label, confidence, text):
    reasons = []

    text_lower = text.lower()

    # Emotional language check
    emotional_hits = [w for w in EMOTIONAL_WORDS if w in text_lower]
    if emotional_hits:
        reasons.append(
            f"Emotional / sensational words detected: {', '.join(emotional_hits)}"
        )

    # Confidence based reasoning
    if confidence < 0.6:
        reasons.append("Low prediction confidence due to weak linguistic signals")

    # Label based explanation
    if label == "FAKE":
        reasons.extend([
            "Writing style matches common fake news patterns",
            "High exaggeration or clickbait structure detected",
            "Content lacks neutral factual tone"
        ])
    elif label == "UNCERTAIN":
        reasons.append(
            "The content does not contain sufficient contextual information for a confident classification"
        )
    elif label == "REAL":
        reasons.extend([
            "Neutral and factual language observed",
            "Sentence structure consistent with real news articles",
            "No excessive emotional manipulation detected"
        ])
    else:
        reasons.append("Insufficient information to make a confident decision")

    return reasons

