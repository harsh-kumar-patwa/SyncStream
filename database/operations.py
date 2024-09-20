import sqlite3
from config import DATABASE_PATH

def get_db_connection():
    return sqlite3.connect(DATABASE_PATH)

def create_customer(name,email):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('INSERT INTO customer (name,email) VALUES (?,?)',(name,email))
    customer_id = cursor.lastrowid
    connection.commit()
    connection.close()
    return customer_id

def update_customer():
    pass

def get_customer():
    pass

def delete_customer():
    pass

