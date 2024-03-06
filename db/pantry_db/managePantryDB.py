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

    # ---------------------------------------------------------------------------------------------- [STOCK List]

    # Insert a new stock item type into the stock table.
    def insertStock(self, name):
        if not self.conn or not self.cursor:
            self.connectDatabase()
        
        if self.conn and self.cursor:
            try:
                self.cursor.execute("INSERT INTO stock (name) VALUES (%s)", 
                                    (name,))
                self.conn.commit()
                print(f"Stock item '{name}' inserted successfully.")
            except Error as e:
                print(e)
                print(f"Failed to insert stock item '{name}'")
            finally:
                self.closeConnection()

    # Delete a stock item type from the stock table based on stock_id or name
    def deleteStock(self, stock_id=None, name=None):
        if not self.conn or not self.cursor:
            self.connectDatabase()

        if self.conn and self.cursor:
            try:
                if stock_id is not None:
                    self.cursor.execute("DELETE FROM stock WHERE stock_id = %s", (stock_id,))
                elif name is not None:
                    self.cursor.execute("DELETE FROM stock WHERE name = %s", (name,))
                else:
                    print("No valid identifier provided for deletion.")
                    return

                self.conn.commit()
                print(f"Stock item {'with ID ' + str(stock_id) if stock_id else 'named ' + name} deleted successfully.")
            except Error as e:
                print(e)
                print("Failed to delete stock item.")
            finally:
                self.closeConnection()
    
    # Retrieve details of all stock items, including name, quantity, and unit
    def getAllStocksDetails(self):
        
        if not self.conn or not self.cursor:
            self.connectDatabase()

        stocks_details = []
        if self.conn and self.cursor:
            try:
                query = "SELECT name FROM stock ORDER BY name;"
                self.cursor.execute(query)
                rows = self.cursor.fetchall()
                for row in rows:
                    stocks_details.append(row[0])
                
                if stocks_details:
                    print("All stock items:")
                    for name in stocks_details:
                        print(f"Name: {name}")
                else:
                    print("No stock items found in the database.")
                
            except Error as e:
                print(e)
                print("Failed to retrieve all stock items details from the database.")
            finally:
                self.closeConnection()
        return stocks_details
    
    # Insert a new stock item detail into the stock_details table
    def insertStockDetail(self, stock_id, quantity, unit, expiration_date):
        if not self.conn or not self.cursor:
            self.connectDatabase()
        
        if self.conn and self.cursor:
            try:
                self.cursor.execute("INSERT INTO stock_details (stock_id, quantity, unit, expiration_date) VALUES (%s, %s, %s, %s)", 
                                    (stock_id, quantity, unit, expiration_date))
                self.conn.commit()
                print(f"Stock detail for stock_id '{stock_id}' inserted successfully.")
            except Error as e:
                print(e)
                print(f"Failed to insert stock detail for stock_id '{stock_id}'")
            finally:
                self.closeConnection()
    
    # Retrieve the total quantity of a specific item from stock_details, summed across all expiration dates.
    def getTotalQuantityOfItem(self, item_name):
       
        if not self.conn or not self.cursor:
            self.connectDatabase()

        if self.conn and self.cursor:
            try:
                query = """
                SELECT s.name, SUM(sd.quantity) AS total_quantity, sd.unit
                FROM stock_details sd
                JOIN stock s ON sd.stock_id = s.stock_id
                WHERE s.name = %s
                GROUP BY s.name, sd.unit;
                """
                self.cursor.execute(query, (item_name,))
                result = self.cursor.fetchone()
                
                if result:
                    print(f"Total quantity for {result[0]}: {result[1]} {result[2]}")
                else:
                    print(f"No stock found for '{item_name}' in the database.")
                
            except Error as e:
                print(e)
                print("Failed to retrieve the total quantity of the item.")
            finally:
                self.closeConnection()

    # Retrieve a list of items from stock_details that are nearing expiration within a specified number of days
    def getItemsNearingExpiration(self, days=30):
        if not self.conn or not self.cursor:
            self.connectDatabase()

        if self.conn and self.cursor:
            try:
                query = """
                SELECT s.name, sd.quantity, sd.unit, sd.expiration_date
                FROM stock_details sd
                JOIN stock s ON sd.stock_id = s.stock_id
                WHERE sd.expiration_date <= DATE_ADD(CURDATE(), INTERVAL %s DAY)
                ORDER BY sd.expiration_date ASC;
                """
                self.cursor.execute(query, (days,))
                rows = self.cursor.fetchall()
                
                if rows:
                    print(f"Items nearing expiration within the next {days} days:")
                    for row in rows:
                        print(f"Name: {row[0]}, Quantity: {row[1]}, Unit: {row[2]}, Expiration Date: {row[3]}")
                else:
                    print("No items are nearing expiration within the specified timeframe.")
                
            except Error as e:
                print(e)
                print("Failed to retrieve items nearing expiration.")
            finally:
                self.closeConnection()

    # ---------------------------------------------------------------------------------------------- [GROCERY LIST]
    
    # Add an item to the grocery list
    def addIngredientToGroceryList(self, name, quantity, unit):
        if not self.conn or not self.cursor:
            self.connectDatabase()

        if self.conn and self.cursor:
            try:
                self.cursor.execute("INSERT INTO grocerylist (name, quantity, unit) VALUES (%s, %s, %s)",
                                    (name, quantity, unit))
                self.conn.commit()
                print(f"Ingredient '{name}' added to grocery list.")
            except Error as e:
                print(e)
                print("Failed to add ingredient to grocery list.")
            finally:
                self.closeConnection()
                
    # Delete an item from the grocery list either by ID or name
    def deleteIngredientFromGroceryList(self, grocerylist_id=None, name=None):
        if not self.conn or not self.cursor:
            self.connectDatabase()

        if self.conn and self.cursor:
            try:
                if grocerylist_id is not None:
                    self.cursor.execute("DELETE FROM grocerylist WHERE grocerylist_id = %s", (grocerylist_id,))
                elif name is not None:
                    self.cursor.execute("DELETE FROM grocerylist WHERE name = %s", (name,))
                else:
                    print("No valid identifier provided for deletion.")
                    return

                self.conn.commit()
                if self.cursor.rowcount > 0:
                    print(f"Grocery list item {'with ID ' + str(grocerylist_id) if grocerylist_id else 'named ' + name} deleted successfully.")
                else:
                    print("Item not found or already deleted from grocery list.")
            except Error as e:
                print(e)
                print("Failed to delete ingredient from grocery list.")
            finally:
                self.closeConnection()              

    # Retrieve all ingredient names currently on the grocery list
    def getGroceryListIngredientNames(self):
        if not self.conn or not self.cursor:
            self.connectDatabase()

        ingredient_names = []
        if self.conn and self.cursor:
            try:
                query = "SELECT name FROM grocerylist ORDER BY name;"
                self.cursor.execute(query)
                rows = self.cursor.fetchall()
                for row in rows:
                    ingredient_names.append(row[0])
                
                if ingredient_names:
                    print("Ingredients on the Grocery List:")
                    for name in ingredient_names:
                        print(name)
                else:
                    print("The grocery list is currently empty.")
                
            except Error as e:
                print(e)
                print("Failed to retrieve ingredient names from the grocery list.")
            finally:
                self.closeConnection()
        return ingredient_names