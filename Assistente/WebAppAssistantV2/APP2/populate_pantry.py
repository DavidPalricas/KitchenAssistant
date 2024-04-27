import pantrydb_queries as pdb
from datetime import datetime, timedelta
import random

# List of products to be inserted into the pantry database
products = [
    ("arroz", "kg"),
    ("feijão", "kg"),
    ("azeite", "l"),
    ("massa", "kg"),
    ("açúcar", "kg"),
    ("sal", "kg"),
    ("farinha", "kg"),
    ("biscoitos", "pacote"),
    ("café", "g"),
    ("chá", "caixa"),
    ("leite", "l"),
    ("tomate pelado", "lata"),
    ("atum", "lata"),
    ("sardinhas enlatadas", "lata"),
    ("pão", "uni"),
    ("manteiga", "g"),
    ("maçãs", "kg"),
    ("bananas", "kg"),
    ("bifanas", "kg"),
    ("frango", "kg"),
    ("salmão", "kg")
]

grocery_items = [
    "vinho",
    "oléo",
    "pimenta Preta",
    "pato",
    "bacalhau",
    "repolho",
    "alho",
    "cebola",
    "cenoura",
    "batata",
    "bróculos",
    "couve",
    "camarão"
]

# Function to populate the pantry database
def populate_pantry():
    today = datetime.now()
    for name, unit in products:
        # Randomize the quantity and create between 1 and 3 entries per product
        for _ in range(random.randint(1, 3)):
            quantity = random.randint(1, 5)  # Random quantity between 1 and 5
            # Generate a random expiration date within the next two years
            expiration_date = today + timedelta(days=random.randint(30, 730))
            expiration_date_str = expiration_date.strftime('%Y-%m-%d')
            # Insert the stock item into the database
            pdb.insertStock(name, quantity, unit, expiration_date_str)
            
def populate_shopping_list():
    for name in grocery_items:
        message = pdb.insertGrocery(name)
        print(message)  # This will print the outcome of each insert operation


# Call the function to populate the database
populate_pantry()
populate_shopping_list()
