CREATE TABLE IF NOT EXISTS stocks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    price REAL NOT NULL,
    shares INTEGER NOT NULL, 
    symbol TEXT NOT NULL,
    bought_at TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);