import requests
from config.settings import BINANCE_API, TWELVEDATA_API, TWELVEDATA_KEY

def get_price(symbol):

    if symbol == "BTCUSD":

        url=f"{BINANCE_API}/ticker/price?symbol=BTCUSDT"

        r=requests.get(url).json()

        return float(r["price"])

    else:

        url=f"{TWELVEDATA_API}/price?symbol={symbol}&apikey={TWELVEDATA_KEY}"

        r=requests.get(url).json()

        return float(r["price"])


def get_candles(symbol):

    if symbol=="BTCUSD":

        url=f"{BINANCE_API}/klines?symbol=BTCUSDT&interval=1m&limit=100"

        data=requests.get(url).json()

        candles=[]

        for c in data:

            candles.append({
                "time":c[0],
                "open":float(c[1]),
                "high":float(c[2]),
                "low":float(c[3]),
                "close":float(c[4]),
                "volume":float(c[5])
            })

        return candles
