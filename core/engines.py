import numpy as np

def breakout_engine(df):

    last = df.iloc[-1]
    prev = df.iloc[-2]

    score = 0

    if last.Close > prev.High:
        score += 40

    body = abs(last.Close - last.Open)
    rng = last.High - last.Low

    strength = body / rng

    score += strength * 30

    return score


def reversal_engine(df):

    last = df.iloc[-1]

    upper = last.High - max(last.Open, last.Close)
    lower = min(last.Open, last.Close) - last.Low

    rng = last.High - last.Low

    score_buy = lower / rng * 100
    score_sell = upper / rng * 100

    return score_buy, score_sell


def continuation_engine(df):

    closes = df.Close.values

    momentum = np.mean(np.diff(closes[-5:]))

    if momentum > 0:
        return momentum * 10000, 0
    else:
        return 0, abs(momentum) * 10000
