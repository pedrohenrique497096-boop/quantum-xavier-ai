from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.scanner import scan

app = FastAPI(
    title="Quantum Xavier API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {
        "status": "online",
        "app": "Quantum Xavier API"
    }

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }

@app.get("/scan")
def get_scan():
    try:
        data = scan()

        if data is None:
            return []

        if isinstance(data, list):
            return data

        return []
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
