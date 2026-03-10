def detect_orderflow(candles):

    volumes = [c["volume"] for c in candles]

    avg = sum(volumes[:-1]) / len(volumes[:-1])

    last = volumes[-1]

    if last > avg * 2:
        return "strong_volume"

    return "normal"
