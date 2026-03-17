from DB_Connection import *
from DB_Connection import Error

def insertToDBUsers(connection, usernameUser, passwordUser, role):
    try:
        cursor = connection.cursor()
        sql_insert_query = """INSERT INTO users (usernameUser, passwordUser, role) VALUES (%s, %s, %s)"""
        insert_tuple = (usernameUser, passwordUser, role)
                
        cursor.execute(sql_insert_query, insert_tuple)
        connection.commit()
        print("Η εγγραφή εισήχθη επιτυχώς στην βάση δεδομένων")
    except Error as e:
        print(f"Σφάλμα κατά την εκτέλεση του ερωτήματος: {e}")
    finally:
        if cursor:
            cursor.close()

# Δημιουργία σύνδεσης
connection = create_connection()

if connection:
    # Κλήση της συνάρτησης με τις επιθυμητές τιμές
    insertToDBUsers(connection, "Tassos", "456456", "Manager")
    insertToDBUsers(connection, "Panos", "789789", "Manager")
    insertToDBUsers(connection, "Marios", "123123", "Waiter")
    insertToDBUsers(connection, "Maria", "456456", "Waiter")
    insertToDBUsers(connection, "Eleni", "789789", "Waiter")
    insertToDBUsers(connection, "Makis", "132", "Waiter")
    insertToDBUsers(connection, "Dionisia", "321", "Waiter")

    # Κλείσιμο της σύνδεσης
    connection.close()
    print("Η σύνδεση με τη MySQL έκλεισε")