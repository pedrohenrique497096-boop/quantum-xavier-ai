def detect_liquidity_pools(candles):

    highs = [c["high"] for c in candles]
    lows = [c["low"] for c in candles]

    liquidity_zones = []

    for i in range(5, len(highs)):

        if abs(highs[i] - highs[i-1]) < 0.001:
            liquidity_zones.append({
                "type": "sell_liquidity",
                "price": highs[i]
            })

        if abs(lows[i] - lows[i-1]) < 0.001:
            liquidity_zones.append({
                "type": "buy_liquidity",
                "price": lows[i]
            })

    return liquidity_zones
