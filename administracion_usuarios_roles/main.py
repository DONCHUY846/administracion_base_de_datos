import psycopg2
import os
from psycopg2 import sql

# Function to get the database connection
def get_connection():
   # returns the database connection
    return psycopg2.connect(
        host=os.getenv('HOST'),
        user=os.getenv('USER'),
        password=os.getenv('PASSWORD'),
        database=os.getenv('DB_NAME'),
        port=os.getenv('PORT')
    )

# Function to show the list of databases
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

# Function to create a new user/role in PostgreSQL
def create_user(connection, user_name, password):
    cursor = None
    try:
        cursor = connection.cursor()
        
        query = sql.SQL("CREATE USER {name} WITH LOGIN PASSWORD %s").format(
            name=sql.Identifier(user_name)
        )
        
        cursor.execute(query, (password,))
        # connection.commit() 
        
        print(f"Usuario '{user_name}' creado exitosamente.")
    except Exception as e:
        connection.rollback()
        print(f"Error al crear rol: {e}")
    finally:
        if cursor:
            cursor.close()

def create_role(connection, role_name):
    cursor = None
    try:
        cursor = connection.cursor()
        
        query = sql.SQL("CREATE ROLE {name}").format(
            name=sql.Identifier(role_name),
        )
        
        cursor.execute(query)
        # connection.commit() 
        
        print(f"Rol '{role_name}' creado exitosamente")
    except Exception as e:
        connection.rollback()
        print(f"Error al crear rol: {e}")
    finally:
        if cursor:
            cursor.close()

# Function to assign privileges to a role in PostgreSQL
def assign_privileges(connection, role_name, privileges, database_name):
    cursor = None
    try:
        cursor = connection.cursor()
        
        query = sql.SQL("GRANT {privileges} ON DATABASE {db} TO {role}").format(
            privileges=sql.SQL(', ').join(map(sql.SQL, privileges)),
            db=sql.Identifier(database_name),
            role=sql.Identifier(role_name)
        )
        
        cursor.execute(query)
        # connection.commit() 
        
        print(f"Privilegios '{', '.join(privileges)}' asignados al rol '{role_name}' en la base de datos '{database_name}'")
    except Exception as e:
        connection.rollback()
        print(f"Error al asignar privilegios: {e}")
    finally:
        if cursor:
            cursor.close()
# function to assign privileges to a user in PostgreSQL
def assign_privileges_to_user(connection, user_name, privileges):
    cursor = None
    try:
        cursor = connection.cursor()
        
        query = sql.SQL("GRANT {privileges} TO {user}").format(
            privileges=sql.SQL(', ').join(map(sql.SQL, privileges)),
            user=sql.Identifier(user_name)
        )
        
        cursor.execute(query)
        # connection.commit() 
        
        print(f"Privilegios '{', '.join(privileges)}' asignados al usuario '{user_name}'")
    except Exception as e:
        connection.rollback()
        print(f"Error al asignar privilegios: {e}")
    finally:
        if cursor:
            cursor.close()
# Main execution
def main():
    connection = None
    try:
        connection = get_connection()
        print("Conexión exitosa a PostgreSQL.")
        show_databases(connection)
    except Exception as e:
        print(f"Error de conexión: {e}")
    finally:
        if connection:
            connection.close()
            print("Conexión cerrada.")

if __name__ == "__main__":
    main()