signals=[]

history=[]

def save_signal(signal):

    signals.append(signal)

    history.append({
        "confidence":signal["confidence"],
        "result":1
    })


def get_signals():

    return signals


def get_dataset():

    return history
