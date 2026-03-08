import sqlite3

DB = "signals.db"

def setup():

    conn = sqlite3.connect(DB)

    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS signals (
        id INTEGER PRIMARY KEY,
        symbol TEXT,
        direction TEXT,
        entry REAL,
        stop REAL,
        target REAL,
        confidence REAL,
        result TEXT,
        time TEXT
    )
    """)

    conn.commit()
    conn.close()


def save_signal(signal):

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO signals
    (symbol,direction,entry,stop,target,confidence,result,time)
    VALUES (?,?,?,?,?,?,?,datetime('now'))
    """,(
        signal["symbol"],
        signal["direction"],
        signal["entry"],
        signal["stop"],
        signal["target"],
        signal["confidence"],
        "OPEN"
    ))

    conn.commit()
    conn.close()
