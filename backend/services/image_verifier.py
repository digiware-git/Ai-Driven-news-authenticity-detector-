import pytesseract
from PIL import Image
import re

def verify_image(image_path: str):
    try:
        text = pytesseract.image_to_string(Image.open(image_path))
        text = text.strip()

        if len(text) < 40:
            return {
                "label": "UNCERTAIN",
                "confidence": 0,
                "trusted_source": False,
                "explanation": [
                    "Image does not contain sufficient readable news text",
                    "Unable to extract meaningful content from the image"
                ]
            }

        fake_keywords = [
            "breaking", "share fast", "forward", "must read",
            "guaranteed", "shocking", "viral", "alert"
        ]

        fake_hits = sum(1 for k in fake_keywords if k in text.lower())

        if fake_hits >= 2:
            return {
                "label": "FAKE",
                "confidence": 75,
                "trusted_source": False,
                "explanation": [
                    "Sensational or clickbait language detected in image text",
                    "Common fake-news patterns found in visual content"
                ]
            }

        return {
            "label": "UNCERTAIN",
            "confidence": 35,
            "trusted_source": False,
            "explanation": [
                "Image contains text but lacks full news context",
                "Manual verification is recommended for image-based claims"
            ]
        }

    except Exception:
        return {
            "label": "UNCERTAIN",
            "confidence": 0,
            "trusted_source": False,
            "explanation": [
                "Failed to process the image",
                "OCR could not extract readable text"
            ]
        }
