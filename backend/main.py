from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Serve React buildato
app.mount("/", StaticFiles(directory="frontend_dist", html=True), name="static")

@app.get("/ping")
def ping():
    return {"message": "pong"}
