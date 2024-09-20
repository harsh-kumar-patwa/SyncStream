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

    columns = ', '.join([f'{k} = ?' for k in kwargs])
    values = list(kwargs.values())
    cursor.execute(f'UPDATE customer SET {columns} WHERE id = ?', (*values,customer_id))

    connection.commit()
    count= cursor.rowcount
    connection.close()

    if count>0:
        return customer_id
    else :
        return None

def get_customer(customer_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM customer WHERE id = ?', (customer_id,))
    customer = cursor.fetchone()
    connection.close()
    return customer

def delete_customer(customer_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('DELETE FROM customer WHERE id = ?', (customer_id,))
    deleted = cursor.rowcount > 0
    connection.commit()
    connection.close()
    
    if deleted:
        return customer_id
    else:
        return None
    
# for the stripe or other integration update 
def get_customer_by_external_id(external_id_type, external_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(f'SELECT * FROM customer WHERE {external_id_type} = ?', (external_id,))
    customer = cursor.fetchone()
    connection.close()
    return customer

