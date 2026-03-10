def calculate_confluence(*signals):

    score=50

    for s in signals:

        if s:
            score+=5

    return min(score,95)
