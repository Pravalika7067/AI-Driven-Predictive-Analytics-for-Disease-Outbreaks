@echo off
echo Starting Checkup Buddy...
cd /d "%~dp0"
if exist .venv\Scripts\python.exe (
    echo Using Virtual Environment...
    .venv\Scripts\python.exe -m streamlit run app.py
) else (
    echo Virtual environment not found. Trying system python...
    python -m streamlit run app.py
)
pause
