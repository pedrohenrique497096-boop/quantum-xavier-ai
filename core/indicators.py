def ema(series,length):

    return series.ewm(span=length).mean()


def rsi(series,length=14):

    delta = series.diff()

    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(length).mean()
    avg_loss = loss.rolling(length).mean()

    rs = avg_gain / avg_loss

    return 100 - (100/(1+rs))
