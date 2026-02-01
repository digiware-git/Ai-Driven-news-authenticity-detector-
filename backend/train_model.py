import pandas as pd
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer

from agents.nlp_utils import clean_text

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(BASE_DIR, "dataset")
MODEL_DIR = os.path.join(BASE_DIR, "models")

os.makedirs(MODEL_DIR, exist_ok=True)

# ----------------------------
# LOAD KAGGLE DATASET (FIXED)
# ----------------------------
kaggle_df = pd.read_csv(
    os.path.join(DATASET_DIR, "fake_news.csv"),
    low_memory=False
)

# Keep only required columns safely
if "text" not in kaggle_df.columns:
    kaggle_df.rename(columns={kaggle_df.columns[0]: "text"}, inplace=True)

if "label" not in kaggle_df.columns:
    kaggle_df.rename(columns={kaggle_df.columns[1]: "label"}, inplace=True)

kaggle_df = kaggle_df[["text", "label"]]

# Clean rows
kaggle_df.dropna(inplace=True)

def fix_label(x):
    if str(x).strip() in ["0", "1"]:
        return int(x)
    if str(x).lower().strip() in ["fake", "false"]:
        return 0
    if str(x).lower().strip() in ["real", "true"]:
        return 1
    return None

kaggle_df["label"] = kaggle_df["label"].apply(fix_label)
kaggle_df.dropna(inplace=True)
kaggle_df["label"] = kaggle_df["label"].astype(int)

# ----------------------------
# LOAD LIAR DATASET
# ----------------------------
def load_liar(path):
    df = pd.read_csv(path, sep="\t", header=None)
    df = df[[1, 2]]
    df.columns = ["label", "text"]
    return df

liar_train = load_liar(os.path.join(DATASET_DIR, "liar_train.tsv"))
liar_valid = load_liar(os.path.join(DATASET_DIR, "liar_valid.tsv"))
liar_test  = load_liar(os.path.join(DATASET_DIR, "liar_test.tsv"))

liar_df = pd.concat([liar_train, liar_valid, liar_test])

REAL = ["true", "mostly-true", "half-true"]
FAKE = ["false", "barely-true", "pants-fire"]

liar_df["label"] = liar_df["label"].apply(
    lambda x: 1 if x in REAL else 0
)

liar_df.dropna(inplace=True)

# ----------------------------
# COMBINE DATASETS
# ----------------------------
final_df = pd.concat([kaggle_df, liar_df], ignore_index=True)

print("REAL:", sum(final_df["label"] == 1))
print("FAKE:", sum(final_df["label"] == 0))

# ----------------------------
# CLEAN TEXT
# ----------------------------
final_df["text"] = final_df["text"].apply(clean_text)

# ----------------------------
# TRAIN MODEL
# ----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    final_df["text"],
    final_df["label"],
    test_size=0.2,
    random_state=42,
    stratify=final_df["label"]
)

vectorizer = TfidfVectorizer(
    max_features=5000,
    ngram_range=(1, 2)
)

X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

model = LogisticRegression(
    max_iter=300,
    class_weight="balanced"
)

model.fit(X_train_vec, y_train)

# ----------------------------
# SAVE MODEL
# ----------------------------
joblib.dump(model, os.path.join(MODEL_DIR, "news_model.pkl"))
joblib.dump(vectorizer, os.path.join(MODEL_DIR, "vectorizer.pkl"))

print("✅ Combined model trained & saved successfully")
# ----------------------------
# SAVE BM25 CORPUS
# ----------------------------
bm25_corpus = list(X)  # cleaned text corpus

joblib.dump(
    bm25_corpus,
    os.path.join(MODEL_DIR, "bm25_corpus.pkl")
)

print("✅ BM25 corpus saved")
