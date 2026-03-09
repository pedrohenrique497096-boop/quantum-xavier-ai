from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.scanner import scan

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "online", "app": "Quantum Xavier API"}

@app.get("/scan")
def run_scan():
    data = scan()
    return data

@app.get("/health")
def health():
    return {"status": "ok"}
