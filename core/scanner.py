from config.settings import TIMEFRAME, HISTORY, MIN_CONFIDENCE
from data.market import get_data
from core.engines import (
    breakout_engine,
    reversal_engine,
    continuation_engine,
    volume_engine,
    explain_signal,
)
from core.signals import build_signal


def scan(symbol: str):
    df = get_data(symbol, interval=TIMEFRAME, bars=HISTORY)

    if df is None or len(df) < 10:
        return None, None

    try:
        breakout_buy, breakout_sell, breakout_reason = breakout_engine(df)
        rev_buy, rev_sell, rev_reason = reversal_engine(df)
        cont_buy, cont_sell, cont_reason = continuation_engine(df)
        vol_buy, vol_sell, vol_reason = volume_engine(df)

        buy_score = breakout_buy + rev_buy + cont_buy + vol_buy
        sell_score = breakout_sell + rev_sell + cont_sell + vol_sell

        direction = "BUY" if buy_score >= sell_score else "SELL"
        confidence = buy_score if direction == "BUY" else sell_score

        explanation = explain_signal(
            direction=direction,
            confidence=confidence,
            reasons=[breakout_reason, rev_reason, cont_reason, vol_reason]
        )

        signal = build_signal(symbol, df, buy_score, sell_score, explanation)
        if signal is None:
            return None, df

        if signal["confidence"] < MIN_CONFIDENCE:
            return None, df

        return signal, df

    except Exception:
        return None, df
