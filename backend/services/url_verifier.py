import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

from services.news_verifier import verify_text


TRUSTED_DOMAINS = [
    "bbc.com",
    "reuters.com",
    "cnn.com",
    "thehindu.com",
    "ndtv.com",
    "indiatoday.in",
    "hindustantimes.com"
]

ENTERTAINMENT_KEYWORDS = [
    "movie", "cinema", "film", "entertainment",
    "bollywood", "hollywood", "celebrity",
    "teaser", "trailer"
]


def extract_article_text(url: str) -> str:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    paragraphs = soup.find_all("p")

    text = " ".join(p.get_text(strip=True) for p in paragraphs)
    return text


def verify_url(url: str):
    try:
        parsed = urlparse(url)
        domain = parsed.netloc.lower()

        # Entertainment filter
        if any(word in domain for word in ENTERTAINMENT_KEYWORDS):
            return {
                "label": "UNCERTAIN",
                "confidence": 0.0,
                "trusted_source": False,
                "explanation": [
                    "Entertainment or opinion-based source detected",
                    "Such content is outside factual news verification scope"
                ]
            }

        trusted = any(td in domain for td in TRUSTED_DOMAINS)

        # Try scraping
        try:
            article_text = extract_article_text(url)
        except Exception:
            article_text = ""

        # 🔥 TRUSTED SOURCE OVERRIDE (KEY FIX)
        if trusted and len(article_text.split()) < 80:
            return {
                "label": "REAL",
                "confidence": 70.0,
                "trusted_source": True,
                "explanation": [
                    "The article is published by a highly trusted news organization",
                    "Trusted source credibility outweighs automated content extraction limitations",
                    "Such organizations follow strict editorial and fact-checking standards"
                ]
            }

        # If enough content → ML verification
        if len(article_text.split()) >= 80:
            result = verify_text(article_text)
            result["trusted_source"] = trusted

            if trusted:
                result["explanation"].insert(
                    0,
                    "The article is published by a trusted and established news organization"
                )
            else:
                result["explanation"].insert(
                    0,
                    "The article source is not listed among widely trusted news organizations"
                )

            return result

        # Default fallback
        return {
            "label": "UNCERTAIN",
            "confidence": 0.0,
            "trusted_source": trusted,
            "explanation": [
                "Insufficient article content could be extracted",
                "The website may use dynamic loading or block automated scraping"
            ]
        }

    except Exception:
        return {
            "label": "UNCERTAIN",
            "confidence": 0.0,
            "trusted_source": False,
            "explanation": [
                "Failed to fetch or process the article URL",
                "The website may restrict automated access"
            ]
        }
