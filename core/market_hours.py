from datetime import datetime, timezone


def market_is_open(symbol: str) -> bool:
    now = datetime.now(timezone.utc)
    weekday = now.weekday()  # Monday=0 ... Sunday=6
    hour = now.hour

    # BTC 24/7
    if symbol == "BTC-USD":
        return True

    # Saturday closed
    if weekday == 5:
        return False

    # Sunday opens 22:00 UTC
    if weekday == 6 and hour < 22:
        return False

    # Friday closes 22:00 UTC
    if weekday == 4 and hour >= 22:
        return False

    return True
