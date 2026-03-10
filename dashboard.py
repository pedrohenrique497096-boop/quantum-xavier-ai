from database.trades import get_signals

def dashboard():

    signals=get_signals()

    return {

        "signals_total":len(signals)

    }
