import yfinance as yf
import pandas as pd


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    if df is None or df.empty:
        return df

    # Se vier MultiIndex, achata
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [col[0] if isinstance(col, tuple) else col for col in df.columns]

    rename_map = {}
    for col in df.columns:
        low = str(col).lower()
        if low == "open":
            rename_map[col] = "Open"
        elif low == "high":
            rename_map[col] = "High"
        elif low == "low":
            rename_map[col] = "Low"
        elif low == "close":
            rename_map[col] = "Close"
        elif low == "volume":
            rename_map[col] = "Volume"

    df = df.rename(columns=rename_map)
    return df


def get_data(symbol, interval="5m", bars=300):
    try:
        df = yf.download(
            symbol,
            interval=interval,
            period="7d",
            progress=False,
            auto_adjust=False,
            threads=False
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
