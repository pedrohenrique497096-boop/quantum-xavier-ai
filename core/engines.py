import numpy as np

def breakout_engine(df):

    last = df.iloc[-1]
    prev = df.iloc[-2]

    close = last["Close"]
    open_ = last["Open"]
    high = last["High"]
    low = last["Low"]

    prev_high = prev["High"]

    score = 0

    if close > prev_high:
        score += 40

    body = abs(close - open_)
    rng = high - low

    if rng == 0:
        return score

    strength = body / rng

    score += strength * 30

    return score


def reversal_engine(df):

    last = df.iloc[-1]

    high = last["High"]
    low = last["Low"]
    close = last["Close"]
    open_ = last["Open"]

    upper = high - max(open_, close)
    lower = min(open_, close) - low

    rng = high - low

    if rng == 0:
        return 0, 0

    score_buy = lower / rng * 100
    score_sell = upper / rng * 100

    return score_buy, score_sell


def continuation_engine(df):

    closes = df["Close"].values

    if len(closes) < 5:
        return 0, 0

    momentum = np.mean(np.diff(closes[-5:]))

    if momentum > 0:
        return momentum * 10000, 0
    else:
        return 0, abs(momentum) * 10000
