import pantrydb_queries as pdb
from datetime import datetime, timedelta
import random

# List of products to be inserted into the pantry database
products = [
   # Seafood
    ("bacalhau", "kg"),
    ("sardinhas", "lata"),
    ("polvo", "kg"),
    ("amêijoas", "kg"),
    ("lulas", "kg"),

    # Meats
    ("frango", "kg"),
    ("perna de frango", "kg"),
    ("bife de vaca", "kg"),
    ("lombo de porco", "kg"),
    ("peru", "kg"),

    # Dairy
    ("queijo da serra", "kg"),
    ("leite", "l"),
    ("iogurte", "uni"),
    ("manteiga", "g"),
    ("requeijão", "g"),

    # Vegetables
    ("batatas", "kg"),
    ("tomates", "kg"),
    ("cenouras", "kg"),
    ("espinafres", "molho"),
    ("abóbora", "kg"),

    # Fruits
    ("laranjas", "kg"),
    ("maçãs", "kg"),
    ("bananas", "kg"),
    ("uvas", "kg"),
    ("melancia", "kg"),

    # Grains
    ("arroz", "kg"),
    ("feijão", "kg"),
    ("quinoa", "kg"),
    ("aveia", "kg"),
    ("farinha de trigo", "kg"),

    # Herbs and spices
    ("salsa", "g"),
    ("coentros", "g"),
    ("paprika", "g"),
    ("canela", "g"),
    ("sal", "kg"),

    # Nuts
    ("amêndoa", "kg"),
    ("noz", "kg"),
    ("castanhas", "kg"),
    ("pistácios", "kg"),
    ("amendoins", "kg"),

    # Oils and others
    ("azeite", "l"),
    ("vinagre", "l"),
    ("massa", "kg"),
    ("manteiga de amendoim", "g"),
    ("molho de tomate", "lata")
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
        for _ in range(random.randint(0, 1)):
            quantity = random.randint(1, 4)  # Random quantity between 1 and 4
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
