import psycopg2
import os
from psycopg2 import sql

def get_connection():
   # returns the database connection
    return psycopg2.connect(
        host=os.getenv('HOST'),
        user=os.getenv('USER'),
        password=os.getenv('PASSWORD'),
        database=os.getenv('DB_NAME'),
        port=os.getenv('PORT')
    )

def show_databases(connection):
    # shows the list of databases
    cursor = None
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT datname FROM pg_database WHERE datistemplate = false;")
        databases = cursor.fetchall()
        
        print("-- Bases de Datos ---")
        for db in databases:
            print(f"-> {db[0]}")
            
    except Exception as e:
        print(f"Error al obtener bases de datos: {e}")
    finally:
        if cursor:
            cursor.close()

def create_user(connection, role_name, password):
    cursor = None
    try:
        cursor = connection.cursor()
        
        query = sql.SQL("CREATE USER {name} WITH LOGIN PASSWORD %s").format(
            name=sql.Identifier(role_name)
        )
        
        cursor.execute(query, (password,))
        # connection.commit() 
        
        print(f"Rol '{role_name}' creado exitosamente.")
    except Exception as e:
        connection.rollback()
        print(f"Error al crear rol: {e}")
    finally:
        if cursor:
            cursor.close()
def main():
    connection = None
    try:
        connection = get_connection()
        print("Conexión exitosa a PostgreSQL.")
        show_databases(connection)
        # Example of creating a new role
        create_user(connection, 'test_user', 'test_password')
    except Exception as e:
        print(f"Error de conexión: {e}")
    finally:
        if connection:
            connection.close()
            print("Conexión cerrada.")

if __name__ == "__main__":
    main()