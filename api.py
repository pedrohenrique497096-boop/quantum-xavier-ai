from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()

# ===============================
# CONFIG
# ===============================

TWELVEDATA_API_KEY = "1bbb904ae0994fb7b2d120da18c66602"

SUPPORTED_ASSETS = {
    "BTCUSD": "BTC/USD",
    "XAUUSD": "XAU/USD",
    "EURUSD": "EUR/USD",
    "GBPUSD": "GBP/USD",
    "USDJPY": "USD/JPY",
    "EURJPY": "EUR/JPY"
}

# ===============================
# CORS (para o app acessar)
# ===============================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===============================
# STATUS API
# ===============================

@app.get("/")
def status():
    return {
        "api": "Quantum Xavier AI",
        "status": "online"
    }

# ===============================
# PREÇO ATUAL
# ===============================

@app.get("/price/{symbol}")
def get_price(symbol: str):

    if symbol not in SUPPORTED_ASSETS:
        return {"error": "Asset not supported"}

    td_symbol = SUPPORTED_ASSETS[symbol]

    url = f"https://api.twelvedata.com/price?symbol={td_symbol}&apikey={TWELVEDATA_API_KEY}"

    response = requests.get(url)

    data = response.json()

    if "price" not in data:
        return {
            "error": "Market data unavailable",
            "data": data
        }

    return {
        "symbol": symbol,
        "price": float(data["price"])
    }

# ===============================
# GERADOR DE SINAIS (SIMPLES)
# ===============================

@app.get("/signals")
def get_signals():

    signals = []

    for symbol in SUPPORTED_ASSETS:

        td_symbol = SUPPORTED_ASSETS[symbol]

        url = f"https://api.twelvedata.com/price?symbol={td_symbol}&apikey={TWELVEDATA_API_KEY}"

        r = requests.get(url)

        data = r.json()

        if "price" not in data:
            continue

        price = float(data["price"])

        signal = {
            "asset": symbol,
            "direction": "BUY",
            "entry": round(price, 2),
            "stop_loss": round(price * 0.99, 2),
            "take_profit_1": round(price * 1.01, 2),
            "take_profit_2": round(price * 1.02, 2),
            "take_profit_3": round(price * 1.03, 2),
            "confidence": 80
        }

        signals.append(signal)

    return signals

# ===============================
# DADOS DE GRÁFICO
# ===============================

@app.get("/chart/{symbol}")
def get_chart(symbol: str):

    if symbol not in SUPPORTED_ASSETS:
        return {"error": "Asset not supported"}

    td_symbol = SUPPORTED_ASSETS[symbol]

    url = f"https://api.twelvedata.com/time_series?symbol={td_symbol}&interval=1min&outputsize=30&apikey={TWELVEDATA_API_KEY}"

    r = requests.get(url)

    data = r.json()

    if "values" not in data:
        return {"error": "chart unavailable"}

    return {
        "symbol": symbol,
        "candles": data["values"]
    }
