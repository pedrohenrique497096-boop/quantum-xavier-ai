import pandas as pd

from config.settings import (
    WATCHLIST,
    SYMBOL_NAMES,
    TIMEFRAME_MACRO,
    TIMEFRAME_TREND,
    TIMEFRAME_ENTRY,
    HISTORY_MACRO,
    HISTORY_TREND,
    HISTORY_ENTRY,
    MIN_CONFIDENCE,
)

from data.market import get_data
from core.market_hours import market_is_open
from core.engine import macro_bias, trend_bias
from ai.model import adaptive_confidence_boost
from database.trades import (
    load_open_trades,
    close_trade,
)


def evaluate_open_trades():
    open_df = load_open_trades()

    if open_df is None or open_df.empty:
        return

    for index, trade in open_df.iterrows():
        # lógica simples de fechamento
        close_trade(trade["id"])


def scan():

    if not market_is_open():
        return {"status": "market closed"}

    results = []

    for symbol in WATCHLIST:

        macro_data = get_data(symbol, TIMEFRAME_MACRO, HISTORY_MACRO)
        trend_data = get_data(symbol, TIMEFRAME_TREND, HISTORY_TREND)
        entry_data = get_data(symbol, TIMEFRAME_ENTRY, HISTORY_ENTRY)

        if macro_data is None or trend_data is None or entry_data is None:
            continue

        macro = macro_bias(macro_data)
        trend = trend_bias(trend_data)

        confidence = adaptive_confidence_boost(macro, trend)

        if confidence >= MIN_CONFIDENCE:
            results.append({
                "symbol": symbol,
                "name": SYMBOL_NAMES.get(symbol, symbol),
                "macro": macro,
                "trend": trend,
                "confidence": confidence
            })

    evaluate_open_trades()

    return results
