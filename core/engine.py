from config.settings import ENTRY_LOOKBACK, RISK_REWARD
from core.indicators import ema, rsi, momentum, candle_strength, atr_like
from core.liquidity import liquidity_zones, stop_hunt


def macro_bias(df):
    if df is None or len(df) < 200:
        return "neutral"

    ema50 = ema(df["Close"], 50)
    ema200 = ema(df["Close"], 200)

    if ema50.iloc[-1] > ema200.iloc[-1]:
        return "bull"
    if ema50.iloc[-1] < ema200.iloc[-1]:
        return "bear"

    return "neutral"


def trend_bias(df):
    if df is None or len(df) < 50:
        return "neutral"

    ema20 = ema(df["Close"], 20)
    ema50 = ema(df["Close"], 50)
    last_rsi = float(rsi(df["Close"]).iloc[-1])
    mom = momentum(df["Close"], 5)

    if ema20.iloc[-1] > ema50.iloc[-1] and last_rsi >= 52 and mom > 0:
        return "bull"

    if ema20.iloc[-1] < ema50.iloc[-1] and last_rsi <= 48 and mom < 0:
        return "bear"

    return "neutral"


def build_entry_signal(df_m5, macro, trend):
    if df_m5 is None or len(df_m5) < ENTRY_LOOKBACK + 5:
        return None

    if macro != trend or macro == "neutral":
        return None

    last = df_m5.iloc[-1]
    price = float(last["Close"])
    structure_high = float(df_m5["High"].iloc[:-1].tail(ENTRY_LOOKBACK).max())
    structure_low = float(df_m5["Low"].iloc[:-1].tail(ENTRY_LOOKBACK).min())
    strength = candle_strength(df_m5)
    sweep = stop_hunt(df_m5)
    atr = atr_like(df_m5, 14)

    confidence = 50.0
    reasons = []

    if macro == "bull":
        if price > structure_high:
            confidence += 12
            reasons.append("Rompimento da estrutura M5")
        if sweep == "sell_liquidity_taken":
            confidence += 10
            reasons.append("Varredura de liquidez compradora")
        if strength > 0.55:
            confidence += 8
            reasons.append("Candle forte")

        if price <= structure_high:
            return None

        entry = price
        stop = min(structure_low, price - max(atr, price * 0.0015))
        target = entry + (entry - stop) * RISK_REWARD
        direction = "BUY"

    else:
        if price < structure_low:
            confidence += 12
            reasons.append("Perda da estrutura M5")
        if sweep == "buy_liquidity_taken":
            confidence += 10
            reasons.append("Varredura de liquidez vendedora")
        if strength > 0.55:
            confidence += 8
            reasons.append("Candle forte")

        if price >= structure_low:
            return None

        entry = price
        stop = max(structure_high, price + max(atr, price * 0.0015))
        target = entry - (stop - entry) * RISK_REWARD
        direction = "SELL"

    reasons.append(f"Bias D1: {macro}")
    reasons.append(f"Bias H1: {trend}")

    return {
        "direction": direction,
        "entry": float(entry),
        "stop": float(stop),
        "target": float(target),
        "confidence": float(min(confidence, 95)),
        "reason": " | ".join(reasons),
    }
