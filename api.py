from fastapi import FastAPI
from core.scanner import scan

app = FastAPI(
    title="Quantum Xavier AI",
    description="AI institucional de análise de mercado",
    version="1.0"
)

@app.get("/")
def home():
    return {
        "AI": "Quantum Xavier",
        "status": "online",
        "version": "v12",
        "message": "Sistema funcionando"
    }

@app.get("/scan")
def run_scan():
    try:
        scan()
        return {
            "scan": "executado com sucesso"
        }
    except Exception as e:
        return {
            "erro": str(e)
        }
