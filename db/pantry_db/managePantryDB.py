import mysql.connector
from mysql.connector import Error
from decimal import Decimal

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

    # Extending Conversion Factors for Weight and Volume
    #   The basic idea is that:
    #
    #   - 1 liter (l) of water = 1000 milliliters (ml) = 1000 grams (g)
    #   - 1 milliliter (ml) of water = 1 gram (g)
    #   - 1 kilogram (kg) of water = 1000 grams (g) = 1000 milliliters (ml)
    #
    conversion_factors = {
        # Volume to Weight (assuming density of water)
        'l': {'ml': Decimal('1000'), 'cl': Decimal('100'), 'dl': Decimal('10'), 'l': Decimal('1'), 'g': Decimal('1000'), 'kg': Decimal('1')},
        'ml': {'l': Decimal('0.001'), 'cl': Decimal('0.1'), 'dl': Decimal('0.01'), 'ml': Decimal('1'), 'g': Decimal('1'), 'mg': Decimal('1000')},
        'cl': {'ml': Decimal('10'), 'l': Decimal('0.01'), 'dl': Decimal('0.1'), 'cl': Decimal('1'), 'g': Decimal('10'), 'mg': Decimal('10000')},
        'dl': {'ml': Decimal('100'), 'l': Decimal('0.1'), 'cl': Decimal('10'), 'dl': Decimal('1'), 'g': Decimal('100'), 'kg': Decimal('0.1')},

        # Weight to Volume (assuming density of water)
        'g': {'kg': Decimal('0.001'), 'mg': Decimal('1000'), 'g': Decimal('1'), 'ml': Decimal('1'), 'l': Decimal('0.001')},
        'kg': {'g': Decimal('1000'), 'mg': Decimal('1000000'), 'kg': Decimal('1'), 'l': Decimal('1'), 'ml': Decimal('1000')},
        'mg': {'g': Decimal('0.001'), 'kg': Decimal('0.000001'), 'mg': Decimal('1'), 'ml': Decimal('0.001')},

        # Non-standard units (examples for cooking, assuming conversions to ml or g)
        'lata': {'ml': Decimal('330')},
        'colher de sopa': {'ml': Decimal('15')},
        'colher de chá': {'ml': Decimal('5')},
        'copo': {'ml': Decimal('200')},
        'garrafa': {'l': Decimal('1.5')},
        'tablete': {'g': Decimal('200')},
        'pacote': {'kg': Decimal('1')},
        'saqueta': {'g': Decimal('5')}
    }
    
    # ---------------------------------------------------------------------------------------------- [CONVERT MEASURE]
    
    # Convert a quantity from one unit to another using a dictionary of conversion factors 
    def convert_measure(self, quantity, from_unit, to_unit, conversion_factors):
        from_unit = from_unit.lower().strip('s')  # Normalize the from_unit name
        to_unit = to_unit.lower().strip('s')  # Normalize the to_unit name

        def find_conversion(current_quantity, current_unit, target_unit, visited_units=set()):
            # Direct conversion case
            if target_unit in conversion_factors[current_unit]:
                return current_quantity * conversion_factors[current_unit][target_unit], target_unit

            # Recursive conversion case: find a path through an intermediary
            for intermediate_unit in conversion_factors[current_unit]:
                if intermediate_unit not in visited_units:  # Avoid cycles
                    visited_units.add(intermediate_unit)
                    intermediate_quantity = current_quantity * conversion_factors[current_unit][intermediate_unit]
                    # Recursively convert from intermediate unit to target unit
                    result = find_conversion(intermediate_quantity, intermediate_unit, target_unit, visited_units)
                    if result:
                        return result
            return None

        # Start the conversion process
        result = find_conversion(quantity, from_unit, to_unit)
        if result:
            return result
        else:
            raise ValueError("No valid conversion path found from {} to {}".format(from_unit, to_unit))

    # ---------------------------------------------------------------------------------------------- [STOCK List]

    # [UNUSED] Insert a new type of stock item into the stock table. 
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
        else:
            print("Failed to connect to the database.")

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
                    cursor.execute("INSERT INTO stock (name) VALUES (%s)", (name,))
                    conn.commit()
                    print(f"Stock item '{name}' inserted successfully.")
                    #self.insertStock_table(name)
                    
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
        else:
            print("Failed to connect to the database.")

    # Remove [update] stock item from stock_details           
    def removeStock(self, name, quantity, unit):
        conn, cursor = self.connectDatabase()
        if conn is not None and cursor is not None:
            try:
                # Fetch stock_id using the name
                cursor.execute("SELECT stock_id FROM stock WHERE name = %s", (name,))
                stock_id_result = cursor.fetchone()
                if stock_id_result:
                    stock_id = stock_id_result[0]
                    # Fetch the stock detail with the nearest expiration date for the given unit
                    cursor.execute("""
                    SELECT detail_id, quantity, unit
                    FROM stock_details
                    WHERE stock_id = %s
                    ORDER BY expiration_date ASC
                    LIMIT 1
                    """, (stock_id,))
                    stock_detail = cursor.fetchone()
                                
                    if stock_detail:
                        detail_id, stock_quantity, stock_unit = stock_detail
                        print(f"Found stock detail for '{name}' with quantity {stock_quantity} {stock_unit} in stock_details.")
                        # If the unit is diferent, convert the quantity to the same unit
                        if stock_unit != unit:
                            new_quantity, new_unit = self.convert_measure(quantity, unit, stock_unit, self.conversion_factors)
                            print(f"Converted {quantity} {unit} to {new_quantity} {new_unit}.")
                        else:
                            new_quantity, new_unit = quantity, unit
                            print(f"Units {new_quantity} {new_unit}.")
                            
                        if new_quantity == stock_quantity:
                            # Delete the row if quantity to remove is equal to current quantity
                            cursor.execute("DELETE FROM stock_details WHERE detail_id = %s", (detail_id,))
                            print(f"Removed {stock_quantity} {new_unit} of '{name}' from stock_details.")
                        elif new_quantity < stock_quantity:
                            # Update the row with the new quantity
                            updated_quantity = Decimal(stock_quantity) - Decimal(new_quantity)
                            print(f"Removing {new_quantity} {new_unit} of '{name}' from stock_details.")
                            print(f"New quantity will be {updated_quantity} {stock_unit}.")
                            cursor.execute("UPDATE stock_details SET quantity = %s WHERE detail_id = %s", (updated_quantity, detail_id))
                            print(f"Updated '{name}' quantity to {updated_quantity} {stock_unit} in stock_details.")
                        elif new_quantity > stock_quantity:
                            # Search if there is another stock detail with the same name and that we could remove too
                            cursor.execute("DELETE FROM stock_details WHERE detail_id = %s", (detail_id,))
                            conn.commit()
                            print(f"Removed {stock_quantity} {new_unit} of '{name}' from stock_details.")
                            updated_quantity = Decimal(new_quantity) - Decimal(stock_quantity)
                            print(f"Searching for another stock in order to remove the remaining {updated_quantity} {new_unit} of '{name}' from stock_details.")
                            # Fetch the stock detail with the nearest expiration date for the given unit
                            self.removeStock(name, updated_quantity, stock_unit)
                            
                        conn.commit()
                    else:
                        print(f"No stock detail found for '{name}' with unit '{unit}'.")
                else:
                    print(f"Stock item '{name}' does not exist in the database.")
            except Error as e:
                print(e)
                print(f"Failed to remove stock item '{name}'")
            finally:
                cursor.close()
                conn.close()
                print("Connection closed.")
        else:
            print("Failed to connect to the database.")

    # ---------------------------------------------------------------------------------------------- [GROCERY List]
    
    # Insert a new Stock item into grocery_list
    def insertGrocery(self, name):
        conn, cursor = self.connectDatabase()
        if conn is not None and cursor is not None:
            try:
                cursor.execute("SELECT stock_id FROM stock WHERE name = %s", (name,))
                stock_id_result = cursor.fetchone()
                if stock_id_result:
                    print(f"Stock item '{name}' exists in the database.")
                else:
                    print(f"Stock item '{name}' does not exist in the database, inserting it now.")
                    cursor.execute("INSERT INTO stock (name) VALUES (%s)", (name,))
                    conn.commit()
                    print(f"Stock item '{name}' inserted successfully.")
    
                # Insert into grocery_list
                cursor.execute("INSERT INTO grocerylist (name) VALUES (%s)", (name,))
                conn.commit()
                print(f"Stock item '{name}' inserted successfully in the GROCERY LIST.")
            except Error as e:
                print(e)
                print(f"Failed to insert stock item '{name}'")
            finally:
                cursor.close()
                conn.close()
                print("Connection closed.")
        else:
            print("Failed to connect to the database.")
    
    # Remove a Stock item from grocery_list
    def removeGrocery(self, name):
        conn, cursor = self.connectDatabase()
        if conn is not None and cursor is not None:
            try:
                cursor.execute("DELETE FROM grocerylist WHERE name = %s", (name,))
                conn.commit()
                print(f"Stock item '{name}' removed successfully from the GROCERY LIST.")
            except Error as e:
                print(e)
                print(f"Failed to remove stock item '{name}'")
            finally:
                cursor.close()
                conn.close()
                print("Connection closed.")
        else:
            print("Failed to connect to the database.")
    
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
    # Test inserting details for an existing stock item
    db_manager.insertStock("Apples", 15, "kg", "2024-08-01")
    print("----------------------------------------------")
    print("\n")
    # Test inserting a new stock item that does not exist in the stock table
    db_manager.insertStock("Oranges", 20, "kg", "2024-02-01")
    print("----------------------------------------------")
    print("\n")
    
    # Test removing stock EQUAL to the stock item in the stock_details 
    db_manager.removeStock("Apples", 10000, "g")
    print("----------------------------------------------")
    print("\n")
    # Test removing stock item stock item SMALLER than the stock item in the stock_details
    db_manager.removeStock("Apples", 3000, "g")
    print("----------------------------------------------")
    print("\n")
    # Test removing stock item stock item BIGGER than the stock item in the stock_details
    db_manager.removeStock("Apples", 10000, "g")
    print("----------------------------------------------")
    print("\n")
    # Test inserting a item in the grocery list
    db_manager.insertGrocery("Oranges")
    print("----------------------------------------------")
    print("\n")
    # Test inserting a item in the grocery list
    db_manager.insertGrocery("Garlic")
    print("----------------------------------------------")
    print("\n")
    # Test removing a item in the grocery list
    db_manager.removeGrocery("Oranges")
    print("----------------------------------------------")
    print("\n")
    
    # CONVERT_MEASURE : Example usage:
    # inicial_quantity = 1
    # inicial_unit = 'lata'
    # quantity, unit = db_manager.convert_measure(inicial_quantity, inicial_unit, 'kg', db_manager.conversion_factors)
    # print(f"{inicial_quantity} {inicial_unit} is approximately {quantity} {unit}")  
    # quantity, unit = db_manager.convert_measure(inicial_quantity, inicial_unit, 'l', db_manager.conversion_factors)
    # print(f"{inicial_quantity} {inicial_unit} is approximately {quantity} {unit}")  