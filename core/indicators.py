import numpy as np
import pandas as pd


def ema(series: pd.Series, length: int) -> pd.Series:
    return series.ewm(span=length, adjust=False).mean()


def rsi(series: pd.Series, length: int = 14) -> pd.Series:
    delta = series.diff()

    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(length).mean()
    avg_loss = loss.rolling(length).mean()

    rs = avg_gain / avg_loss.replace(0, np.nan)
    out = 100 - (100 / (1 + rs))
    return out.fillna(50)


def momentum(series: pd.Series, lookback: int = 5) -> float:
    if len(series) < lookback + 1:
        return 0.0
    return float(series.iloc[-1] - series.iloc[-lookback])


def candle_strength(df: pd.DataFrame) -> float:
    if df is None or len(df) == 0:
        return 0.0

    last = df.iloc[-1]
    body = abs(float(last["Close"]) - float(last["Open"]))
    rng = float(last["High"]) - float(last["Low"])

    if rng <= 0:
        return 0.0

    return float(body / rng)


def atr_like(df: pd.DataFrame, lookback: int = 14) -> float:
    if df is None or len(df) < lookback:
        return 0.0
    return float((df["High"] - df["Low"]).tail(lookback).mean())
