import requests
from config.settings import TWELVEDATA_API, TWELVEDATA_KEY


def get_price(symbol):

    url = f"{TWELVEDATA_API}/price"

    params = {
        "symbol": symbol,
        "apikey": TWELVEDATA_KEY
    }

    r = requests.get(url, params=params)

    data = r.json()

    return float(data["price"])


def get_candles(symbol):

    url = f"{TWELVEDATA_API}/time_series"

    params = {
        "symbol": symbol,
        "interval": "1min",
        "outputsize": 100,
        "apikey": TWELVEDATA_KEY
    }

    r = requests.get(url, params=params)

    data = r.json()

    candles = []

    if "values" in data:

        for c in data["values"]:

            candles.append({
                "datetime": c["datetime"],
                "open": float(c["open"]),
                "high": float(c["high"]),
                "low": float(c["low"]),
                "close": float(c["close"])
            })

    return candles
