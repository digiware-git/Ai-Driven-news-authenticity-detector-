from rank_bm25 import BM25Okapi
import joblib
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load training corpus (same used for ML)
CORPUS_PATH = os.path.join(BASE_DIR, "../models/bm25_corpus.pkl")

# Load once
with open(CORPUS_PATH, "rb") as f:
    corpus = joblib.load(f)

tokenized_corpus = [doc.split() for doc in corpus]
bm25 = BM25Okapi(tokenized_corpus)


def bm25_score(query: str) -> float:
    query_tokens = query.split()
    scores = bm25.get_scores(query_tokens)
    return max(scores)
