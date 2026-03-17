import tkinter as tk
from tkinter import ttk, messagebox
from DB_Connection import create_connection, Error
import csv

class CreateOrderWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Create Supplier Order")

        self.selected_ingredients = {}

        self.create_widgets()
        self.load_ingredients()

    def create_widgets(self):
        # Treeview for displaying ingredients
        self.tree = ttk.Treeview(self.root, columns=("ID", "Name", "Quantity", "Threshold", "Category", "Plate ID"), show='headings')
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Quantity", text="Quantity")
        self.tree.heading("Threshold", text="Threshold")
        self.tree.heading("Category", text="Category")
        self.tree.heading("Plate ID", text="Plate ID")
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Button to add ingredient to order
        self.add_button = tk.Button(self.root, text="Add to Order", command=self.add_to_order)
        self.add_button.pack()

        # Button to complete the order
        self.order_button = tk.Button(self.root, text="Complete Order", command=self.complete_order)
        self.order_button.pack()

    def load_ingredients(self):
        connection = create_connection()
        if connection:
            try:
                cursor = connection.cursor()
                sql = "SELECT * FROM ingredient"
                cursor.execute(sql)
                rows = cursor.fetchall()
                for row in rows:
                    self.tree.insert("", tk.END, values=row)
                cursor.close()
                connection.close()
            except Error as e:
                print(f"Failed to load ingredients: {e}")

    def add_to_order(self):
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showerror("Error", "Please select at least one ingredient to add to the order.")
            return

        for item in selected_items:
            ingredient = self.tree.item(item, "values")
            quantity = self.prompt_for_quantity(ingredient[1])
            if quantity:
                self.selected_ingredients[ingredient[1]] = (ingredient[0], quantity)
                messagebox.showinfo("Success", f"Added {quantity} of {ingredient[1]} to the order.")
        
        self.display_order()

    def prompt_for_quantity(self, ingredient_name):
        quantity = tk.simpledialog.askinteger("Quantity", f"Enter quantity for {ingredient_name}:")
        return quantity

    def display_order(self):
        order_summary = "Current Order:\n"
        for name, (id, quantity) in self.selected_ingredients.items():
            order_summary += f"{name}: {quantity}\n"
        messagebox.showinfo("Order Summary", order_summary)

    def complete_order(self):
        if not self.selected_ingredients:
            messagebox.showerror("Error", "No ingredients selected for the order.")
            return

        confirm = messagebox.askyesno("Confirm Order", "Are you sure you want to complete the order?")
        if confirm:
            self.create_order_file(self.selected_ingredients)
            self.send_order_to_supplier(self.selected_ingredients)
            messagebox.showinfo("Success", "Order sent to supplier successfully.")
            self.root.destroy()

    def create_order_file(self, order):
        with open('supplier_order.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Name", "Quantity"])
            for name, (id, quantity) in order.items():
                writer.writerow([id, name, quantity])

    def send_order_to_supplier(self, order):
        print("Order sent to supplier:", order)

def main():
    root = tk.Tk()
    app = CreateOrderWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()
