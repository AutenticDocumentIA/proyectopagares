import mysql.connector
from mysql.connector import Error

def connect_to_mysql():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='admin',
            password='Admin202427001atic*',
            database='pagares_db'
        )
        if connection.is_connected():
            print("✅ Conexión exitosa a MySQL")
        return connection
    except Error as e:
        print(f"❌ Error al conectar a MySQL compa: {e}")
        return None

