from data.market import get_data
from core.engine import macro_bias, trend_bias
from core.liquidity import liquidity_zones

from config.settings import (
    TIMEFRAME_MACRO,
    TIMEFRAME_TREND,
    TIMEFRAME_ENTRY,
    HISTORY
)

def scan(symbol):

    d1 = get_data(symbol,TIMEFRAME_MACRO,HISTORY)
    h1 = get_data(symbol,TIMEFRAME_TREND,HISTORY)
    m5 = get_data(symbol,TIMEFRAME_ENTRY,HISTORY)

    if d1 is None or h1 is None or m5 is None:
        return None

    macro = macro_bias(d1)
    trend = trend_bias(h1)

    if macro != trend:
        return None

    high, low = liquidity_zones(m5)

    last = m5.iloc[-1]["Close"]

    if macro=="bull" and last>high:

        return {
            "symbol":symbol,
            "direction":"BUY",
            "entry":high,
            "stop":low
        }

    if macro=="bear" and last<low:

        return {
            "symbol":symbol,
            "direction":"SELL",
            "entry":low,
            "stop":high
        }

    return None
