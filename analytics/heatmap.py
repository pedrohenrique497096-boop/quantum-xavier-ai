import pandas as pd


def market_heatmap(signals_df: pd.DataFrame):
    if signals_df is None or signals_df.empty:
        return {"buy": 0, "sell": 0}

    buy = int((signals_df["direction"] == "BUY").sum())
    sell = int((signals_df["direction"] == "SELL").sum())

    return {"buy": buy, "sell": sell}
