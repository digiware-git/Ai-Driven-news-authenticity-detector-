@echo off
echo ===============================
echo  AI NEWS AUTHENTICITY DETECTOR
echo ===============================

cd backend

if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

call venv\Scripts\activate

echo Installing requirements...
pip install -r requirements.txt

echo Starting FastAPI server...
uvicorn app:app --reload

pause
