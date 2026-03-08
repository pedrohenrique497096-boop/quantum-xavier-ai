import sqlite3
import pandas as pd
from config.settings import DB_PATH


def get_conn():
    return sqlite3.connect(DB_PATH, check_same_thread=False)


def setup():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS open_signals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        symbol TEXT,
        direction TEXT,
        entry REAL,
        stop REAL,
        target REAL,
        close REAL,
        confidence REAL,
        reason TEXT,
        opened_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS closed_signals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        symbol TEXT,
        direction TEXT,
        entry REAL,
        stop REAL,
        target REAL,
        close REAL,
        confidence REAL,
        reason TEXT,
        opened_at TEXT,
        closed_at TEXT DEFAULT CURRENT_TIMESTAMP,
        result TEXT
    )
    """)

    conn.commit()
    conn.close()


def open_signal_exists(signal: dict) -> bool:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT 1 FROM open_signals
        WHERE symbol = ? AND direction = ? AND ABS(entry - ?) < 0.000001
        LIMIT 1
    """, (signal["symbol"], signal["direction"], signal["entry"]))
    row = cur.fetchone()
    conn.close()
    return row is not None


def save_open_signal(signal: dict):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
    INSERT INTO open_signals
    (symbol, direction, entry, stop, target, close, confidence, reason)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        signal["symbol"],
        signal["direction"],
        signal["entry"],
        signal["stop"],
        signal["target"],
        signal["close"],
        signal["confidence"],
        signal.get("reason", ""),
    ))
    conn.commit()
    conn.close()


def load_open_signals():
    conn = get_conn()
    df = pd.read_sql_query("SELECT * FROM open_signals ORDER BY id DESC", conn)
    conn.close()
    return df


def load_closed_signals(limit=100):
    conn = get_conn()
    df = pd.read_sql_query(
        f"SELECT * FROM closed_signals ORDER BY id DESC LIMIT {int(limit)}",
        conn
    )
    conn.close()
    return df


def close_signal(signal_id: int, result: str):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT * FROM open_signals WHERE id = ?", (signal_id,))
    row = cur.fetchone()
    if row is None:
        conn.close()
        return

    cur.execute("""
    INSERT INTO closed_signals
    (symbol, direction, entry, stop, target, close, confidence, reason, opened_at, result)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], result
    ))

    cur.execute("DELETE FROM open_signals WHERE id = ?", (signal_id,))
    conn.commit()
    conn.close()


def stats_summary():
    conn = get_conn()
    open_count = pd.read_sql_query("SELECT COUNT(*) AS n FROM open_signals", conn)["n"].iloc[0]
    closed = pd.read_sql_query("SELECT result, COUNT(*) AS n FROM closed_signals GROUP BY result", conn)
    conn.close()

    wins = int(closed.loc[closed["result"] == "TAKE", "n"].sum()) if not closed.empty else 0
    losses = int(closed.loc[closed["result"] == "STOP", "n"].sum()) if not closed.empty else 0
    total = wins + losses
    winrate = (wins / total * 100) if total > 0 else 0.0

    return {
        "open": int(open_count),
        "wins": wins,
        "losses": losses,
        "winrate": winrate,
    }
