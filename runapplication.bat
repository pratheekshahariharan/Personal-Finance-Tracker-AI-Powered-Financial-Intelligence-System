@echo off
echo ================================================
echo   Personal Finance Tracker – Starting Application
echo ================================================
echo.

echo Starting backend (FastAPI) on http://localhost:8000 ...
start "Personal Finance Tracker Backend" cmd /k "call env\Scripts\activate && cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

:: Small delay to let the backend start before the browser opens
timeout /t 3 /nobreak >nul

echo Starting frontend (React) on http://localhost:3000 ...
start "Personal Finance Tracker Frontend" cmd /k "cd frontend && npm start"

echo.
echo ================================================
echo   API docs: http://localhost:8000/docs
echo   App:      http://localhost:3000
echo ================================================
