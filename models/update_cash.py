from database import execute

def update_cash(user_id: int, cash: int):
    return execute("UPDATE users SET cash = ? WHERE user_id = ?", cash, user_id)