import tkinter as tk
from tkinter import ttk, messagebox
from mysql.connector import Error
from mysql.connector import connect
from Create_Order import CreateOrderWindow

def create_connection():
    try:
        connection = connect(
            host='localhost',
            database='pantrypal',
            user='root',
            password='3315'
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

class TableSelectionWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Table Selection")

        self.tables_frame = tk.Frame(self.root)
        self.tables_frame.pack()

        self.load_tables()

    def load_tables(self):
        connection = create_connection()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute("SELECT idTable, status FROM tableNo")
                tables = cursor.fetchall()
                cursor.close()
                connection.close()

                for table in tables:
                    button_text = f"Table {table[0]} - {table[1]}"
                    table_button = tk.Button(self.tables_frame, text=button_text, command=lambda t=table[0]: self.open_table_menu(t))
                    table_button.pack(fill=tk.BOTH, expand=True)

            except Error as e:
                print(f"Error loading tables: {e}")

    def open_table_menu(self, table_id):
        table_menu = tk.Toplevel(self.root)
        table_menu.title(f"Table {table_id} Menu")

        create_order_button = tk.Button(table_menu, text="Δημιουργία νέας παραγγελίας", command=lambda: self.create_order(table_id))
        create_order_button.pack(fill=tk.BOTH, expand=True)

        payment_button = tk.Button(table_menu, text="Πληρωμή τραπεζιού", command=lambda: self.pay_table(table_id))
        payment_button.pack(fill=tk.BOTH, expand=True)

    def create_order(self, table_id):
        CreateOrderWindow(self.root, table_id)

    def pay_table(self, table_id):
        messagebox.showinfo("Pay Table", f"Processing payment for table {table_id}")
        
    def open_table_menu(self, table_id):
        table_menu = tk.Toplevel(self.root)
        table_menu.title(f"Table {table_id} Menu")

        create_order_button = tk.Button(table_menu, text="Δημιουργία νέας παραγγελίας", command=lambda: self.create_order(table_id))
        create_order_button.pack(fill=tk.BOTH, expand=True)

        view_orders_button = tk.Button(table_menu, text="Προβολή παραγγελιών", command=lambda: self.view_orders(table_id))
        view_orders_button.pack(fill=tk.BOTH, expand=True)

        payment_button = tk.Button(table_menu, text="Πληρωμή τραπεζιού", command=lambda: self.pay_table(table_id))
        payment_button.pack(fill=tk.BOTH, expand=True)

    def view_orders(self, table_id):
        # Λειτουργικότητα για την προβολή των παραγγελιών ενός τραπεζιού
        view_orders_window = tk.Toplevel(self.root)
        view_orders_window.title(f"Παραγγελίες τραπεζιού {table_id}")

        connection = create_connection()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute("SELECT Orders.order_id, plate.namePlate, OrderItems.quantity, OrderItems.special_requests FROM Orders "
                               "INNER JOIN OrderItems ON Orders.order_id = OrderItems.order_id "
                               "INNER JOIN plate ON OrderItems.menu_item_id = plate.idPlate "
                               "WHERE Orders.table_id = %s", (table_id,))
                orders = cursor.fetchall()
                cursor.close()
                connection.close()

                orders_tree = ttk.Treeview(view_orders_window, columns=("OrderID", "Item", "Quantity", "Special Requests"), show='headings')
                orders_tree.heading("OrderID", text="Order ID")
                orders_tree.heading("Item", text="Item")
                orders_tree.heading("Quantity", text="Quantity")
                orders_tree.heading("Special Requests", text="Special Requests")
                orders_tree.pack(fill=tk.BOTH, expand=True)

                for order in orders:
                    orders_tree.insert("", tk.END, values=order)

            except Error as e:
                print(f"Error loading orders: {e}")
                
def main():
    root = tk.Tk()
    app = TableSelectionWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()
