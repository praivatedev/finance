from database import execute, query_one

def find_user(user_id: int):
    return query_one("SELECT * FROM users WHERE id = ?", (user_id,) )
