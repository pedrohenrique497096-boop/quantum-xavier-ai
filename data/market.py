import yfinance as yf

def get_data(symbol, interval="5m", bars=300):

    df = yf.download(
        symbol,
        interval=interval,
        period="7d",
        progress=False
    )

    if df is None or df.empty:
        return None

    df = df.tail(bars)

    return df
