from fastapi import FastAPI
from core.scanner import scan

app = FastAPI()

@app.get("/")
def home():
    return {"Quantum Xavier AI": "online"}

@app.get("/signals")
def signals():
    return scan().to_dict(orient="records")
