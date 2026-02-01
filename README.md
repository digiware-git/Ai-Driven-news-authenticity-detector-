# 🧠 AI-Driven News Authenticity Detector

An end-to-end **AI-powered web application** that detects whether a news article is **REAL**, **FAKE**, or **UNCERTAIN** using **Natural Language Processing (NLP)**, **Machine Learning**, and **Multimodal Analysis** (Text, URL & Image).

> 🚀 Built with **FastAPI + HTML + CSS + JavaScript**  
> 🎯 Focused on **Explainable AI**, not black-box predictions  

---

## 📌 Problem Statement

Fake news spreads rapidly on social media and news platforms, influencing public opinion and causing social, political, and economic harm.  
Manual verification is slow, unreliable, and not scalable.

### ❌ Challenges
- Clickbait and emotionally charged language  
- Misleading or fake images  
- Unverified online sources  
- Rapid spread of misinformation  

### ✅ Solution
This system uses **Artificial Intelligence** to automatically analyze and verify news content and provide **confidence scores with explanations**.

---

## 🚀 Key Features

### 🔹 Multimodal Verification
- 📝 **Text-based News Verification**
- 🔗 **URL-based News Verification**
- 📷 **Image-based News Verification**

### 🔹 Explainable AI
- Shows **WHY** news is Fake / Real / Uncertain
- Linguistic patterns & semantic reasoning
- Confidence score for every prediction

### 🔹 Live Top News Verification
- Fetches real-time news
- One-click verification using AI

### 🔹 User System
- Secure Login & Signup
- Profile dropdown with logout
- JWT-based authentication

### 🔹 Unified History Panel
- Stores verification history of:
  - Text
  - URL
  - Image
  - Top News
- Time-stamped and categorized

---

## 🧠 System Architecture

            ┌────────────────────┐
            │   User Interface   │
            │ (HTML / CSS / JS)  │
            └─────────┬──────────┘
                      │
                      ▼
            ┌────────────────────┐
            │   FastAPI Backend  │
            │   (REST APIs)     │
            └─────────┬──────────┘
                      │
    ┌─────────────────┼─────────────────┐
   ▼                 ▼                 ▼
┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│ Text Model │ │ URL Analyzer│ │ Image Model │
│ (NLP + ML) │ │ Content NLP │ │ CV Analysis │
└──────┬──────┘ └──────┬──────┘ └──────┬──────┘
│ │ │
└────────┬────────┴────────┬────────┘
▼ ▼
┌────────────────────────────┐
│ Explainability Engine │
│ (Why Fake / Real?) │
└────────────┬───────────────┘
▼
┌─────────────────┐
│ Final Prediction│
│ REAL / FAKE / ? │
└─────────────────┘


---

## 🔍 System Workflow

User Input
│
├── Text → NLP Cleaning → Feature Extraction → ML Model
│
├── URL → Article Extraction → NLP Analysis → ML Model
│
└── Image → Image Processing → Visual Analysis → Model
│
▼
Prediction + Confidence Score
│
▼
Explainable AI Output


---

## 🧪 Verification Techniques

### 📝 Text Verification
- Tokenization
- Stop-word removal
- Lemmatization
- TF-IDF & semantic analysis
- Detection of emotional exaggeration

### 🔗 URL Verification
- Article scraping
- Source credibility analysis
- Content normalization
- Semantic consistency check

### 📷 Image Verification
- Image preprocessing
- Manipulation detection
- Context mismatch detection

---

## 📊 Explainability Layer

Instead of a simple label, the system explains:
- Suspicious keywords
- Emotional manipulation
- Clickbait indicators
- Linguistic anomalies
- Source trust issues

---

## 🧑‍💻 Technology Stack

### Frontend
- HTML5  
- CSS3 (Glass UI, Navbar, Modals)  
- JavaScript (Vanilla)

### Backend
- Python
- FastAPI
- SQLAlchemy
- JWT Authentication

### AI / ML
- NLP preprocessing
- Machine Learning classifier
- Confidence-based predictions

---

## 🔐 Authentication Flow

- Secure Signup & Login
- Password hashing
- Token-based authentication
- Protected routes

---

## 📡 API Endpoints

| Method | Endpoint        | Description |
|------|----------------|-------------|
| POST | `/register`    | User registration |
| POST | `/login`       | User login |
| POST | `/verify-text` | Verify news text |
| POST | `/verify-url`  | Verify news URL |
| POST | `/verify-image`| Verify news image |
| GET  | `/top-news`    | Fetch live top news |

---

## 🕒 Unified History System

All verification results are stored together:

[TEXT] REAL (92%)
[URL] FAKE (87%)
[IMAGE] UNCERTAIN (55%)
[NEWS] REAL (90%)


---

## 📂 Project Structure

AI-News-Authenticity-Detection
│
├── backend/
│ ├── app.py
│ ├── train.py
│ ├── utils.py
│
├── models/ (ignored - download separately)
├── dataset/ (ignored - download separately)
├── requirements.txt
├── README.md
└── .gitignore




---

## ⚠️ Important (Large Files)

Due to GitHub size limits (>100MB not allowed), dataset and model files are hosted separately.

### 📥 Download Files

### 🔹 Dataset
Download fake_news.csv:
👉 **[Click Here to Download Dataset](https://drive.google.com/drive/folders/1RncdQSeIUGonF0EfA4ETx2-A0iOKUmp6?usp=drive_link)**

### 🔹 Trained Model
Download bm25_corpus.pkl:
👉 **[Click Here to Download Model](https://drive.google.com/drive/folders/19MhvYq1xYCeMNKQqyd6ao4DAjAWlXs2u?usp=drive_link)**

After downloading:

Place files like this:

backend/
├── dataset/(place all dataset file in this folder)
├── models/(place all model in this folder)






---

## 📈 Advantages

- ✔ Multimodal fake news detection  
- ✔ Explainable AI output  
- ✔ Scalable FastAPI backend  
- ✔ User-friendly professional UI  
- ✔ Real-world applicability  

---

## 🚀 Future Enhancements

- 📄 PDF verification reports  
- 🧠 Deep Learning models (BERT, CNN)  
- 🌍 Multilingual support  
- ☁ Cloud deployment  
- 📊 Admin analytics dashboard  

---

## 🏁 Conclusion

This project demonstrates how **Artificial Intelligence** can effectively combat misinformation using **accuracy, transparency, and explainability**.  
It provides a strong foundation for real-world fake news detection systems.

---

## 👨‍🎓 Author

**Abhishek singh**  
B.Tech (Computer Science Engineering)  
Project: *AI-Driven News Authenticity Detector*
