import sqlite3
import pandas as pd

DB = "signals.db"


def setup():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS signals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        symbol TEXT,
        direction TEXT,
        entry REAL,
        stop REAL,
        target REAL,
        confidence REAL,
        reason TEXT,
        status TEXT,
        time TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()


def save_signal(signal):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO signals
    (symbol, direction, entry, stop, target, confidence, reason, status, time)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, datetime('now'))
    """, (
        signal["symbol"],
        signal["direction"],
        signal["entry"],
        signal["stop"],
        signal["target"],
        signal["confidence"],
        signal.get("reason", ""),
        signal.get("status", "OPEN")
    ))

    conn.commit()
    conn.close()


def load_signals(limit=100):
    conn = sqlite3.connect(DB)
    df = pd.read_sql_query(
        f"SELECT * FROM signals ORDER BY id DESC LIMIT {int(limit)}",
        conn
    )
    conn.close()
    return df
