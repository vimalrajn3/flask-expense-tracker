import sqlite3
from pathlib import Path

DB_PATH = Path("databases/data.db")
DB_PATH.parent.mkdir(exist_ok=True)

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            amount TEXT NOT NULL,
            category TEXT NOT NULL,
            date  TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()
