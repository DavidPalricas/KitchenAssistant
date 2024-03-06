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

    def insertstock(self, name, quantity, unit, calories, source_url):
        if not self.conn or not self.cursor:
            self.connectDatabase()
        
        if self.conn and self.cursor:
            try:
                self.cursor.execute("INSERT INTO stocks (name, quantity, unit, calories, source_url) VALUES (%s, %s, %s, %s, %s)", 
                                    (name, quantity, unit, calories, source_url))
                self.conn.commit()
                print(f"stock '{name}' inserted successfully.")
            except Error as e:
                print(e)
                print(f"Failed to insert stock '{name}'")
            finally:
                self.closeConnection()

    def deletestock(self, stock_id=None, name=None):
        if not self.conn or not self.cursor:
            self.connectDatabase()

        if self.conn and self.cursor:
            try:
                if stock_id is not None:
                    self.cursor.execute("DELETE FROM stocks WHERE stock_id = %s", (stock_id,))
                elif name is not None:
                    self.cursor.execute("DELETE FROM stocks WHERE name = %s", (name,))
                else:
                    print("No valid identifier provided for deletion.")
                    return

                self.conn.commit()
                if self.cursor.rowcount > 0:
                    print(f"stock {'with ID ' + str(stock_id) if stock_id else 'named ' + name} deleted successfully.")
                else:
                    print("stock not found or already deleted.")
            except Error as e:
                print(e)
                print("Failed to delete stock.")
            finally:
                self.closeConnection()
       
    def getAllstocksDetails(self):
        if not self.conn or not self.cursor:
            self.connectDatabase()

        stocks_details = []
        if self.conn and self.cursor:
            try:
                query = "SELECT name, quantity, unit FROM stocks ORDER BY name;"
                self.cursor.execute(query)
                rows = self.cursor.fetchall()
                for row in rows:
                    stocks_details.append(row)
                
                if stocks_details:
                    print("All stocks details (Name, Quantity, Unit):")
                    for detail in stocks_details:
                        print(f"Name: {detail[0]}, Quantity: {detail[1]}, Unit: {detail[2]}")
                else:
                    print("No stocks found in the database.")
                
            except Error as e:
                print(e)
                print("Failed to retrieve all stocks details from the database.")
            finally:
                self.closeConnection()
        return stocks_details   
    
    # ---------------------------------------------------------------------------------------------- [GROCERY LIST]
                
    def addstockToGroceryList(self, stock_id, quantity, unit):
        if not self.conn or not self.cursor:
            self.connectDatabase()

        if self.conn and self.cursor:
            try:
                # First, check if the stock exists in the 'stocks' table
                self.cursor.execute("SELECT stock_id FROM stocks WHERE stock_id = %s", (stock_id,))
                if not self.cursor.fetchone():
                    print(f"No stock found with ID {stock_id}. Please add it to the stocks table first.")
                    return
                
                # If the stock exists, add it to the grocery list
                self.cursor.execute("INSERT INTO grocerylists (stock_id, quantity, unit) VALUES (%s, %s, %s)",
                                    (stock_id, quantity, unit))
                self.conn.commit()
                print(f"stock with ID {stock_id} added to grocery list.")
            except Error as e:
                print(e)
                print("Failed to add stock to grocery list.")
            finally:
                self.closeConnection()
                
    def deletestockFromGroceryList(self, grocerylist_id=None, stock_id=None):
        if not self.conn or not self.cursor:
            self.connectDatabase()

        if self.conn and self.cursor:
            try:
                if grocerylist_id is not None:
                    # Delete by grocerylist_id
                    self.cursor.execute("DELETE FROM grocerylists WHERE grocerylist_id = %s", (grocerylist_id,))
                elif stock_id is not None:
                    # Delete all entries for a specific stock_id
                    self.cursor.execute("DELETE FROM grocerylists WHERE stock_id = %s", (stock_id,))
                else:
                    print("No valid identifier provided for deletion.")
                    return

                self.conn.commit()
                if self.cursor.rowcount > 0:
                    print(f"Grocery list item{'s' if stock_id else ''} {'with ID ' + str(grocerylist_id) if grocerylist_id else 'for stock ID ' + str(stock_id)} deleted successfully.")
                else:
                    print("Item not found or already deleted from grocery list.")
            except Error as e:
                print(e)
                print("Failed to delete stock from grocery list.")
            finally:
                self.closeConnection()       

    def getGroceryListstockNames(self):
        if not self.conn or not self.cursor:
            self.connectDatabase()

        stock_names = []
        if self.conn and self.cursor:
            try:
                query = """
                SELECT i.name 
                FROM stocks i
                JOIN grocerylists g ON i.stock_id = g.stock_id
                ORDER BY i.name;
                """
                self.cursor.execute(query)
                rows = self.cursor.fetchall()
                for row in rows:
                    stock_names.append(row[0])
                
                if stock_names:
                    print("stocks on the Grocery List:")
                    for name in stock_names:
                        print(name)
                else:
                    print("The grocery list is currently empty.")
                
            except Error as e:
                print(e)
                print("Failed to retrieve stock names from the grocery list.")
            finally:
                self.closeConnection()
        return stock_names