from fastapi import FastAPI, UploadFile, File, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
import shutil
import uuid
import time
from yt_dlp import YoutubeDL

app = FastAPI()

UPLOAD_DIR = "static/uploads"
PROCESSED_DIR = "static/processed"
COOKIES_PATH = "static/cookies.txt"

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
        filename = f"{uuid.uuid4()}.mp4"
        upload_path = os.path.join(UPLOAD_DIR, filename)

        with open(upload_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        output_path = os.path.join(PROCESSED_DIR, f"processed_{filename}")
        time.sleep(2)
        shutil.copy(upload_path, output_path)

        return JSONResponse(content={"info": "Analisi completata", "output": output_path})
    except Exception as e:
        return JSONResponse(content={"error": f"Errore durante upload: {str(e)}"}, status_code=500)

@app.post("/youtube")
async def download_youtube(url: str = Form(...)):
    try:
        if not os.path.exists(COOKIES_PATH):
            return JSONResponse(content={"error": "cookies.txt non trovato in static/."}, status_code=400)

        ydl_opts = {
            'outtmpl': os.path.join(UPLOAD_DIR, '%(title)s.%(ext)s'),
            'format': 'bv*+ba/best',
            'cookiefile': COOKIES_PATH,
            'quiet': True,
            'merge_output_format': 'mp4',
            'postprocessors': [
                {
                    'key': 'FFmpegVideoConvertor',
                    'preferedformat': 'mp4'
                },
                {
                    'key': 'FFmpegVideoRemuxer',
                    'preferedformat': 'mp4'
                }
            ]
        }

        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            downloaded_file = ydl.prepare_filename(info)
            if not downloaded_file.endswith(".mp4"):
                downloaded_file = downloaded_file.rsplit(".", 1)[0] + ".mp4"

        processed_name = f"processed_{os.path.basename(downloaded_file)}"
        processed_path = os.path.join(PROCESSED_DIR, processed_name)
        time.sleep(2)
        shutil.copy(downloaded_file, processed_path)

        return JSONResponse(content={"info": "Analisi completata", "output": processed_path})
    except Exception as e:
        return JSONResponse(content={"error": f"Errore durante download: {str(e)}"}, status_code=500)
