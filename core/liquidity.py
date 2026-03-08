from config.settings import LIQUIDITY_LOOKBACK


def liquidity_zones(df):
    if df is None or len(df) < LIQUIDITY_LOOKBACK + 1:
        return None, None

    ref = df.iloc[:-1].tail(LIQUIDITY_LOOKBACK)
    high_zone = float(ref["High"].max())
    low_zone = float(ref["Low"].min())

    return high_zone, low_zone


def stop_hunt(df):
    if df is None or len(df) < LIQUIDITY_LOOKBACK + 1:
        return "neutral"

    high_zone, low_zone = liquidity_zones(df)
    last = df.iloc[-1]

    if high_zone is None or low_zone is None:
        return "neutral"

    if float(last["High"]) > high_zone and float(last["Close"]) < high_zone:
        return "buy_liquidity_taken"

    if float(last["Low"]) < low_zone and float(last["Close"]) > low_zone:
        return "sell_liquidity_taken"

    return "neutral"
