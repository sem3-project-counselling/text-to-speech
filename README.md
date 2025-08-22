# Offline TTS (macOS/Windows/Linux)

## Backend (FastAPI)
- macOS: uses `say` -> AIFF -> WAV (via `afconvert`)
- Windows/Linux: uses `pyttsx3` to generate WAV

### Run
```bash
pip install fastapi uvicorn pyttsx3
python backend/main.py
```

Server: http://localhost:8000

## Frontend (Vite + React single file)
```bash
cd frontend
npm install
npm run dev
```
Open http://localhost:5173

