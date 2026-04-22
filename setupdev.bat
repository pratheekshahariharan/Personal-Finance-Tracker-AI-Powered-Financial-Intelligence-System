@echo off
echo ================================================
echo   Personal Finance Tracker – Development Setup
echo ================================================
echo.

:: ── Backend ──────────────────────────────────────────────────────────────────
echo [1/5] Creating Python virtual environment...
python -m venv env
if errorlevel 1 (echo ERROR: Python not found. Install Python 3.10+ and retry. & pause & exit /b 1)

echo [2/5] Installing backend dependencies...
call env\Scripts\activate
pip install -r backend\requirements.txt
if errorlevel 1 (echo ERROR: pip install failed. & pause & exit /b 1)

echo [3/5] Running Alembic database migrations...
cd backend
alembic upgrade head
if errorlevel 1 (echo WARNING: Alembic migration failed. Tables will be created on first run.)

echo [4/5] Loading seed data...
sqlite3 finance.db < seed_data.sql 2>nul || echo (sqlite3 not found – seed data skipped. Run the app and add data manually.)
cd ..

:: ── Frontend ─────────────────────────────────────────────────────────────────
echo [5/5] Installing frontend dependencies...
cd frontend
npm install
if errorlevel 1 (echo ERROR: npm install failed. Make sure Node.js 18+ is installed. & pause & exit /b 1)
cd ..

echo.
echo ================================================
echo   Setup complete!
echo   Run:  runapplication.bat
echo ================================================
pause
