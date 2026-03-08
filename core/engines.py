import numpy as np


def breakout_engine(df):
    if df is None or len(df) < 2:
        return 0

    last = df.iloc[-1]
    prev = df.iloc[-2]

    close = float(last["Close"])
    open_ = float(last["Open"])
    high = float(last["High"])
    low = float(last["Low"])
    prev_high = float(prev["High"])

    score = 0

    if close > prev_high:
        score += 40

    body = abs(close - open_)
    rng = high - low

    if rng <= 0:
        return score

    strength = body / rng
    score += strength * 30

    return float(score)


def reversal_engine(df):
    if df is None or len(df) < 1:
        return 0, 0

    last = df.iloc[-1]

    high = float(last["High"])
    low = float(last["Low"])
    close = float(last["Close"])
    open_ = float(last["Open"])

    upper = high - max(open_, close)
    lower = min(open_, close) - low
    rng = high - low

    if rng <= 0:
        return 0, 0

    score_buy = lower / rng * 100
    score_sell = upper / rng * 100

    return float(score_buy), float(score_sell)


def continuation_engine(df):
    if df is None or len(df) < 5:
        return 0, 0

    closes = df["Close"].astype(float).values

    if len(closes) < 5:
        return 0, 0

    diffs = np.diff(closes[-5:])
    if len(diffs) == 0:
        return 0, 0

    momentum = float(np.mean(diffs))

    if momentum > 0:
        return momentum * 10000, 0
    return 0, abs(momentum) * 10000


def volume_engine(df):
    if df is None or len(df) < 10 or "Volume" not in df.columns:
        return 0, 0

    vols = df["Volume"].astype(float).values
    current = vols[-1]
    avg = np.mean(vols[-10:]) if len(vols[-10:]) else 0

    if avg <= 0:
        return 0, 0

    ratio = current / avg

    bonus = min(ratio * 10, 20)
    return float(bonus), float(bonus)
