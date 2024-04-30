"""
@brief Módulo para gerir operações na base de dados de uma despensa, incluindo inserções, remoções e conversões de unidades.

Este módulo utiliza o MySQL para gerir uma base de dados de itens de despensa, 
permitindo inserir, remover, converter e procurar itens com detalhes como quantidade e data de validade. 
As operações são realizadas assumindo que todos os itens podem ser convertidos entre unidades de medida baseadas 
no sistema métrico e algumas unidades não-padrão com base em fatores de conversão predefinidos.

@details As principais funções do módulo incluem:
- `connectDatabase()`: Conecta-se à base de dados MySQL.
- `insertStock()`, `removeStock()`: Funções para inserir e remover itens da despensa.
- `getStockDetails()`, `searchStock()`: Funções para procurar detalhes dos itens armazenados.
- `convert_measure()`: Converte quantidades entre diferentes unidades de medida usando fatores de conversão.
- `insertGrocery()`, `removeGrocery()`, `showAllGrocery()`: Gere uma lista de compras separada.

@code
    result = insertStock("Tomates", 5, "kg", "2025-12-01")
    print(result)
    //Output: 
    "Item 'Tomates' inserido com sucesso com data de validade '2025-12-01'"
@endcode

@note Para a execução deste módulo é necessário ter instalado e configurado o MySQL, assim como a biblioteca mysql.connector do Python.

@see https://dev.mysql.com/doc/
@see https://pypi.org/project/mysql-connector-python/

"""
import mysql.connector
from mysql.connector import Error
from decimal import Decimal

def connectDatabase():
    """
    @brief Conecção à base de dados 'pantry_database'.
    @details Tenta conectar-se à base de dados 'pantry_database' usando as credenciais fornecidas. 
    Retorna o objeto de conexão e cursor se bem sucedido.
    
    @return (conn, cursor) Tuplo contendo o objeto de conexão e o cursor se a conexão for bem sucedida, None caso contrário.
    
    @note As credenciais de acesso à base de dados estão definidas no corpo da função e podem ser alteradas conforme necessário.
    
    @warning Esta conecção não é segura e deve ser usada apenas para fins de demonstração e testes. 
    """
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
        

## @var conversion_factors
# @brief Dicionário de fatores de conversão para unidades de volume e peso.
# @details Este dicionário contém fatores de conversão para unidades de volume e peso,
# permitindo a conversão entre diferentes unidades de medida com base em fatores predefinidos.
#
# @note Os fatores de conversão são baseados na densidade da água para unidades de volume e peso.
#
# A ideia básica é:
# - 1 litro (l) de água = 1000 mililitros (ml) = 1000 gramas (g)
# - 1 mililitro (ml) de água = 1 grama (g)
# - 1 quilograma (kg) de água = 1000 gramas (g) = 1000 mililitros (ml)
#
# @note O dicionário pode ser expandido para incluir mais unidades e fatores de conversão conforme necessário.
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
    'saqueta': {'g': Decimal('5')},
    'uni': {'g': Decimal('200')},
    'caixa': {'saqueta': Decimal('20')}
}

# ---------------------------------------------------------------------------------------------- [CONVERT MEASURE]

# Convert a quantity from one unit to another using a dictionary of conversion factors 
def convert_measure(quantity, from_unit, to_unit, conversion_factors):
    """
    @brief Convert Uma quantidade de uma unidade para outra.
    @details Converte uma quantidade de uma unidade para outra, usando um dicionário de fatores de conversão. 
    Trata casos diretos e requer conversões recursivas se necessário.
    
    @param quantity <int> Quantidade a ser convertida.
    @param from_unit <string> Unidade inicial.
    @param to_unit <string> Unidade final.
    @param conversion_factors <dict> Dicionário contendo os fatores de conversão.
    
    @return <tuplo> contendo a quantidade convertida e a unidade final.
    
    @note Funcção usada para podermos subtrair/adicionar quantidades em unidades diferentes do mesmo produto
    
    @warning ValueError Se não encontrar um caminho de conversão válido.
    """
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
def insertStock_table(name):
    conn, cursor = connectDatabase()
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
def insertStock(name, quantity, unit, expiration_date):
    """
    @brief Insere um item no stock da despensa com os detalhes fornecidos.
    @details Insere um item no stock da despensa com os detalhes fornecidos, incluindo a data de validade. 
    Se o item já existir, apenas atualiza os detalhes.
    
    @param name <string> Nome do item.
    @param quantity <int> Quantidade do item a ser inserido.
    @param unit <string> Unidade de medida da quantidade do item.
    @param expiration_date <string> Data de validade do item.
    
    @return <string> Mensagem de sucesso ou falha.
    """
    conn, cursor = connectDatabase()
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
def removeStock(name, quantity, unit):
    """
    @brief Remove ou atualiza a quantidade de um item.
    @details Remove ou atualiza a quantidade de um item no stock baseado no nome e na quantidade especificada. 
    Considera a conversão de unidades se necessário.
    
    @param name <string> Nome do item a ser removido.
    @param quantity <string> Quantidade do item a ser removida.
    @param unit <Int> Unidade de medida da quantidade do item.
    
    @return <string> Mensagem de sucesso ou falha.
    """
    conn, cursor = connectDatabase()
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
                        new_quantity, new_unit = convert_measure(quantity, unit, stock_unit, conversion_factors)
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
                        removeStock(name, updated_quantity, stock_unit)
                        
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

# Get all stock details
def getStockDetails():
    """
    @brief Procura e retorna todos os detalhes de cada item em stock.
    @details Procura e retorna todos os detalhes de cada item em stock, incluindo nome, quantidade, unidade e data de validade.
    
    @return <list> Lista de strings descrevendo cada item em stock, ou None se ocorrer um erro.
    """
    conn,cursor = connectDatabase()
    if conn is not None:
        try:
            query = """
            SELECT s.name, sd.quantity, sd.unit, sd.expiration_date
            FROM stock_details sd
            JOIN stock s ON sd.stock_id = s.stock_id
            ORDER BY s.name, sd.expiration_date ASC
            """
            cursor.execute(query)
            rows = cursor.fetchall()
            result = [
                f"{row[0]} {float(row[1])} {row[2]}, Data de Validade : {row[3].strftime('%Y/%m/%d')}"
                for row in rows
            ]
            return result
        except Error as e:
            print(f"Error fetching stock details: {e}")
            return None
        finally:
            cursor.close()
            conn.close()
    else:
        return None

# Search for a stock item in the pantry table
def searchStock(name):
    """
    @brief Procura por um item específico no stock.
    @details Procura por um produto específico no stock e retorna a soma total das quantidades numa unidade base, 
    convertendo as unidades conforme necessário.
    
    @param name <string> Nome do item a ser procurado no stock.
    @return <string> Descrição da quantidade total e unidade do produto, ou mensagem de erro.
    """
    conn, cursor = connectDatabase()
    if conn is not None and cursor is not None:
        try:
            # Fetch stock_id using the name
            cursor.execute("SELECT stock_id FROM stock WHERE name = %s", (name,))
            stock_id_result = cursor.fetchone()
            if stock_id_result:
                stock_id = stock_id_result[0]

                # Fetch all stock details for this stock_id
                cursor.execute("""
                SELECT quantity, unit
                FROM stock_details
                WHERE stock_id = %s
                """, (stock_id,))
                
                total_quantity = Decimal(0)
                base_unit = None
                
                for quantity, unit in cursor.fetchall():
                    if base_unit is None:
                        # Initialize base unit if not set
                        base_unit = unit
                        total_quantity += Decimal(quantity)
                    elif unit == base_unit:
                        # Sum directly if unit is the same
                        total_quantity += Decimal(quantity)
                    else:
                        # Convert and then sum if different units
                        converted_quantity, _ = convert_measure(Decimal(quantity), unit, base_unit, conversion_factors)
                        total_quantity += converted_quantity

                return f"{total_quantity} {base_unit}"
            else:
                return f"No stock found for '{name}'."
        except Exception as e:
            return f"Database error: {str(e)}"
        finally:
            cursor.close()
            conn.close()
    else:
        return "Failed to connect to the database."

# remove all entries of a stock item from stock_details
def removeAllStock(name):
    """
    @brief Remove todos os registos de um item.
    @details Remove todos os registos de um item específico (name) da tabela stock_details (despensa).
    
    @param name <string> Nome do item cujos detalhes devem ser removidos completamente.
    
    @return <string> Mensagem de sucesso ou de erro.
    """
    conn, cursor = connectDatabase()
    if conn is not None:
        try:
            cursor.execute("SELECT stock_id FROM stock WHERE name = %s", (name,))
            stock_id_result = cursor.fetchone()
            if stock_id_result:
                stock_id = stock_id_result[0]
                cursor.execute("DELETE FROM stock_details WHERE stock_id = %s", (stock_id,))
                conn.commit()
                message = f"Removed all stock details for '{name}' from stock_details."
                print(message)
                return message
                
            else:
                message = f"Stock item '{name}' does not exist in the database."
                print(message)
                return message
        except Error as e:
            print(e)
            message = f"Failed to remove all stock details for '{name}'"
            print(message)
            return message
        finally:
            cursor.close()
            conn.close()
            print("Connection closed.")
    else:
        print("Failed to connect to the database.")
        
# clear all entries from stock_details table
def clearStock():
    """
    @brief Limpa a despensa.
    @details Limpa todos os registos da tabela de stock_details (Despensa).
    
    @return Clear all stock details from stock_details | Failed to clear all stock details from stock_details.
    """
    conn, cursor = connectDatabase()
    if conn is not None:
        try:
            cursor.execute("DELETE FROM stock_details")
            conn.commit()
            print("Cleared all stock details from stock_details.")
        except Error as e:
            print(e)
            print("Failed to clear all stock details from stock_details.")
        finally:
            cursor.close()
            conn.close()
            print("Connection closed.")
    else:
        print("Failed to connect to the database.")
    
# ---------------------------------------------------------------------------------------------- [GROCERY List]

# Insert a new Stock item into grocery_list
def insertGrocery(name):
    """
    @brief Insere um item na lista de compras.
    @details Insere um item na lista de compras, verificando primeiro se ele já existe no stock. 
    Se não existir, o item é adicionado ao estoque e à lista de compras.
    
    @param name <string> Nome do item a ser inserido na lista de compras.
    
    @return <string> Mensagem de sucesso ou falha.
    """
    conn, cursor = connectDatabase()
    if conn is not None and cursor is not None:
        try:
            cursor.execute("SELECT stock_id FROM stock WHERE name = %s", (name,))
            stock_id_result = cursor.fetchone()
            if stock_id_result:
                print(f"Stock item '{name}' exists in the database.")
                message = f"Stock item '{name}' exists in the database."
            else:
                print(f"Stock item '{name}' does not exist in the database, inserting it now.")
                cursor.execute("INSERT INTO stock (name) VALUES (%s)", (name,))
                conn.commit()
                print(f"Stock item '{name}' inserted successfully.")
                message = f"Stock item '{name}' inserted successfully."

            # Check id the stock item already exists in the grocery list
            cursor.execute("SELECT name FROM grocerylist WHERE name = %s", (name,))
            existing_grocery = cursor.fetchone()
            
            if existing_grocery:
                print(f"Stock item '{name}' already exists in the GROCERY LIST.")
                message = f" Stock item '{name}' already exists in the GROCERY LIST."
            else:
                # Insert into grocery_list
                cursor.execute("INSERT INTO grocerylist (name) VALUES (%s)", (name,))
                conn.commit()
                print(f"Stock item '{name}' inserted successfully in the GROCERY LIST.")
                message = f" Stock item '{name}' inserted successfully in the GROCERY LIST."
            return message
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
def removeGrocery(name):
    """
    @brief Remove um item da lista de compras.
    @details Remove um item da lista de compras baseado no nome fornecido.
    
    @param name <string> Nome do item a ser removido da lista de compras.
    
    @return <string> Mensagem de sucesso ou falha.
    """
    conn, cursor = connectDatabase()
    if conn is not None and cursor is not None:
        try:
            cursor.execute("DELETE FROM grocerylist WHERE name = %s", (name,))
            conn.commit()
            print(f"Stock item '{name}' removed successfully from the GROCERY LIST.")
            message = f"Stock item '{name}' removed successfully from the GROCERY LIST."
            return message
        except Error as e:
            print(e)
            print(f"Failed to remove stock item '{name}'")
        finally:
            cursor.close()
            conn.close()
            print("Connection closed.")
    else:
        print("Failed to connect to the database.")

# Get all items in the grocery list
def showAllGrocery():
    """
    @brief Mostra todos os itens na lista de compras.
    @details Mostra todos os itens na lista de compras, retornando uma lista de nomes de itens.
    
    
    @return <list> Lista de nomes dos itens na lista de compras, ou None se ocorrer um erro.
    """
    conn, cursor = connectDatabase()
    if conn is not None and cursor is not None:
        try:
            cursor.execute("SELECT name FROM grocerylist")
            rows = cursor.fetchall()
            names = [row[0] for row in rows]
            return names
        except Error as e:
            print(e)
            print(f"Failed to show grocery list")
            return None
        finally:
            cursor.close()
            conn.close()
            print("Connection closed.")
    else:
        print("Failed to connect to the database.")

# clear all entries from grocery_list table
def clearGrocery():
    """
    @brief Limpa a lista de compras.
    @details Limpa todos os registos da tabela da lista de compras.
    
    @return Clear all stock details from grocerylist | Failed to clear all stock details from grocerylist.
    """
    conn, cursor = connectDatabase()
    if conn is not None:
        try:
            cursor.execute("DELETE FROM grocerylist")
            conn.commit()
            print("Cleared all stock details from grocerylist.")
        except Error as e:
            print(e)
            print("Failed to clear all stock details from grocerylist.")
        finally:
            cursor.close()
            conn.close()
            print("Connection closed.")
    else:
        print("Failed to connect to the database.")

# ---------------------------------------------------------------------------------------------- [TESTS]

#removeAllStock("Azeite")
#clearStock()
#print(searchStock("banana"))

# print("\n")
# # Test inserting a new stock item and its details
#insertStock("Azeite", 1, "l", "2024-01-01")
#print("----------------------------------------------")
#print("\n")
# # Test inserting details for an existing stock item
#insertStock("Azeite", 6, "l", "2024-05-01")
#print("----------------------------------------------")
#print("\n")
# # Test inserting details for an existing stock item
#insertStock("Apples", 15, "kg", "2024-08-01")
#print("----------------------------------------------")
#print("\n")
# # Test inserting a new stock item that does not exist in the stock table
#insertStock("Oranges", 20, "kg", "2024-02-01")
#print("----------------------------------------------")
#print("\n")

# Test showing all stock details
#print(getStockDetails())
#print("----------------------------------------------")
#print("\n")
# # Test removing stock EQUAL to the stock item in the stock_details 
# removeStock("Azeite", 50, "ml")
# print("----------------------------------------------")
# print("\n")
# # Test removing stock item stock item SMALLER than the stock item in the stock_details
# removeStock("Apples", 3000, "g")
# print("----------------------------------------------")
# print("\n")
# # Test removing stock item stock item BIGGER than the stock item in the stock_details
# removeStock("Apples", 10000, "g")
# print("----------------------------------------------")
# print("\n")
# Test inserting a item in the grocery list
#insertGrocery("Oranges")
#print("----------------------------------------------")
#print("\n")
# Test inserting a item in the grocery list
#insertGrocery("azeite")
#print("----------------------------------------------")
#print("\n")
# Test showing all items in the grocery list
#print(showAllGrocery())
#print("----------------------------------------------")
#print("\n")
# # Test removing a item in the grocery list
#removeGrocery("azeite")
#print("----------------------------------------------")
#print("\n")

# CONVERT_MEASURE : Example usage:
# inicial_quantity = 1
# inicial_unit = 'lata'
# quantity, unit = convert_measure(inicial_quantity, inicial_unit, 'kg',conversion_factors)
# print(f"{inicial_quantity} {inicial_unit} is approximately {quantity} {unit}")  
# quantity, unit = convert_measure(inicial_quantity, inicial_unit, 'l', conversion_factors)
# print(f"{inicial_quantity} {inicial_unit} is approximately {quantity} {unit}")  
