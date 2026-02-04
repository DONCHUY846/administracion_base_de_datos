import psycopg2
import os

try:
    connection = psycopg2.connect(
    host=os.getenv('HOST'),
    user=os.getenv('USER'),
    database=os.getenv('DB_NAME'),
    port=os.getenv('PORT')
    )

    cursor = connection.cursor()
    print("Database connection successful")
except Exception as e:
    print("Error connecting to the database:", e)
