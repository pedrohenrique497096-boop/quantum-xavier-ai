from data.market import get_data
from core.engines import (
    breakout_engine,
    reversal_engine,
    continuation_engine,
    volume_engine,
)
from core.signals import build_signal
from config.settings import TIMEFRAME, HISTORY, MIN_CONFIDENCE


def scan(symbol):
    df = get_data(symbol, interval=TIMEFRAME, bars=HISTORY)

    if df is None or len(df) < 10:
        return None

    try:
        breakout = breakout_engine(df)
        rev_buy, rev_sell = reversal_engine(df)
        cont_buy, cont_sell = continuation_engine(df)
        vol_buy, vol_sell = volume_engine(df)

        buy_score = breakout + rev_buy + cont_buy + vol_buy
        sell_score = rev_sell + cont_sell + vol_sell

        signal = build_signal(symbol, df, buy_score, sell_score)
        if signal is None:
            return None

        if signal["confidence"] < MIN_CONFIDENCE:
            return None

        return signal

    except Exception:
        return None
