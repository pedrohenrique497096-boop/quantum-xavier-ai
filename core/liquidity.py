def liquidity_zones(df):

    highs = df["High"].tail(20)
    lows = df["Low"].tail(20)

    return highs.max(), lows.min()
