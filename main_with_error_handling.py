from fastapi import FastAPI, UploadFile, File, Form, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
import shutil
import uuid
import subprocess
import time

app = FastAPI()

UPLOAD_DIR = "static/uploads"
PROCESSED_DIR = "static/processed"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    try:
        if not file:
            raise HTTPException(status_code=400, detail="Nessun file ricevuto.")
        filename = f"{uuid.uuid4()}.mp4"
        upload_path = os.path.join(UPLOAD_DIR, filename)

        with open(upload_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Analisi automatica simulata
        output_path = os.path.join(PROCESSED_DIR, f"processed_{filename}")
        time.sleep(2)
        shutil.copy(upload_path, output_path)

        return {"info": "Analisi completata", "output": output_path}
    except Exception as e:
        return {"error": f"Errore durante upload: {str(e)}"}

@app.post("/youtube")
async def download_youtube(url: str = Form(...)):
    try:
        filename = f"{uuid.uuid4()}.mp4"
        output_path = os.path.join(UPLOAD_DIR, filename)
        command = ["yt-dlp", "-o", output_path, url]
        subprocess.run(command)

        # Analisi automatica simulata
        processed_path = os.path.join(PROCESSED_DIR, f"processed_{filename}")
        time.sleep(2)
        shutil.copy(output_path, processed_path)

        return {"info": "Analisi completata", "output": processed_path}
    except Exception as e:
        return {"error": f"Errore durante download: {str(e)}"}
