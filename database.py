import sqlite3
from flask import g
from contextlib import contextmanager

DATABASE = "finance.db"

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA journal_mode=WAL")
    return g.db

def close_db(e=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()

@contextmanager
def transaction():
    db = get_db()

    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise

def query(sql: str, params: tuple = ()) -> list:
    db = get_db()
    return db.execute(sql, params).fetchall()

def query_one(sql: str, params: tuple = ()) -> sqlite3.Row | None:
    db = get_db()
    return db.execute(sql, params).fetchone()

def execute(sql: str, params: tuple = ()):
    with transaction() as db:
        cursor = db.execute(sql, params)
        return cursor.rowcount

def init_db():
    conn = sqlite3.connect(DATABASE)

    with open("schema.sql") as f:
        conn.executescript(f.read())
    
    conn.commit()
    conn.close()

init_db()


    