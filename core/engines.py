import math
import numpy as np


def safe_float(v, default=0.0):
    try:
        x = float(v)
        if math.isnan(x) or math.isinf(x):
            return default
        return x
    except Exception:
        return default


def breakout_engine(df):
    if df is None or len(df) < 3:
        return 0.0, 0.0, "Sem barras suficientes para rompimento."

    last = df.iloc[-1]
    prev = df.iloc[-2]

    close_ = safe_float(last["Close"])
    open_ = safe_float(last["Open"])
    high_ = safe_float(last["High"])
    low_ = safe_float(last["Low"])
    prev_high = safe_float(prev["High"])
    prev_low = safe_float(prev["Low"])

    rng = high_ - low_
    if rng <= 0:
        return 0.0, 0.0, "Range inválido no candle."

    body = abs(close_ - open_)
    strength = body / rng

    buy = 0.0
    sell = 0.0

    if close_ > prev_high:
        buy += 35
    if close_ < prev_low:
        sell += 35

    if close_ > open_:
        buy += strength * 25
    else:
        sell += strength * 25

    reason = f"Rompimento | força candle={strength:.2f}"
    return buy, sell, reason


def reversal_engine(df):
    if df is None or len(df) < 3:
        return 0.0, 0.0, "Sem barras suficientes para reversão."

    last = df.iloc[-1]

    high_ = safe_float(last["High"])
    low_ = safe_float(last["Low"])
    close_ = safe_float(last["Close"])
    open_ = safe_float(last["Open"])

    rng = high_ - low_
    if rng <= 0:
        return 0.0, 0.0, "Range inválido no candle."

    upper_wick = high_ - max(open_, close_)
    lower_wick = min(open_, close_) - low_

    buy = (lower_wick / rng) * 100
    sell = (upper_wick / rng) * 100

    reason = f"Reversão | pavio inferior={lower_wick/rng:.2f} | pavio superior={upper_wick/rng:.2f}"
    return buy, sell, reason


def continuation_engine(df):
    if df is None or len(df) < 6:
        return 0.0, 0.0, "Sem barras suficientes para continuação."

    closes = df["Close"].astype(float).values
    diffs = np.diff(closes[-5:])
    if len(diffs) == 0:
        return 0.0, 0.0, "Sem momentum."

    momentum = float(np.mean(diffs))

    buy = max(momentum * 10000, 0.0)
    sell = max(abs(momentum) * 10000, 0.0) if momentum < 0 else 0.0

    reason = f"Continuação | momentum={momentum:.6f}"
    return buy, sell, reason


def volume_engine(df):
    if df is None or len(df) < 10 or "Volume" not in df.columns:
        return 0.0, 0.0, "Sem volume suficiente."

    vols = df["Volume"].astype(float).values
    current = safe_float(vols[-1])
    avg = safe_float(np.mean(vols[-10:]))

    if avg <= 0:
        return 0.0, 0.0, "Volume não disponível."

    ratio = current / avg
    bonus = min(ratio * 10, 20)

    reason = f"Volume | razão={ratio:.2f}x"
    return bonus, bonus, reason


def explain_signal(direction: str, confidence: float, reasons: list[str]) -> str:
    reasons_text = " | ".join(reasons[:4])
    if direction == "BUY":
        return f"Sinal comprador com confiança {confidence:.2f}. Motivos: {reasons_text}."
    return f"Sinal vendedor com confiança {confidence:.2f}. Motivos: {reasons_text}."
