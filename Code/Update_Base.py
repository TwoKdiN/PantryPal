import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from DB_Connection import create_connection, Error

class UpdateIngredientWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Update Ingredient")

        self.search_label = tk.Label(root, text="Search Ingredient:")
        self.search_label.pack()
        self.search_entry = tk.Entry(root)
        self.search_entry.pack()

        self.quantity_label = tk.Label(root, text="New Quantity:")
        self.quantity_label.pack()
        self.quantity_entry = tk.Entry(root)
        self.quantity_entry.pack()

        self.update_button = tk.Button(root, text="Update", command=self.update_ingredient)
        self.update_button.pack()

    def update_ingredient(self):
        ingredient_name = self.search_entry.get()
        new_quantity = self.quantity_entry.get()

        if not ingredient_name or not new_quantity:
            messagebox.showerror("Error", "Please enter both ingredient name and new quantity.")
            return

        connection = create_connection()
        if connection:
            try:
                cursor = connection.cursor()
                # Check if the ingredient exists
                check_sql = "SELECT COUNT(*) FROM ingredient WHERE nameIngredient = %s"
                cursor.execute(check_sql, (ingredient_name,))
                count = cursor.fetchone()[0]
                
                if count == 0:
                    # Ingredient not found
                    add_new = messagebox.askyesno("Not Found", "Το υλικό δεν βρέθηκε. Θέλετε να το προσθέσετε;")
                    if add_new:
                        self.add_new_ingredient(ingredient_name, new_quantity)
                    else:
                        return
                else:
                    # Ingredient found, update it
                    sql = "UPDATE ingredient SET quantityOfIngredient = %s WHERE nameIngredient = %s"
                    cursor.execute(sql, (new_quantity, ingredient_name))
                    connection.commit()
                    messagebox.showinfo("Success", f"Ingredient '{ingredient_name}' updated successfully.")
                    self.clear_form()

                cursor.close()
                connection.close()
            except Error as e:
                print(f"Failed to update ingredient: {e}")
                messagebox.showerror("Error", "Failed to update ingredient.")
    
    def add_new_ingredient(self, ingredient_name, quantity):
        connection = create_connection()
        if connection:
            try:
                cursor = connection.cursor()
                sql = "INSERT INTO ingredient (nameIngredient, quantityOfIngredient) VALUES (%s, %s)"
                cursor.execute(sql, (ingredient_name, quantity))
                connection.commit()
                cursor.close()
                connection.close()
                messagebox.showinfo("Success", f"New ingredient '{ingredient_name}' added successfully.")
                self.clear_form()
            except Error as e:
                print(f"Failed to add new ingredient: {e}")
                messagebox.showerror("Error", "Failed to add new ingredient.")

    def clear_form(self):
        self.search_entry.delete(0, tk.END)
        self.quantity_entry.delete(0, tk.END)

def main():
    root = tk.Tk()
    app = UpdateIngredientWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()
