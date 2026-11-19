from database import execute, transaction

def buy_stock(name: str, price: float, symbol: str, user_id: int, total_cost: float, shares: int) -> None:

    with transaction() as db:
        db.execute("INSERT INTO stocks (symbol, name, price, user_id, shares, bought_at) VALUES (?, ?, ?, ?, ?, datetime('now'))",(symbol, name, price, user_id, shares))

        db.execute("UPDATE users SET cash = cash - ? WHERE id = ?", (total_cost, user_id))

# def find_stock():
#     execute("SELECT * FROM stocks WHERE ")

