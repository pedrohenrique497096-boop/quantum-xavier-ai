
from fastapi import FastAPI
from core.scanner import scan_all

app = FastAPI()

@app.get("/signals")
def get_signals():
    return scan_all().to_dict(orient="records")
