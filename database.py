import sqlite3

db = "finance.db"

def get_db():
    conn = sqlite3.connect(db)
    conn.row_factory = sqlite3.Row
    return conn

def query(sql, params=(), fetch="all"):
    conn = get_db()
    row = conn.execute(sql, params).fetchone() if fetch == "one" else conn.execute(sql, params).fetchall()
    conn.commit()
    conn.close()
    return row

def execute(sql, params=()):
    conn = get_db()
    conn.execute(sql, params)
    conn.commit()
    conn.close()