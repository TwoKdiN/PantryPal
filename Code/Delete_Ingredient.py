import tkinter as tk
from tkinter import ttk, messagebox
from DB_Connection import create_connection, Error

class DeleteIngredientWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Delete Ingredient")

        # Label and Entry for search
        self.search_label = tk.Label(root, text="Search Ingredient:")
        self.search_label.pack()
        self.search_entry = tk.Entry(root)
        self.search_entry.pack()

        self.search_button = tk.Button(root, text="Search", command=self.search_ingredients)
        self.search_button.pack()

        # Treeview for displaying ingredients
        self.tree = ttk.Treeview(root, columns=("ID", "Name", "Quantity", "Threshold", "Category", "Plate ID"), show='headings')
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Quantity", text="Quantity")
        self.tree.heading("Threshold", text="Threshold")
        self.tree.heading("Category", text="Category")
        self.tree.heading("Plate ID", text="Plate ID")
        self.tree.pack(fill=tk.BOTH, expand=True)

        self.load_all_ingredients()

        # Delete button
        self.delete_button = tk.Button(root, text="Delete Selected Ingredient", command=self.delete_selected_ingredient)
        self.delete_button.pack()

    def load_all_ingredients(self):
        self.tree.delete(*self.tree.get_children())
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

    def search_ingredients(self):
        ingredient_name = self.search_entry.get()
        if not ingredient_name:
            messagebox.showerror("Error", "Please enter an ingredient name to search.")
            return

        self.tree.delete(*self.tree.get_children())
        connection = create_connection()
        if connection:
            try:
                cursor = connection.cursor()
                sql = "SELECT * FROM ingredient WHERE nameIngredient LIKE %s"
                cursor.execute(sql, ('%' + ingredient_name + '%',))
                rows = cursor.fetchall()
                if not rows:
                    messagebox.showinfo("Info", f"Ingredient '{ingredient_name}' not found.")
                    self.load_all_ingredients()
                    return
                for row in rows:
                    self.tree.insert("", tk.END, values=row)
                cursor.close()
                connection.close()
            except Error as e:
                print(f"Failed to search ingredients: {e}")

    def delete_selected_ingredient(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select an ingredient to delete.")
            return

        ingredient_id = self.tree.item(selected_item, "values")[0]
        ingredient_name = self.tree.item(selected_item, "values")[1]
        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{ingredient_name}'?")
        if confirm:
            connection = create_connection()
            if connection:
                try:
                    cursor = connection.cursor()
                    sql = "DELETE FROM ingredient WHERE idIngredient = %s"
                    cursor.execute(sql, (ingredient_id,))
                    connection.commit()
                    cursor.close()
                    connection.close()
                    messagebox.showinfo("Success", f"Ingredient '{ingredient_name}' deleted successfully.")
                    self.tree.delete(selected_item)
                except Error as e:
                    print(f"Failed to delete ingredient: {e}")

def main():
    root = tk.Tk()
    app = DeleteIngredientWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()
