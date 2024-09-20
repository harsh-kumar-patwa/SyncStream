import sqlite3 
from config import DATABASE_PATH
import logging

logger = logging.getLogger(__name__)

def get_db_connection():
    return sqlite3.connect(DATABASE_PATH)


def create_customer(name, email, stripe_id=None):
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute('INSERT INTO customer (name, email, stripe_id) VALUES (?, ?, ?)', (name, email, stripe_id))
        customer_id = cursor.lastrowid
        connection.commit()
        return customer_id, None
    except sqlite3.Error as e:
        if "UNIQUE constraint failed: customer.email" in str(e):
            return None, "Email already exists"
        else:
            return None, "An unexpected error occurred"
    finally:
        connection.close()


def update_customer(customer_id, **kwargs):
    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        columns = ', '.join([f'{k} = ?' for k in kwargs])
        values = list(kwargs.values())
        cursor.execute(f'UPDATE customer SET {columns} WHERE id = ?', (*values, customer_id))
        connection.commit()
        if cursor.rowcount == 0:
            return None, "Customer not found"
        return get_customer(customer_id)
    except sqlite3.Error as e:
        logger.error(f"Database error: {str(e)}")
        return None, f"Database error: {str(e)}"
    finally:
        connection.close()


def get_customer(customer_id):
    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM customer WHERE id = ?', (customer_id,))
        customer = cursor.fetchone()
        if customer:
            return dict(zip(['id', 'name', 'email', 'stripe_id'], customer)), None
        else:
            return None, "Customer not found"
    except sqlite3.Error as e:
        logger.error(f"Database error: {str(e)}")
        return None, f"Database error: {str(e)}"
    finally:
        connection.close()


def delete_customer(customer_id):
    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        cursor.execute('SELECT stripe_id FROM customer WHERE id = ?', (customer_id,))
        result = cursor.fetchone()
        
        if not result:
            return None, "Customer not found"
        
        stripe_id = result[0]
        cursor.execute('DELETE FROM customer WHERE id = ?', (customer_id,))
        connection.commit()
        if cursor.rowcount == 0:
            return None, "Customer not found"
        return stripe_id, None
    except sqlite3.Error as e:
        logger.error(f"Database error: {str(e)}")
        return None, f"Database error: {str(e)}"
    finally:
        connection.close()


def get_customer_by_external_id(external_id_type, external_id):
    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        cursor.execute(f'SELECT * FROM customer WHERE {external_id_type} = ?', (external_id,))
        customer = cursor.fetchone()
        if customer:
            return dict(zip(['id', 'name', 'email', 'stripe_id'], customer)), None
        else:
            return None, f"Customer with {external_id_type} {external_id} not found"
    except sqlite3.Error as e:
        logger.error(f"Database error: {str(e)}")
        return None, f"Database error: {str(e)}"
    finally:
        connection.close()

def get_customer_by_email(email):
    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM customer WHERE email = ?', (email,))
        customer = cursor.fetchone()
        if customer:
            return dict(zip(['id', 'name', 'email', 'stripe_id'], customer)), None
        else:
            return None, "Customer not found"
    except sqlite3.Error as e:
        logger.error(f"Database error: {str(e)}")
        return None, f"Database error: {str(e)}"
    finally:
        connection.close()