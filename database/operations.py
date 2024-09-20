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

def update_customer(customer_id,**kwargs):
    connection = get_db_connection()
    cursor = connection.cursor()
    set_clause = ', '.join([f'{k} = ?' for k in kwargs.keys()])
    values = list(kwargs.values()) + [customer_id]
    cursor.execute(f'UPDATE customers SET {set_clause} WHERE id = ?', values)
    connection.commit()
    connection.close()

    if cursor.rowcount>0:
        return customer_id
    else :
        return None

def get_customer(customer_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM customers WHERE id = ?', (customer_id,))
    customer = cursor.fetchone()
    connection.close()
    return customer

def delete_customer(customer_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('DELETE FROM customers WHERE id = ?', (customer_id))
    deleted = cursor.rowcount > 0
    connection.commit()
    connection.close()
    
    if deleted:
        return customer_id
    else:
        return None
    
def get_customer_by_external_id(external_id_type, external_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(f'SELECT * FROM customers WHERE {external_id_type} = ?', (external_id,))
    customer = cursor.fetchone()
    connection.close()
    return customer

