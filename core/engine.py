from core.structure import detect_structure
from core.liquidity import detect_liquidity
from core.orderblock import detect_orderblock
from core.fvg import detect_fvg
from core.confluence import calculate_confluence
from core.risk import calculate_risk
from core.narrative import build_narrative


def analyze_market(symbol, candles, price):

    structure = detect_structure(candles)

    liquidity = detect_liquidity(candles)

    orderblock = detect_orderblock(candles)

    fvg = detect_fvg(candles)

    confidence = calculate_confluence(
        structure,
        liquidity,
        orderblock,
        fvg
    )

    risk = calculate_risk(price)

    narrative = build_narrative(symbol, confidence)

    direction = "BUY"

    if confidence < 75:
        direction = "SELL"

    return {
        "asset": symbol,
        "direction": direction,
        "entry": round(price, 2),
        "stop_loss": round(risk["stop"], 2),
        "take_profit_1": round(risk["tp1"], 2),
        "take_profit_2": round(risk["tp2"], 2),
        "take_profit_3": round(risk["tp3"], 2),
        "confidence": confidence,
        "analysis": narrative
    }
