import sqlite3

def initialise_db():
    connection = sqlite3.connect("")
    cursor = connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL
    )
    ''')
    connection.commit()
    connection.close()