import tkinter as tk
from tkinter import ttk, messagebox
from DB_Connection import create_connection, Error

class CreateRecipeWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Create Recipe")

        self.ingredients = []

        self.create_widgets()

    def create_widgets(self):
        # Recipe Name
        self.recipe_name_label = tk.Label(self.root, text="Recipe Name:")
        self.recipe_name_label.pack()
        self.recipe_name_entry = tk.Entry(self.root)
        self.recipe_name_entry.pack()

        # Plate ID
        self.plate_id_label = tk.Label(self.root, text="Plate ID:")
        self.plate_id_label.pack()
        self.plate_id_combo = ttk.Combobox(self.root)
        self.plate_id_combo.pack()
        self.load_plate_ids()

        # Add New Plate Button
        self.add_new_plate_button = tk.Button(self.root, text="Add New Plate", command=self.add_new_plate)
        self.add_new_plate_button.pack()

        # Ingredients List
        self.ingredients_frame = tk.Frame(self.root)
        self.ingredients_frame.pack()

        self.add_ingredient_button = tk.Button(self.ingredients_frame, text="Add Ingredient", command=self.add_ingredient)
        self.add_ingredient_button.grid(row=0, column=0)

        self.ingredients_tree = ttk.Treeview(self.ingredients_frame, columns=("Name", "Quantity", "Threshold"), show='headings')
        self.ingredients_tree.heading("Name", text="Name")
        self.ingredients_tree.heading("Quantity", text="Quantity")
        self.ingredients_tree.heading("Threshold", text="Threshold")
        self.ingredients_tree.grid(row=1, column=0, columnspan=2)

        # Complete Recipe Button
        self.complete_recipe_button = tk.Button(self.root, text="Complete Recipe", command=self.complete_recipe)
        self.complete_recipe_button.pack()

    def load_plate_ids(self):
        connection = create_connection()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute("SELECT idPlate FROM plate")
                plates = cursor.fetchall()
                plate_ids = [str(plate[0]) for plate in plates]
                self.plate_id_combo['values'] = plate_ids
                cursor.close()
                connection.close()
            except Error as e:
                print(f"Failed to load plate ids: {e}")
                messagebox.showerror("Error", "Failed to load plate ids.")

    def add_new_plate(self):
        new_plate_window = tk.Toplevel(self.root)
        new_plate_window.title("Add New Plate")

        tk.Label(new_plate_window, text="Plate Name:").grid(row=0, column=0)
        plate_name_entry = tk.Entry(new_plate_window)
        plate_name_entry.grid(row=0, column=1)

        tk.Label(new_plate_window, text="Price:").grid(row=1, column=0)
        plate_price_entry = tk.Entry(new_plate_window)
        plate_price_entry.grid(row=1, column=1)

        def insert_new_plate():
            plate_name = plate_name_entry.get()
            plate_price = plate_price_entry.get()

            if not plate_name or not plate_price:
                messagebox.showerror("Error", "Please enter all fields")
                return

            try:
                plate_price = float(plate_price)
            except ValueError:
                messagebox.showerror("Error", "Price must be a float")
                return

            connection = create_connection()
            if connection:
                try:
                    cursor = connection.cursor()
                    sql = "INSERT INTO plate (namePlate, price) VALUES (%s, %s)"
                    cursor.execute(sql, (plate_name, plate_price))
                    connection.commit()
                    cursor.close()
                    connection.close()
                    messagebox.showinfo("Success", "Plate added successfully")
                    new_plate_window.destroy()
                    self.load_plate_ids()  # Reload plate IDs to include the new plate
                except Error as e:
                    print(f"Failed to insert plate into database: {e}")
                    messagebox.showerror("Error", "Failed to add plate")

        tk.Button(new_plate_window, text="Add", command=insert_new_plate).grid(row=2, column=0, columnspan=2)

    def add_ingredient(self):
        ingredient_window = tk.Toplevel(self.root)
        ingredient_window.title("Add Ingredient")

        tk.Label(ingredient_window, text="Ingredient Name:").grid(row=0, column=0)
        ingredient_name_entry = tk.Entry(ingredient_window)
        ingredient_name_entry.grid(row=0, column=1)

        tk.Label(ingredient_window, text="Quantity:").grid(row=1, column=0)
        ingredient_quantity_entry = tk.Entry(ingredient_window)
        ingredient_quantity_entry.grid(row=1, column=1)

        tk.Label(ingredient_window, text="Threshold:").grid(row=2, column=0)
        ingredient_threshold_entry = tk.Entry(ingredient_window)
        ingredient_threshold_entry.grid(row=2, column=1)

        def add_to_list():
            name = ingredient_name_entry.get()
            quantity = ingredient_quantity_entry.get()
            threshold = ingredient_threshold_entry.get()

            if name and quantity and threshold:
                self.ingredients.append((name, quantity, threshold))
                self.ingredients_tree.insert("", tk.END, values=(name, quantity, threshold))
                ingredient_window.destroy()
            else:
                messagebox.showerror("Error", "Please enter all fields")

        tk.Button(ingredient_window, text="Add", command=add_to_list).grid(row=3, column=0, columnspan=2)

    def complete_recipe(self):
        recipe_name = self.recipe_name_entry.get()
        plate_id = self.plate_id_combo.get()

        if not recipe_name or not plate_id or not self.ingredients:
            messagebox.showerror("Error", "Please enter the recipe name, plate ID, and add at least one ingredient.")
            return

        try:
            plate_id = int(plate_id)
        except ValueError:
            messagebox.showerror("Error", "Plate ID must be an integer.")
            return

        confirm = messagebox.askyesno("Confirm Recipe", "Are you sure you want to complete the recipe?")
        if confirm:
            self.insert_recipe_into_db(recipe_name, plate_id, self.ingredients)
            messagebox.showinfo("Success", "Recipe created successfully.")
            self.root.destroy()
        else:
            self.root.deiconify()

    def insert_recipe_into_db(self, recipe_name, plate_id, ingredients):
        connection = create_connection()
        if connection:
            try:
                cursor = connection.cursor()

                # Insert recipe
                sql_recipe = "INSERT INTO recipe (nameRecipe, idPlate) VALUES (%s, %s)"
                cursor.execute(sql_recipe, (recipe_name, plate_id))
                recipe_id = cursor.lastrowid

                # Insert ingredients
                sql_ingredient = "INSERT INTO recipe_ingredient (recipe_id, nameIngredient, quantity, threshold) VALUES (%s, %s, %s, %s)"
                for ingredient in ingredients:
                    cursor.execute(sql_ingredient, (recipe_id, ingredient[0], ingredient[1], ingredient[2]))

                connection.commit()
                cursor.close()
                connection.close()
            except Error as e:
                print(f"Failed to insert recipe into database: {e}")
                messagebox.showerror("Error", "Failed to create recipe.")

def main():
    root = tk.Tk()
    app = CreateRecipeWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()
