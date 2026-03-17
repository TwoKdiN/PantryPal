import mysql.connector
from mysql.connector import Error

def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='Pantrypal',
            user='root',
            password='3315'
        )
        if connection.is_connected():
            print("Η σύνδεση με τη βάση δεδομένων ήταν επιτυχής")
        return connection
    except Error as e:
        print(f"Σφάλμα κατά τη σύνδεση στη MySQL: {e}")
        return None

