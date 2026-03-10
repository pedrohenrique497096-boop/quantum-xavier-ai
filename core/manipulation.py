def detect_manipulation(candles):

    last = candles[-1]
    prev = candles[-2]

    body = abs(last["close"] - last["open"])
    wick = last["high"] - last["low"]

    if wick > body * 3:
        return True

    return False
