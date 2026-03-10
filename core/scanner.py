from config.settings import ASSETS
from data.market import get_price, get_candles
from core.engine import analyze_market


def scan_market():

    signals = []

    for asset in ASSETS:

        try:

            candles = get_candles(asset)

            price = get_price(asset)

            result = analyze_market(
                symbol=asset,
                candles=candles,
                price=price
            )

            if result and result["confidence"] >= 70:
                signals.append(result)

        except Exception as e:
            print(f"Erro analisando {asset}: {e}")

    return signals
