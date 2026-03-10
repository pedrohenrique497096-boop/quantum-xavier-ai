from core.structure import detect_structure
from core.liquidity import detect_liquidity
from core.orderblock import detect_orderblock
from core.orderflow import detect_orderflow
from core.fvg import detect_fvg
from core.confluence import calculate_confluence
from core.risk import calculate_risk
from core.narrative import build_narrative

def analyze_market(symbol,candles,price):

    structure=detect_structure(candles)

    liquidity=detect_liquidity(candles)

    ob=detect_orderblock(candles)

    fvg=detect_fvg(candles)

    flow=detect_orderflow(candles)

    confidence=calculate_confluence(
        structure,
        liquidity,
        ob,
        fvg,
        flow
    )

    risk=calculate_risk(price)

    narrative=build_narrative(symbol,confidence)

    return {

        "asset":symbol,
        "entry":price,
        "stop":risk["stop"],
        "take1":risk["tp1"],
        "take2":risk["tp2"],
        "take3":risk["tp3"],
        "confidence":confidence,
        "analysis":narrative

    }
