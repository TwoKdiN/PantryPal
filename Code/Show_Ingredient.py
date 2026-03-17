import tkinter as tk
from tkinter import ttk
from DB_Connection import create_connection
from mysql.connector import Error

class ShowIngredient:
    
    def __init__(self, root):
        self.root = root
        self.root.title("Ingredients")
        self.create_table()
        self.load_data()

    def create_table(self):
        self.tree = ttk.Treeview(self.root, columns=("ID", "Name", "Quantity", "Threshold", "Category", "Plate ID"), show='headings')
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Quantity", text="Quantity")
        self.tree.heading("Threshold", text="Threshold")
        self.tree.heading("Category", text="Category")
        self.tree.heading("Plate ID", text="Plate ID")
        self.tree.pack(fill=tk.BOTH, expand=True)
        
    def load_data(self):
        connection = create_connection()
        if connection:
            try:
                cursor = connection.cursor()
                sql = """SELECT * FROM ingredient"""
                cursor.execute(sql)
                rows = cursor.fetchall()
                
                for row in rows:
                    self.tree.insert("", tk.END, values=row)
                    
                cursor.close()
                connection.close()
                
            except Error as e:
                print(f"Failed to show ingredients: {e}")

def main():
    root = tk.Tk()
    app = ShowIngredient(root)
    root.mainloop()

if __name__ == "__main__":
    main()
