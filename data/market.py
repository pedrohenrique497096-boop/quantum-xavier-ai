import yfinance as yf

def get_data(symbol, interval="5m", bars=500):

    try:

        df = yf.download(
            symbol,
            interval=interval,
            period="60d",
            progress=False
        )

        if df is None or df.empty:
            return None

        return df.tail(bars)

    except:
        return None
