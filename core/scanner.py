from data.market import get_data
from core.engines import breakout_engine, reversal_engine, continuation_engine
from core.signals import build_signal

def scan(symbol):

    df = get_data(symbol)

    if df is None:
        return None

    breakout = breakout_engine(df)

    rev_buy, rev_sell = reversal_engine(df)

    cont_buy, cont_sell = continuation_engine(df)

    buy_score = breakout + rev_buy + cont_buy
    sell_score = breakout + rev_sell + cont_sell

    signal = build_signal(symbol, df, buy_score, sell_score)

    return signal
