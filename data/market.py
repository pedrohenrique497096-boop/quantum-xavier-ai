import pandas as pd
import yfinance as yf


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    if df is None or df.empty:
        return df

    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [c[0] if isinstance(c, tuple) else c for c in df.columns]

    rename = {}
    for c in df.columns:
        low = str(c).lower()
        if low == "open":
            rename[c] = "Open"
        elif low == "high":
            rename[c] = "High"
        elif low == "low":
            rename[c] = "Low"
        elif low == "close":
            rename[c] = "Close"
        elif low == "volume":
            rename[c] = "Volume"

    df = df.rename(columns=rename)
    return df


def get_data(symbol: str, interval: str = "5m", bars: int = 250):
    try:
        df = yf.download(
            tickers=symbol,
            period="7d",
            interval=interval,
            progress=False,
            auto_adjust=False,
            threads=False,
        )

        if df is None or df.empty:
            return None

        df = normalize_columns(df)

        required = ["Open", "High", "Low", "Close"]
        for col in required:
            if col not in df.columns:
                return None

        if "Volume" not in df.columns:
            df["Volume"] = 0

        df = df.dropna(subset=["Open", "High", "Low", "Close"]).copy()
        if df.empty:
            return None

        df = df.tail(bars).copy()
        return df

    except Exception:
        return None
