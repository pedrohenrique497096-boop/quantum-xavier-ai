import pandas as pd
import yfinance as yf


def _normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    if df is None or df.empty:
        return df

    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [c[0] if isinstance(c, tuple) else c for c in df.columns]

    rename_map = {}
    for c in df.columns:
        low = str(c).lower()
        if low == "open":
            rename_map[c] = "Open"
        elif low == "high":
            rename_map[c] = "High"
        elif low == "low":
            rename_map[c] = "Low"
        elif low == "close":
            rename_map[c] = "Close"
        elif low == "volume":
            rename_map[c] = "Volume"

    df = df.rename(columns=rename_map)
    return df


def get_data(symbol: str, interval: str = "5m", bars: int = 300):
    try:
        period_map = {
            "1d": "2y",
            "1h": "90d",
            "5m": "10d",
            "1m": "7d",
        }

        df = yf.download(
            tickers=symbol,
            interval=interval,
            period=period_map.get(interval, "60d"),
            progress=False,
            auto_adjust=False,
            threads=False,
        )

        if df is None or df.empty:
            return None

        df = _normalize_columns(df)

        needed = ["Open", "High", "Low", "Close"]
        for col in needed:
            if col not in df.columns:
                return None

        if "Volume" not in df.columns:
            df["Volume"] = 0.0

        df = df.dropna(subset=["Open", "High", "Low", "Close"]).copy()
        if df.empty:
            return None

        return df.tail(bars).copy()

    except Exception:
        return None
