from data.market import get_data
from core.market_hours import market_is_open
from core.engine import macro_bias, trend_bias
from config.settings import (
    WATCHLIST,
    TIMEFRAME_MACRO,
    TIMEFRAME_TREND,
    TIMEFRAME_ENTRY,
    HISTORY_MACRO,
    HISTORY_TREND,
    HISTORY_ENTRY,
)

def scan():
    results = []

    for symbol in WATCHLIST:
        try:
            if not market_is_open(symbol):
                continue

            macro_data = get_data(symbol, TIMEFRAME_MACRO, HISTORY_MACRO)
            trend_data = get_data(symbol, TIMEFRAME_TREND, HISTORY_TREND)
            entry_data = get_data(symbol, TIMEFRAME_ENTRY, HISTORY_ENTRY)

            if macro_data is None or trend_data is None or entry_data is None:
                continue

            macro = macro_bias(macro_data)
            trend = trend_bias(trend_data)

            side = "BUY" if macro == "bullish" and trend == "bullish" else "SELL"

            confidence = 80 if macro == trend else 65

            last_price = None
            if "Close" in entry_data.columns and len(entry_data) > 0:
                last_price = float(entry_data["Close"].iloc[-1])

            entry = last_price if last_price is not None else 0

            if side == "BUY":
                stop_loss = round(entry * 0.98, 2)
                take_profit = round(entry * 1.04, 2)
            else:
                stop_loss = round(entry * 1.02, 2)
                take_profit = round(entry * 0.96, 2)

            results.append({
                "symbol": symbol,
                "side": side,
                "confidence": confidence,
                "entry": entry,
                "stop_loss": stop_loss,
                "take_profit": take_profit
            })

        except Exception:
            continue

    return results
