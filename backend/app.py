from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import shutil, os, uuid, tempfile

from database import SessionLocal, engine
from models.user import User
from database import Base

from services.news_verifier import verify_text
from services.url_verifier import verify_url
from services.image_verifier import verify_image
from services.auth_service import hash_password, verify_password, create_token
from schemas.auth_schema import UserRegister, UserLogin

# 🔥 CREATE TABLES
Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Driven News Authenticity Detector")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------- VERIFY APIs ----------------

@app.post("/verify-text")
def verify_news_text(payload: dict):
    return verify_text(payload.get("text", ""))

@app.post("/verify-url")
def verify_news_url(payload: dict):
    return verify_url(payload.get("url", ""))

@app.post("/verify-image")
def verify_news_image(file: UploadFile = File(...)):
    ext = file.filename.split(".")[-1]
    path = os.path.join(tempfile.gettempdir(), f"{uuid.uuid4()}.{ext}")
    with open(path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    return verify_image(path)

# ---------------- AUTH APIs ----------------

@app.post("/register")
def register(user: UserRegister, db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(400, "User already exists")

    new_user = User(
        username=user.username,
        email=user.email,
        password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    return {"message": "User registered successfully"}

@app.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()

    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(401, "Invalid credentials")

    token = create_token(db_user.username)
    return {"access_token": token, "token_type": "bearer"}
import requests

NEWS_API_KEY = "9d69f4254b804c26b4a908df86c126bd"

@app.get("/top-news")
def get_top_news():
    url = (
    "https://newsapi.org/v2/everything"
    "?q=india"
    "&language=en"
    "&pageSize=10"
    f"&apiKey={NEWS_API_KEY}"
)

    res = requests.get(url)
    return res.json()

import requests

NEWS_API_KEY = "9d69f4254b804c26b4a908df86c126bd"

@app.get("/top-news")
def get_top_news():
    url = (
        "https://newsapi.org/v2/top-headlines"
        "?country=in&pageSize=10&apiKey=" + NEWS_API_KEY
    )
    response = requests.get(url)
    return response.json()
