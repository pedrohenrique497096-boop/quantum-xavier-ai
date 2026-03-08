from config.settings import RISK_REWARD


def build_signal(symbol, df, buy_score, sell_score):
    if df is None or len(df) < 1:
        return None

    last = df.iloc[-1]

    high = float(last["High"])
    low = float(last["Low"])
    close = float(last["Close"])

    if high <= low:
        return None

    if buy_score > sell_score:
        entry = high
        stop = low
        target = entry + (entry - stop) * RISK_REWARD
        direction = "BUY"
        confidence = float(buy_score)
    else:
        entry = low
        stop = high
        target = entry - (stop - entry) * RISK_REWARD
        direction = "SELL"
        confidence = float(sell_score)

    reason = (
        f"Sinal {direction} | "
        f"confiança={confidence:.2f} | "
        f"preço={close:.5f}"
    )

    return {
        "symbol": symbol,
        "direction": direction,
        "entry": float(entry),
        "stop": float(stop),
        "target": float(target),
        "confidence": float(confidence),
        "reason": reason,
        "status": "OPEN"
    }
