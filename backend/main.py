from fastapi import FastAPI, Form
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import platform
import subprocess
import pyttsx3
import os
import uuid

app = FastAPI()

# 👇 Add CORS middleware immediately after app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for dev, allow all (later restrict to ["http://localhost:3000"])
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Create a dedicated folder for generated files ---
GENERATED_DIR = os.path.join(os.path.dirname(__file__), "generated")
os.makedirs(GENERATED_DIR, exist_ok=True)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/speak")
def speak(text: str = Form(...)):
    os_name = platform.system()
    tmp_id = str(uuid.uuid4())

    # Save all files inside generated/
    wav_path = os.path.join(GENERATED_DIR, f"speech_{tmp_id}.wav")
    mp3_path = os.path.join(GENERATED_DIR, f"speech_{tmp_id}.mp3")

    # --- Generate WAV/AIFF depending on OS ---
    if os_name == "Darwin":  # macOS
        aiff_path = os.path.join(GENERATED_DIR, f"speech_{tmp_id}.aiff")
        subprocess.run(["say", "-o", aiff_path, text])
        subprocess.run(
            ["ffmpeg", "-y", "-i", aiff_path, mp3_path],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        if os.path.exists(aiff_path):
            os.remove(aiff_path)

    elif os_name in ["Windows", "Linux"]:  # Windows or Linux
        engine = pyttsx3.init()
        engine.save_to_file(text, wav_path)
        engine.runAndWait()
        subprocess.run(
            ["ffmpeg", "-y", "-i", wav_path, mp3_path],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        if os.path.exists(wav_path):
            os.remove(wav_path)

    else:
        return {"error": "Unsupported OS"}

    # --- Serve MP3 to frontend ---
    response = FileResponse(mp3_path, media_type="audio/mpeg", filename="speech.mp3")
    # os.remove(mp3_path)  # Uncomment to auto-delete MP3 after sending
    return response
