import os
import sqlite3
from config.settings import DB_PATH


def adaptive_confidence_boost() -> float:
    if not os.path.exists(DB_PATH):
        return 0.0

    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()

        cur.execute("SELECT COUNT(*) FROM closed_trades")
        total = cur.fetchone()[0]

        if total == 0:
            conn.close()
            return 0.0

        cur.execute("SELECT COUNT(*) FROM closed_trades WHERE result='TP'")
        wins = cur.fetchone()[0]
        conn.close()

        winrate = wins / total

        # boost leve, para não distorcer demais
        return (winrate - 0.5) * 20.0

    except Exception:
        return 0.0


def explain_signal(signal: dict) -> str:
    return (
        f"Análise da IA\n\n"
        f"Ativo: {signal['display_symbol']}\n"
        f"Direção: {signal['direction']}\n"
        f"Confiança: {signal['confidence']:.2f}\n\n"
        f"Motivos:\n{signal['reason']}"
    )
