# database.py
import psycopg2
import os

def connect_to_database():
    """Establishes a connection to the PostgreSQL database."""
    try:
        # NOTE: The original code did not specify a database, 
        # which is required for some operations. You may need to add it.
        connection = psycopg2.connect(
            host=os.getenv('HOST'),
            user=os.getenv('USER'),
            password=os.getenv('PASSWORD'),
            port=os.getenv('PORT')
        )
        print("Conexión exitosa a PostgreSQL.")
        return connection
    except Exception as e:
        print(f"Error de conexión: {e}")
        return None
