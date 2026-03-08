import pandas as pd

def heatmap(signals):

    df = pd.DataFrame(signals)

    if df.empty:
        return df

    return df[["symbol","direction"]]
