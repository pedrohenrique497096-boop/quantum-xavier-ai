from config.settings import ASSETS
from data.market import get_candles,get_price
from core.engine import analyze_market

def scan_market():

    signals=[]

    for asset in ASSETS:

        candles=get_candles(asset)

        price=get_price(asset)

        signal=analyze_market(asset,candles,price)

        if signal["confidence"]>65:

            signals.append(signal)

    return signals
