from database import execute, transaction

def buy_stock(name: str, price: float, symbol: str, user_id: int, cash: int) -> None:

    with transaction() as db:
        db.execute("INSERT INTO stocks (symbol, name, price, user_id, bought_at) VALUES (?, ?, ?, ?, datetime('now'))",(symbol, name, price, user_id))

        db.execute("UPDATE users SET cash = ? WHERE id = ?", (cash, user_id))

