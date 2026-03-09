from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Quantum Xavier API",
    version="1.0"
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

@app.get("/scan")
def scan_market():
    return [
        {
            "symbol": "BTC/USD",
            "signal": "BUY",
            "entry": 67842.50,
            "stop_loss": 65200.00,
            "take_profit": 72500.00,
            "confidence": 92
        },
        {
            "symbol": "ETH/USD",
            "signal": "BUY",
            "entry": 3521.75,
            "stop_loss": 3380.00,
            "take_profit": 3820.00,
            "confidence": 87
        }
    ]
