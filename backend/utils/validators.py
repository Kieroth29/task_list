from modules.db import DB

def user_exists(id) -> bool:
    db = DB()
    db.cursor.execute("SELECT * FROM users WHERE id = %s", (id,))
    
    if len(db.cursor.fetchall()) > 0:
        return True
    
    return False

def task_exists(id) -> bool:
    db = DB()
    db.cursor.execute("SELECT * FROM tasks WHERE id = %s", (id,))
    
    if len(db.cursor.fetchall()) > 0:
        return True
    
    return False