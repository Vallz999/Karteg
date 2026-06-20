import mysql.connector
from mysql.connector import Error
from config import Config


def get_connection():
    try:
        connection = mysql.connector.connect(
            host=Config.DB_HOST,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            database=Config.DB_NAME
        )

        if connection.is_connected():
            return connection

    except Error as e:
        print(f"Database connection error: {e}")
        return None


def execute_query(query, params=None):
    connection = get_connection()

    if not connection:
        return False

    cursor = connection.cursor()

    try:
        cursor.execute(query, params or ())
        connection.commit()
        return True

    except Error as e:
        print(f"Query Error: {e}")
        return False

    finally:
        cursor.close()
        connection.close()


def fetch_all(query, params=None):
    connection = get_connection()

    if not connection:
        return []

    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute(query, params or ())
        return cursor.fetchall()

    except Error as e:
        print(f"Fetch Error: {e}")
        return []

    finally:
        cursor.close()
        connection.close()


def fetch_one(query, params=None):
    connection = get_connection()

    if not connection:
        return None

    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute(query, params or ())
        return cursor.fetchone()

    except Error as e:
        print(f"Fetch Error: {e}")
        return None

    finally:
        cursor.close()
        connection.close()