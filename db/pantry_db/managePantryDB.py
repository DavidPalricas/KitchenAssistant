import mysql.connector
from mysql.connector import Error

class ManagePantryDB:
    def __init__(self):
        pass

    def connectDatabase(self):
        try:
            conn = mysql.connector.connect(
                host='localhost',
                user='admin',
                password='admin',
                database='pantry_database'
            )
            if conn.is_connected():
                cursor = conn.cursor()
                print("Connected to pantry database")
                return conn, cursor
        except Error as e:
            print(e)
            print("Failed to connect to pantry database")
            return None, None

    # ---------------------------------------------------------------------------------------------- [STOCK List]

    # Insert a new type of stock item into the stock table.
    def insertStock_table(self, name):
        conn, cursor = self.connectDatabase()
        if conn is not None and cursor is not None:
            try:
                cursor.execute("SELECT name FROM stock WHERE name = %s", (name,))
                existing_stock = cursor.fetchone()
                
                if existing_stock:
                    stock_id = existing_stock
                    print(f"Stock item '{name}' already exists in the database.")
                else:
                    cursor.execute("INSERT INTO stock (name) VALUES (%s)", (name,))
                    conn.commit()
                    print(f"Stock item '{name}' inserted successfully.")
            except Error as e:
                print(e)
                print(f"Failed to insert stock item '{name}'")
            finally:
                cursor.close()
                conn.close()
                print("Connection closed.")

    # Insert a new Stock item into stock_details with expiration date
    def insertStock(self, name, quantity, unit, expiration_date):
        conn, cursor = self.connectDatabase()
        if conn is not None and cursor is not None:
            try:
                cursor.execute("SELECT stock_id FROM stock WHERE name = %s", (name,))
                stock_id_result = cursor.fetchone()
                if stock_id_result:
                    stock_id = stock_id_result[0]
                else:
                    print(f"Stock item '{name}' does not exist in the database, inserting it now.")
                    self.insertStock_table(name)
                    # Fetch the new stock_id for the just inserted item
                    cursor.execute("SELECT stock_id FROM stock WHERE name = %s", (name,))
                    new_stock_id_result = cursor.fetchone()
                    print(" STOCK ID FROM THE NEW ADDED PRODUCT",new_stock_id_result)
                    if new_stock_id_result:
                        stock_id = new_stock_id_result[0]
                    else:
                        print("Failed to fetch stock_id after insertion.")
                        return

                # Insert into stock_details
                cursor.execute("INSERT INTO stock_details (stock_id, quantity, unit, expiration_date) VALUES (%s, %s, %s, %s)", (stock_id, quantity, unit, expiration_date))
                conn.commit()
                print(f"Stock item '{name}' with expiration date '{expiration_date}' inserted successfully in the PantryDB.")
            except Error as e:
                print(e)
                print(f"Failed to insert stock item '{name}'")
            finally:
                cursor.close()
                conn.close()
                print("Connection closed.")

                

    # ---------------------------------------------------------------------------------------------- [GROCERY List]
    
    
    
    
    
    
    
if __name__ == "__main__":
        
    db_manager = ManagePantryDB()

    print("\n")
    # Test inserting a new stock item and its details
    db_manager.insertStock("Apples", 10, "kg", "2024-01-01")
    print("----------------------------------------------")
    print("\n")
    # Test inserting details for an existing stock item
    db_manager.insertStock("Apples", 5, "kg", "2024-05-01")
    print("----------------------------------------------")
    print("\n")
    # Test inserting a new stock item that does not exist in the stock table
    db_manager.insertStock("Oranges", 20, "kg", "2024-02-01")
    print("----------------------------------------------")
    print("\n")