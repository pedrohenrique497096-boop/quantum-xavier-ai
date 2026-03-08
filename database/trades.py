import os
import sqlite3
import pandas as pd
from config.settings import DB_PATH


def _conn():
    return sqlite3.connect(DB_PATH, check_same_thread=False)


def setup_db():
    conn = _conn()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS open_trades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        symbol TEXT,
        display_symbol TEXT,
        direction TEXT,
        entry REAL,
        stop REAL,
        target REAL,
        confidence REAL,
        reason TEXT,
        opened_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS closed_trades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        symbol TEXT,
        display_symbol TEXT,
        direction TEXT,
        entry REAL,
        stop REAL,
        target REAL,
        confidence REAL,
        reason TEXT,
        opened_at TEXT,
        closed_at TEXT DEFAULT CURRENT_TIMESTAMP,
        result TEXT
    )
    """)

    conn.commit()
    conn.close()


def open_trade_exists(symbol: str, direction: str) -> bool:
    conn = _conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT 1 FROM open_trades
        WHERE symbol = ? AND direction = ?
        LIMIT 1
    """, (symbol, direction))
    row = cur.fetchone()
    conn.close()
    return row is not None


def save_open_trade(signal: dict):
    conn = _conn()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO open_trades
    (symbol, display_symbol, direction, entry, stop, target, confidence, reason)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        signal["symbol"],
        signal["display_symbol"],
        signal["direction"],
        signal["entry"],
        signal["stop"],
        signal["target"],
        signal["confidence"],
        signal["reason"],
    ))

    conn.commit()
    conn.close()


def load_open_trades() -> pd.DataFrame:
    if not os.path.exists(DB_PATH):
        return pd.DataFrame()

    conn = _conn()
    df = pd.read_sql_query("SELECT * FROM open_trades ORDER BY id DESC", conn)
    conn.close()
    return df


def load_closed_trades(limit: int = 100) -> pd.DataFrame:
    if not os.path.exists(DB_PATH):
        return pd.DataFrame()

    conn = _conn()
    df = pd.read_sql_query(
        f"SELECT * FROM closed_trades ORDER BY id DESC LIMIT {int(limit)}",
        conn
    )
    conn.close()
    return df


def close_trade(trade_id: int, result: str):
    conn = _conn()
    cur = conn.cursor()

    cur.execute("SELECT * FROM open_trades WHERE id = ?", (trade_id,))
    row = cur.fetchone()

    if row is None:
        conn.close()
        return

    cur.execute("""
    INSERT INTO closed_trades
    (symbol, display_symbol, direction, entry, stop, target, confidence, reason, opened_at, result)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], result
    ))

    cur.execute("DELETE FROM open_trades WHERE id = ?", (trade_id,))
    conn.commit()
    conn.close()


def stats_summary():
    open_df = load_open_trades()
    closed_df = load_closed_trades(limit=10000)

    wins = int((closed_df["result"] == "TP").sum()) if not closed_df.empty else 0
    losses = int((closed_df["result"] == "STOP").sum()) if not closed_df.empty else 0
    total = wins + losses
    winrate = round((wins / total) * 100, 2) if total > 0 else 0.0

    return {
        "open": 0 if open_df.empty else len(open_df),
        "wins": wins,
        "losses": losses,
        "winrate": winrate,
    }
