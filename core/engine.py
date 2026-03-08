from core.indicators import ema, rsi

def macro_bias(df):

    ema50 = ema(df["Close"],50)
    ema200 = ema(df["Close"],200)

    if ema50.iloc[-1] > ema200.iloc[-1]:
        return "bull"

    return "bear"


def trend_bias(df):

    r = rsi(df["Close"])

    if r.iloc[-1] > 55:
        return "bull"

    if r.iloc[-1] < 45:
        return "bear"

    return "neutral"
