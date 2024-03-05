import mysql.connector
from mysql.connector import Error

class ManagePantryDB:
    def __init__(self):
        self.conn = None
        self.cursor = None

    def connectDatabase(self):
        try:
            self.conn = mysql.connector.connect(
                host='localhost',
                user='admin',
                password='admin',
                database='pantry_database'
            )
            if self.conn.is_connected():
                self.cursor = self.conn.cursor()
                print("Connected to pantry database")
        except Error as e:
            print(e)
            print("Failed to connect to pantry database")
    
    def closeConnection(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        print("Database connection closed")

    # ---------------------------------------------------------------------------------------------- [INGREDIENTS STOCK]

    def insertIngredient(self, name, quantity, unit, calories, source_url):
        if not self.conn or not self.cursor:
            self.connectDatabase()
        
        if self.conn and self.cursor:
            try:
                self.cursor.execute("INSERT INTO ingredients (name, quantity, unit, calories, source_url) VALUES (%s, %s, %s, %s, %s)", 
                                    (name, quantity, unit, calories, source_url))
                self.conn.commit()
                print(f"Ingredient '{name}' inserted successfully.")
            except Error as e:
                print(e)
                print(f"Failed to insert ingredient '{name}'")
            finally:
                self.closeConnection()

    def deleteIngredient(self, ingredient_id=None, name=None):
        if not self.conn or not self.cursor:
            self.connectDatabase()

        if self.conn and self.cursor:
            try:
                if ingredient_id is not None:
                    self.cursor.execute("DELETE FROM ingredients WHERE ingredient_id = %s", (ingredient_id,))
                elif name is not None:
                    self.cursor.execute("DELETE FROM ingredients WHERE name = %s", (name,))
                else:
                    print("No valid identifier provided for deletion.")
                    return

                self.conn.commit()
                if self.cursor.rowcount > 0:
                    print(f"Ingredient {'with ID ' + str(ingredient_id) if ingredient_id else 'named ' + name} deleted successfully.")
                else:
                    print("Ingredient not found or already deleted.")
            except Error as e:
                print(e)
                print("Failed to delete ingredient.")
            finally:
                self.closeConnection()
          
    # ---------------------------------------------------------------------------------------------- [GROCERY LIST]
                
    def addIngredientToGroceryList(self, ingredient_id, quantity, unit):
        if not self.conn or not self.cursor:
            self.connectDatabase()

        if self.conn and self.cursor:
            try:
                # First, check if the ingredient exists in the 'ingredients' table
                self.cursor.execute("SELECT ingredient_id FROM ingredients WHERE ingredient_id = %s", (ingredient_id,))
                if not self.cursor.fetchone():
                    print(f"No ingredient found with ID {ingredient_id}. Please add it to the ingredients table first.")
                    return
                
                # If the ingredient exists, add it to the grocery list
                self.cursor.execute("INSERT INTO grocerylists (ingredient_id, quantity, unit) VALUES (%s, %s, %s)",
                                    (ingredient_id, quantity, unit))
                self.conn.commit()
                print(f"Ingredient with ID {ingredient_id} added to grocery list.")
            except Error as e:
                print(e)
                print("Failed to add ingredient to grocery list.")
            finally:
                self.closeConnection()
                
    def deleteIngredientFromGroceryList(self, grocerylist_id=None, ingredient_id=None):
        if not self.conn or not self.cursor:
            self.connectDatabase()

        if self.conn and self.cursor:
            try:
                if grocerylist_id is not None:
                    # Delete by grocerylist_id
                    self.cursor.execute("DELETE FROM grocerylists WHERE grocerylist_id = %s", (grocerylist_id,))
                elif ingredient_id is not None:
                    # Delete all entries for a specific ingredient_id
                    self.cursor.execute("DELETE FROM grocerylists WHERE ingredient_id = %s", (ingredient_id,))
                else:
                    print("No valid identifier provided for deletion.")
                    return

                self.conn.commit()
                if self.cursor.rowcount > 0:
                    print(f"Grocery list item{'s' if ingredient_id else ''} {'with ID ' + str(grocerylist_id) if grocerylist_id else 'for ingredient ID ' + str(ingredient_id)} deleted successfully.")
                else:
                    print("Item not found or already deleted from grocery list.")
            except Error as e:
                print(e)
                print("Failed to delete ingredient from grocery list.")
            finally:
                self.closeConnection()       
