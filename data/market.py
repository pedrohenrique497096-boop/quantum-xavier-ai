import requests

TWELVEDATA_API_KEY = "COLOQUE_SUA_API_KEY_AQUI"

def get_price(symbol):

    mapping = {
        "BTCUSD": "BTC/USD",
        "XAUUSD": "XAU/USD",
        "EURUSD": "EUR/USD",
        "GBPUSD": "GBP/USD",
        "USDJPY": "USD/JPY",
        "EURJPY": "EUR/JPY"
    }

    if symbol not in mapping:
        return {"error": "symbol not supported"}

    td_symbol = mapping[symbol]

    url = f"https://api.twelvedata.com/price?symbol={td_symbol}&apikey={TWELVEDATA_API_KEY}"

    r = requests.get(url)

    data = r.json()

    if "price" not in data:
        return {"error": data}

    return {
        "symbol": symbol,
        "price": float(data["price"])
    }
