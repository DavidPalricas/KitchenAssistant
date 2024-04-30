"""
@brief Script para povoar a base de dados despensa e a lista de compras.

Este script utiliza o módulo `pantrydb_queries` para inserir uma série de produtos alimentares e itens na lista de compras 
de uma base de dados. É adequado para a inicialização de dados no sistema ( PANTRY_DB ).

@details Os produtos são definidos numa lista de tuplos, cada um contendo o nome do produto e a unidade de medida.
A lista de compras é composta por itens que serão adicionados diretamente à lista de compras na base de dados.

O script executa duas funções principais:
- `populate_pantry()`: Insere produtos na base de dados com quantidades e datas de validade aleatórias.
- `populate_shopping_list()`: Insere itens na lista de compras.

@code
    //Executar este script irá povoar a base de dados com produtos e adicionar itens à lista de compras.
    populate_pantry()
    populate_shopping_list()
@endcode

@note É necessário que a base de dados esteja configurada e acessível conforme especificado no módulo `pantrydb_queries`.
"""
import pantrydb_queries as pdb
from datetime import datetime, timedelta
import random


## @var products
# @brief Lista de produtos com as respetivas unidades de medida.
# @details Esta lista contém uma variedade de produtos alimentares com as respetivas unidades de medida,
# que serão inseridos na base de dados da despensa.
#
# @note Esta lista pode ser expandida conforme necessário para incluir mais produtos.
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

## @var grocery_items
# @brief Lista de itens a adicionar à lista de compras.
# @details Esta lista contém uma série de itens que serão adicionados à lista de compras na base de dados.
#
# @note Esta lista pode ser expandida conforme necessário para incluir mais itens.
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
    """
    @brief Função para povoar a base de dados pantry_db.
    @details Insere produtos na base de dados com quantidades e datas de validade aleatórias.
    Cada produto pode ter entre 0 e 1 entradas com quantidades de 1 a 4 e datas de validade
    que variam de 30 a 730 dias a partir da data atual.
    
    @note Esta função utiliza a função `insertStock` do módulo `pantrydb_queries` para inserir os produtos na base de dados.
    """
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
    """
    @brief Função para adicionar itens à lista de compras.
    @details  Adiciona itens especificados à lista de compras na base de dados.
    Cada inserção é registada e o resultado da operação é impresso, indicando sucesso ou falha.
    
    @note Esta função utiliza a função `insertGrocery` do módulo `pantrydb_queries` para inserir os itens na lista de compras.
    """
    for name in grocery_items:
        message = pdb.insertGrocery(name)
        print(message)  # This will print the outcome of each insert operation


# Call the function to populate the database
populate_pantry()
populate_shopping_list()
