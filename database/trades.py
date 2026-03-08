import sqlite3

DB="trades.db"

def setup():

    conn = sqlite3.connect(DB)

    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS trades(
        id INTEGER PRIMARY KEY,
        symbol TEXT,
        direction TEXT,
        entry REAL,
        stop REAL,
        target REAL,
        result TEXT
    )
    """)

    conn.commit()
    conn.close()
