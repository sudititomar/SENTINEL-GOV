from fastapi import FastAPI
from backend.routes import router

app = FastAPI(title="Sentinel-Gov")

@app.get("/")
def root():
    return {"status": "Sentinel-Gov backend running"}

app.include_router(router)