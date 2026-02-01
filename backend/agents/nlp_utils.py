import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Downloads (safe even if already present)
nltk.download("stopwords")
nltk.download("wordnet")
nltk.download("omw-1.4")

stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()


def safe_lemmatize(word: str) -> str:
    """
    Safely lemmatize a word.
    If WordNet crashes (Windows issue), return word as-is.
    """
    try:
        return lemmatizer.lemmatize(word, pos="v")
    except Exception:
        return word


def clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"http\S+|www\S+", "", text)
    text = re.sub(r"[^a-z\s]", "", text)

    tokens = text.split()

    cleaned_tokens = [
        safe_lemmatize(word)
        for word in tokens
        if word not in stop_words and len(word) > 2
    ]

    return " ".join(cleaned_tokens)
