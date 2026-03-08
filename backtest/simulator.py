import random


def monte_carlo_equity(winrate: float = 0.55, trades: int = 50, start: float = 10000.0):
    equity = start

    for _ in range(trades):
        if random.random() < winrate:
            equity *= 1.02
        else:
            equity *= 0.99

    return round(equity, 2)
