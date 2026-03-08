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
from core.engine import macro_bias, trend_bias, build_entry_signal
from ai.model import adaptive_confidence_boost
from database.trades import (
    load_open_trades,
    close_trade,
)


def evaluate_open_trades():
    open_df = load_open_trades()
    if open_df.empty:
        return

    for _, row in open_df.iterrows():
        symbol = row["symbol"]
        df = get_data(symbol, TIMEFRAME_ENTRY, 50)

        if df is None or df.empty:
            continue

        last = df.iloc[-1]
        high = float(last["High"])
        low = float(last["Low"])

        if row["direction"] == "BUY":
            if low <= float(row["stop"]):
                close_trade(int(row["id"]), "STOP")
            elif high >= float(row["target"]):
                close_trade(int(row["id"]), "TP")

        elif row["direction"] == "SELL":
            if high >= float(row["stop"]):
                close_trade(int(row["id"]), "STOP")
            elif low <= float(row["target"]):
                close_trade(int(row["id"]), "TP")


def scan_all():
    results = []

    boost = adaptive_confidence_boost()

    for symbol in WATCHLIST:
        display_symbol = SYMBOL_NAMES.get(symbol, symbol)

        if not market_is_open(symbol):
            results.append({
                "symbol": symbol,
                "display_symbol": display_symbol,
                "market_status": "Fechado",
                "direction": "-",
                "entry": None,
                "stop": None,
                "target": None,
                "confidence": 0.0,
                "reason": "Mercado fechado neste horário",
            })
            continue

        d1 = get_data(symbol, TIMEFRAME_MACRO, HISTORY_MACRO)
        h1 = get_data(symbol, TIMEFRAME_TREND, HISTORY_TREND)
        m5 = get_data(symbol, TIMEFRAME_ENTRY, HISTORY_ENTRY)

        if d1 is None or h1 is None or m5 is None:
            results.append({
                "symbol": symbol,
                "display_symbol": display_symbol,
                "market_status": "Sem dados",
                "direction": "-",
                "entry": None,
                "stop": None,
                "target": None,
                "confidence": 0.0,
                "reason": "Dados insuficientes",
            })
            continue

        macro = macro_bias(d1)
        trend = trend_bias(h1)

        signal = build_entry_signal(m5, macro, trend)

        if signal is None:
            results.append({
                "symbol": symbol,
                "display_symbol": display_symbol,
                "market_status": "Aberto",
                "direction": "-",
                "entry": None,
                "stop": None,
                "target": None,
                "confidence": 0.0,
                "reason": f"Sem gatilho M5 | Bias D1: {macro} | Bias H1: {trend}",
            })
            continue

        signal["symbol"] = symbol
        signal["display_symbol"] = display_symbol
        signal["market_status"] = "Aberto"
        signal["confidence"] = round(max(0.0, min(95.0, signal["confidence"] + boost)), 2)

        if signal["confidence"] < MIN_CONFIDENCE:
            signal["direction"] = "-"
            signal["entry"] = None
            signal["stop"] = None
            signal["target"] = None
            signal["reason"] = "Sinal descartado por confiança insuficiente"
            results.append(signal)
            continue

        results.append(signal)

    df = pd.DataFrame(results)

    if not df.empty:
        df = df.sort_values(by=["confidence", "display_symbol"], ascending=[False, True]).reset_index(drop=True)

    return df
