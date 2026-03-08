from config.settings import RISK_REWARD

def build_signal(symbol, df, buy_score, sell_score):

    last = df.iloc[-1]

    if buy_score > sell_score:

        entry = last.High
        stop = last.Low
        target = entry + (entry - stop) * RISK_REWARD

        direction = "BUY"
        confidence = buy_score

    else:

        entry = last.Low
        stop = last.High
        target = entry - (stop - entry) * RISK_REWARD

        direction = "SELL"
        confidence = sell_score

    return {
        "symbol": symbol,
        "direction": direction,
        "entry": entry,
        "stop": stop,
        "target": target,
        "confidence": confidence
    }
