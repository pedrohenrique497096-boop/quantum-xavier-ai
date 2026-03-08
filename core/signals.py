import math
from config.settings import RISK_REWARD


def clean_score(x):
    try:
        x = float(x)
        if math.isnan(x) or math.isinf(x):
            return 0.0
        return x
    except Exception:
        return 0.0


def build_signal(symbol, df, buy_score, sell_score, explanation=""):
    if df is None or len(df) < 1:
        return None

    last = df.iloc[-1]

    high_ = float(last["High"])
    low_ = float(last["Low"])
    close_ = float(last["Close"])

    buy_score = clean_score(buy_score)
    sell_score = clean_score(sell_score)

    if high_ <= low_:
        return None

    if buy_score >= sell_score:
        direction = "BUY"
        entry = high_
        stop = low_
        target = entry + (entry - stop) * RISK_REWARD
        confidence = buy_score
    else:
        direction = "SELL"
        entry = low_
        stop = high_
        target = entry - (stop - entry) * RISK_REWARD
        confidence = sell_score

    return {
        "symbol": symbol,
        "direction": direction,
        "entry": float(entry),
        "stop": float(stop),
        "target": float(target),
        "close": float(close_),
        "confidence": float(confidence),
        "reason": explanation,
        "status": "OPEN",
    }
