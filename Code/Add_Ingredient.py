import tkinter as tk
from tkinter import messagebox
from DB_Connection import create_connection, Error

class Ingredient:
    def __init__(self, plateName, name, quantity, threshold, category):
        self.plateName = plateName
        self.name = name
        self.quantity = quantity
        self.threshold = threshold
        self.category = category

    # Getters
    def get_plateName(self):
        return self.plateName

    def get_name(self):
        return self.name

    def get_quantity(self):
        return self.quantity

    def get_threshold(self):
        return self.threshold

    def get_category(self):
        return self.category

    # Setters
    def set_plateName(self, plateName):
        self.plateName = plateName

    def set_name(self, name):
        self.name = name

    def set_quantity(self, quantity):
        self.quantity = quantity

    def set_threshold(self, threshold):
        self.threshold = threshold

    def set_category(self, category):
        self.category = category

    # Παράδειγμα μεθόδου
    def __str__(self):
        return f"Ingredient{{name='{self.name}', quantity={self.quantity}, threshold={self.threshold}, plateName={self.plateName}, category={self.category}}}"

class IngredientApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Add Ingredient")

        self.plateName_label = tk.Label(root, text="Plate ID")
        self.plateName_label.pack()
        self.plateName_entry = tk.Entry(root)
        self.plateName_entry.pack()

        self.name_label = tk.Label(root, text="Name")
        self.name_label.pack()
        self.name_entry = tk.Entry(root)
        self.name_entry.pack()

        self.quantity_label = tk.Label(root, text="Quantity")
        self.quantity_label.pack()
        self.quantity_entry = tk.Entry(root)
        self.quantity_entry.pack()

        self.threshold_label = tk.Label(root, text="Threshold")
        self.threshold_label.pack()
        self.threshold_entry = tk.Entry(root)
        self.threshold_entry.pack()

        self.category_label = tk.Label(root, text="Category")
        self.category_label.pack()
        self.category_var = tk.StringVar(root)
        self.category_var.set('Meat')  # Set default category
        self.category_option = tk.OptionMenu(root, self.category_var, 'Meat', 'Fish', 'Vegetable', 'Dairy Product')
        self.category_option.pack()

        self.add_button = tk.Button(root, text="Add Ingredient", command=self.add_ingredient)
        self.add_button.pack()

    def add_ingredient(self):
        try:
            plateName = int(self.plateName_entry.get())
            name = self.name_entry.get()
            quantity = float(self.quantity_entry.get())
            threshold = float(self.threshold_entry.get())
            category = self.category_var.get()

            ingredient = Ingredient(plateName, name, quantity, threshold, category)
            self.insert_ingredient_into_db(ingredient)
            messagebox.showinfo("Success", f"Added {ingredient}")
            self.ask_for_new_entry()
        except ValueError:
            messagebox.showerror("Error", "Please enter valid data")

    def insert_ingredient_into_db(self, ingredient):
        connection = create_connection()
        if connection:
            try:
                cursor = connection.cursor()
                sql = """
                INSERT INTO ingredient (nameIngredient, quantityOfIngredient, threshold, idOfPlate, category)
                VALUES (%s, %s, %s, %s, %s)
                """
                values = (ingredient.get_name(), ingredient.get_quantity(), ingredient.get_threshold(), ingredient.get_plateName(), ingredient.get_category())
                cursor.execute(sql, values)
                connection.commit()
                cursor.close()
                connection.close()
                print("Ingredient inserted successfully")
            except Error as e:
                print(f"Failed to insert into MySQL table: {e}")

    def ask_for_new_entry(self):
        answer = messagebox.askquestion("New Entry", "Εισαγωγή νέου υλικού;")
        if answer == 'yes':
            self.clear_form()
        else:
            self.root.destroy()

    def clear_form(self):
        self.plateName_entry.delete(0, tk.END)
        self.name_entry.delete(0, tk.END)
        self.quantity_entry.delete(0, tk.END)
        self.threshold_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = IngredientApp(root)
    root.mainloop()
