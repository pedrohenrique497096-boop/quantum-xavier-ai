def backtest(trades):

    wins=0
    losses=0

    for t in trades:

        if t["result"]=="win":
            wins+=1
        else:
            losses+=1

    total=wins+losses

    if total==0:
        return 0

    return wins/total
