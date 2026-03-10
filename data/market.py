import requests
from config.settings import BINANCE_API, TWELVEDATA_API, TWELVEDATA_KEY


SUPPORTED_ASSETS = {
    "BTCUSD": "BTC/USD",
    "XAUUSD": "XAU/USD",
    "EURUSD": "EUR/USD",
    "GBPUSD": "GBP/USD",
    "USDJPY": "USD/JPY",
    "EURJPY": "EUR/JPY",
}


def get_price(symbol: str) -> float:
    if symbol not in SUPPORTED_ASSETS:
        raise ValueError(f"Ativo não suportado: {symbol}")

    if symbol == "BTCUSD":
        url = f"{BINANCE_API}/ticker/price?symbol=BTCUSDT"
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        data = response.json()

        if "price" not in data:
            raise ValueError(f"Resposta inválida da Binance: {data}")

        return float(data["price"])

    td_symbol = SUPPORTED_ASSETS[symbol]
    url = f"{TWELVEDATA_API}/price?symbol={td_symbol}&apikey={TWELVEDATA_KEY}"
    response = requests.get(url, timeout=15)
    response.raise_for_status()
    data = response.json()

    if "price" not in data:
        raise ValueError(f"Resposta inválida da TwelveData: {data}")

    return float(data["price"])


def get_candles(symbol: str, interval: str = "1min", outputsize: int = 30):
    if symbol not in SUPPORTED_ASSETS:
        raise ValueError(f"Ativo não suportado: {symbol}")

    if symbol == "BTCUSD":
        binance_interval_map = {
            "1min": "1m",
            "5min": "5m",
            "15min": "15m",
            "1h": "1h",
        }
        binance_interval = binance_interval_map.get(interval, "1m")

        url = (
            f"{BINANCE_API}/klines?"
            f"symbol=BTCUSDT&interval={binance_interval}&limit={outputsize}"
        )

        response = requests.get(url, timeout=15)
        response.raise_for_status()
        data = response.json()

        candles = []
        for item in data:
            candles.append(
                {
                    "datetime": item[0],
                    "open": float(item[1]),
                    "high": float(item[2]),
                    "low": float(item[3]),
                    "close": float(item[4]),
                    "volume": float(item[5]),
                }
            )

        return candles

    td_symbol = SUPPORTED_ASSETS[symbol]
    url = f"{TWELVEDATA_API}/time_series"
    params = {
        "symbol": td_symbol,
        "interval": interval,
        "outputsize": outputsize,
        "apikey": TWELVEDATA_KEY,
    }

    response = requests.get(url, params=params, timeout=15)
    response.raise_for_status()
    data = response.json()

    if "values" not in data:
        raise ValueError(f"Resposta inválida da TwelveData: {data}")

    candles = []
    for item in reversed(data["values"]):
        candles.append(
            {
                "datetime": item["datetime"],
                "open": float(item["open"]),
                "high": float(item["high"]),
                "low": float(item["low"]),
                "close": float(item["close"]),
                "volume": float(item.get("volume", 0) or 0),
            }
        )

    return candles
