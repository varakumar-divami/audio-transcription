import os
import uuid
import threading
os.environ["HF_HUB_DISABLE_PROGRESS_BARS"] = "0"

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from datetime import datetime

from transcriber import download_audio, transcribe_to_english, save_transcript, DEFAULT_MODEL

app = FastAPI()

# In-memory job store: job_id -> state dict
jobs: dict[str, dict] = {}


class TranscribeRequest(BaseModel):
    url: str
    model: str = DEFAULT_MODEL


def run_job(job_id: str, url: str, model: str):
    job = jobs[job_id]
    try:
        job["status"] = "downloading"
        audio_path, title = download_audio(url, output_dir="recordings")
        job["title"] = title

        job["status"] = "transcribing"
        def on_segment(start, end, text):
            job["segments"].append({"start": round(start, 1), "end": round(end, 1), "text": text})

        transcript = transcribe_to_english(audio_path, model, on_segment=on_segment)

        job["status"] = "saving"
        out_path = save_transcript(transcript, title, output_dir="outputs")
        job["transcript"] = transcript
        job["output_file"] = os.path.basename(out_path)
        job["status"] = "done"

    except Exception as e:
        job["status"] = "error"
        job["error"] = str(e)


@app.post("/api/transcribe")
def start_transcription(req: TranscribeRequest):
    job_id = str(uuid.uuid4())
    jobs[job_id] = {
        "status": "pending",
        "segments": [],
        "transcript": None,
        "output_file": None,
        "title": None,
        "error": None,
    }
    threading.Thread(target=run_job, args=(job_id, req.url, req.model), daemon=True).start()
    return {"job_id": job_id}


@app.get("/api/status/{job_id}")
def get_status(job_id: str):
    if job_id not in jobs:
        return {"error": "Job not found"}
    return jobs[job_id]


def run_voice_job(job_id: str, audio_path: str, title: str, model: str):
    job = jobs[job_id]
    try:
        job["status"] = "transcribing"
        def on_segment(start, end, text):
            job["segments"].append({"start": round(start, 1), "end": round(end, 1), "text": text})

        transcript = transcribe_to_english(audio_path, model, on_segment=on_segment)

        job["status"] = "saving"
        out_path = save_transcript(transcript, title, output_dir="outputs")
        job["transcript"] = transcript
        job["output_file"] = os.path.basename(out_path)
        job["status"] = "done"

    except Exception as e:
        job["status"] = "error"
        job["error"] = str(e)


@app.post("/api/transcribe-audio")
async def transcribe_audio(
    file: UploadFile = File(...),
    model: str = Form(DEFAULT_MODEL),
):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    title = f"voice_recording_{timestamp}"
    ext = os.path.splitext(file.filename or "audio.webm")[1] or ".webm"
    os.makedirs("recordings", exist_ok=True)
    audio_path = os.path.join("recordings", f"{title}{ext}")

    with open(audio_path, "wb") as f:
        f.write(await file.read())

    job_id = str(uuid.uuid4())
    jobs[job_id] = {
        "status": "pending",
        "segments": [],
        "transcript": None,
        "output_file": None,
        "title": title,
        "error": None,
    }
    threading.Thread(target=run_voice_job, args=(job_id, audio_path, title, model), daemon=True).start()
    return {"job_id": job_id}


@app.get("/api/outputs")
def list_outputs():
    if not os.path.exists("outputs"):
        return {"files": []}
    files = sorted(os.listdir("outputs"), reverse=True)
    return {"files": [f for f in files if f.endswith(".txt")]}


@app.get("/api/outputs/{filename}")
def download_output(filename: str):
    path = os.path.join("outputs", filename)
    if not os.path.exists(path):
        return {"error": "File not found"}
    return FileResponse(path, media_type="text/plain", filename=filename)


@app.get("/")
def serve_index():
    return FileResponse("static/index.html")


app.mount("/static", StaticFiles(directory="static"), name="static")
