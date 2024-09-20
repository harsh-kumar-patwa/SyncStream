import sqlite3
from config import DATABASE_PATH

def initialise_db():
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        stripe_id TEXT UNIQUE
    ''')
    connection.commit()
    connection.close()