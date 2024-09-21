import sqlite3
import os
from config import DATABASE_PATH,ENABLED_INTEGRATIONS


def initialise_db():
    os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS customer (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        stripe_id TEXT UNIQUE
    )
    ''')

    # for integration in ENABLED_INTEGRATIONS:
    #     cursor.execute(f'''
    #     ALTER TABLE customer ADD COLUMN {integration}_id TEXT UNIQUE
    #     ''')
    connection.commit()
    connection.close()
    print(f"Database initialized at {DATABASE_PATH}")