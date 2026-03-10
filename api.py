from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from data.market import get_price, get_candles

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
    return {"api": "Quantum Xavier AI", "status": "online"}


@app.get("/price/{symbol}")
def price(symbol: str):
    try:
        return {
            "symbol": symbol,
            "price": get_price(symbol),
        }
    except Exception as e:
        return {"error": str(e)}


@app.get("/chart/{symbol}")
def chart(symbol: str):
    try:
        return {
            "symbol": symbol,
            "candles": get_candles(symbol),
        }
    except Exception as e:
        return {"error": str(e)}


@app.get("/signals")
def signals():
    # temporário: retorna lista vazia até conectar com scanner/engine
    return []
