import os
import joblib
import pandas as pd
import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from agents.nlp_utils import clean_text


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(BASE_DIR, "../dataset")
MODEL_DIR = os.path.join(BASE_DIR, "../models")

os.makedirs(MODEL_DIR, exist_ok=True)

texts = []

# -------- Kaggle Fake News --------
kaggle_path = os.path.join(DATASET_DIR, "fake_news.csv")
if os.path.exists(kaggle_path):
    df = pd.read_csv(kaggle_path, usecols=["text"], low_memory=False)
    texts.extend(df["text"].dropna().astype(str).tolist())

# -------- LIAR Dataset --------
def load_liar(path):
    df = pd.read_csv(path, sep="\t", header=None)
    return df[2].dropna().astype(str).tolist()

for file in ["liar_train.tsv", "liar_test.tsv", "liar_valid.tsv"]:
    p = os.path.join(DATASET_DIR, file)
    if os.path.exists(p):
        texts.extend(load_liar(p))

# -------- CLEAN TEXT --------
cleaned_texts = [clean_text(t) for t in texts if len(t.split()) > 5]

# -------- SAVE --------
corpus_path = os.path.join(MODEL_DIR, "bm25_corpus.pkl")
joblib.dump(cleaned_texts, corpus_path)

print(f"✅ BM25 corpus built & saved: {len(cleaned_texts)} documents")
