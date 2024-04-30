"""
@brief Módulo de interação com a base de dados de receitas.

Este módulo oferece várias funções para aceder e manipular dados armazenados na base de dados de receitas.
As funções cobrem a procura de receitas, ingredientes, ferramentas usadas nas receitas e instruções de cozinha.

@details As funções utilizam a biblioteca `mysql.connector` para conectar-se e realizar consultas na base de dados.
Cada função é responsável por uma tarefa específica, como buscar receitas por nome ou tag, listar ingredientes de uma
receita, ou obter a próxima instrução de cozinha para uma receita.

<b>Dependencies:</b>
- mysql.connector
- random

<b>Usage:</b>
- As funções podem ser importadas e usadas em outros scripts para criar, acessar e manipular dados de receitas.
- O uso efetivo das funções requer uma base de dados MariaDB configurada conforme esperado pelo módulo.

@code
    import recipes_queries as rq
    recipe_id = rq.getRecipe('Pizza Margherita')
    ingredients = rq.getIngredients(recipe_id)
    print(ingredients)
@endcode

@note As funções assumem que a base de dados está corretamente configurada com as tabelas e conexões apropriadas.
Precisa de instalar a biblioteca `mysql.connector` para utilizar este módulo.
Para instalar, utilize um dos comandos a seguir dependendo do seu ambiente:
- pip install mysql-connector-python
- pip3 install mysql-connector-python
- conda install mysql-connector-python

"""
import mysql.connector
from mysql.connector import Error
import random

def create_connection():
    """ 
    @brief Estabelece conexão com a base de dados MariaDB.
    @details Esta função cria uma conexão com a base de dados MariaDB utilizando as credenciais fornecidas.
    
    @return Retorna a conexão se bem sucedida; None se houver erro.
    
    @note Esta função requer que o servidor MariaDB esteja em execução e acessível.
    
    @warning Esta conneção não é segura e deve ser usada apenas para fins de demonstração e testes.
    """
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="admin",
            password="admin",
            database="recipe_database"
        )
        return connection
    except Error as e:
        print(f"Erro ao conectar ao MariaDB: {e}")
        return None

# Returns a list of tuples with the name, number of servings and cooking time of all recipes
def getRecipes():
    """
    @brief Procura todas as receitas disponíveis.
    @details Esta função retorna uma lista de dicionários contendo o nome, número de porções e tempo de confeção de cada receita.
    
    
    @return Lista de dicionários contendo nome, número de porções e tempo de confeção de cada receita.
    """
    conn = create_connection()
    if conn is None:
        return []
    query = "SELECT name, number_of_servings, cooking_time FROM recipes"
    try:
        cursor = conn.cursor(dictionary=True)  # Ensure cursor returns dictionaries
        cursor.execute(query)
        recipes = cursor.fetchall()
        # No need for further formatting here, as each row is already a dictionary
        return recipes
    except Error as e:
        print(f"Error: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

# Returns the recipe_id of a recipe given its tag
def getRecipeByTag(tag):
    """
    @brief Procura IDs de receitas associadas a uma tag específica.
    @details Esta função procura IDs de receitas associadas a uma tag específica na base de dados.
    
    @param tag Nome da tag a ser procurada.
    
    @return <list> Lista de IDs de receitas
    
    @note Se a tag não for encontrada, a função retornará None.
    """
    # Obtém IDs de receitas pelo nome da tag.
    conn = create_connection()
    if conn is None:
        return None
    query = """
    SELECT r.recipe_id
    FROM recipes AS r
    JOIN recipe_tags AS rt ON r.recipe_id = rt.recipe_id
    JOIN tags AS t ON rt.tag_id = t.tag_id
    WHERE t.name = %s
    """
    try:
        cursor = conn.cursor()
        cursor.execute(query, (tag,))
        recipe_ids = cursor.fetchall()  # Isso retornará uma lista de tuplas, cada uma contendo apenas o recipe_id
        return [recipe_id[0] for recipe_id in recipe_ids] if recipe_ids else None
    except Error as e:
        print(f"Erro: {e}")
        return None
    finally:
        cursor.close()
        conn.close()

# Returns the recipe_id of a recipe given its name
def getRecipe(name):
    """
    @brief Procura o ID de uma receita pelo seu nome.
    @details Esta função procura o ID de uma receita pelo seu nome na base de dados.
    
    @param name Nome da receita a ser procurada.
    
    @return ID da receita se encontrada
    
    @note Se a receita não for encontrada, a função retornará None.
    """
    conn = create_connection()
    if conn is None:
        return None
    query = "SELECT recipe_id FROM recipes WHERE name = %s"
    try:
        cursor = conn.cursor()
        cursor.execute(query, (name,))
        recipe_id = cursor.fetchone()
        return recipe_id[0] if recipe_id else None
    except Error as e:
        print(f"Erro: {e}")
        return None
    finally:
        cursor.close()
        conn.close()

# Returns a list of tuples with the name, quantity and unit of all ingredients of a recipe
def getIngredients(recipe_id):
    """
    @brief Procura os ingredientes de uma receita.
    @details Esta função procura os ingredientes de uma receita pelo seu ID na base de dados.
    
    @param recipe_id ID da receita.
    
    @return Lista de ingredientes com nome, quantidade e unidade; lista vazia em caso de erro.
    """

    conn = create_connection()
    if conn is None:
        return []
    query = "SELECT name, quantity, unit FROM recipe_ingredients WHERE recipe_id = %s"
    try:
        cursor = conn.cursor(dictionary=True)  # Adjust based on your DB connector's syntax
        cursor.execute(query, (recipe_id,))
        ingredients = cursor.fetchall()
        return ingredients
    except Error as e:
        print(f"Error: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

# Returns a list of tuples with the name of all tools used in a recipe
def getTools(recipe_id):
    """
    @brief Procura os ingredientes de uma receita.
    @details Esta função procura os utensílios usados em uma receita pelo seu ID na base de dados.
    
    @param recipe_id ID da receita.
    
    @return Lista de ingredientes com nome, quantidade e unidade; lista vazia em caso de erro.
    """

    conn = create_connection()
    if conn is None:
        return []
    query = """
    SELECT DISTINCT t.name FROM tools t
    JOIN instructions_tools it ON t.tool_id = it.tool_id
    JOIN recipe_instructions ri ON it.recipe_instruction_id = ri.recipe_instruction_id
    WHERE ri.recipe_id = %s
    """
    try:
        cursor = conn.cursor()
        cursor.execute(query, (recipe_id,))
        tools = cursor.fetchall()
        return tools
    except Error as e:
        print(f"Erro: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

# Returns a list of tuples with the description of all instructions of a recipe
def getRandomRecipe():
    """
    @brief Escolhe aleatoriamente uma receita da base de dados.
    @details Escolhe aleatoriamente uma receita da base de dados e retorna seu ID.
    
    @return ID de uma receita escolhida aleatoriamente; None em caso de erro.
    """
    conn = create_connection()
    if conn is None:
        return None
    query = "SELECT recipe_id FROM recipes"
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        recipes = cursor.fetchall()
        random_recipe_id = random.choice(recipes)[0]
        return random_recipe_id
    except Error as e:
        print(f"Erro: {e}")
        return None
    finally:
        cursor.close()
        conn.close()

# Returns the name of a recipe given its recipe_id
def getRecipeName(recipe_id):
    """
    @brief Procura o nome de uma receita pelo seu ID.
    @details Esta função procura o nome de uma receita pelo seu ID na base de dados.
    
    @param recipe_id ID da receita.
    
    @return Nome da receita se encontrada; None caso contrário.
    """
    conn = create_connection()
    if conn is None:
        return None
    query = "SELECT name FROM recipes WHERE recipe_id = %s"
    try:
        cursor = conn.cursor()
        cursor.execute(query, (recipe_id,))
        recipe_name = cursor.fetchone()
        return recipe_name[0] if recipe_name else None
    except Error as e:
        print(f"Erro: {e}")
        return None
    finally:
        cursor.close()
        conn.close()

# Returns a list with the description of the next instruction of a recipe
def getNextInstruction(recipe_id, step):
    """
    @brief Procura a próxima instrução.
    @details Procura a descrição da próxima instrução de cozinha para uma receita e passo dados.
    
    @param recipe_id ID da receita.
    @param step Número do passo atual.
    
    @return Descrição da próxima instrução; None se não encontrada ou primeiro passo.
    """
    #Obtém a descrição do próximo passo para um recipe_id e step dado
    conn = create_connection()
    query = """
    SELECT description FROM recipe_instructions
    WHERE recipe_id = %s AND step_number = %s
    """
    next_step = step + 1
    try:
        cursor = conn.cursor()
        cursor.execute(query, (recipe_id, next_step))
        instruction = cursor.fetchone()
        return instruction[0] if instruction else None
    except Error as e:
        print(f"Erro: {e}")
        return None
    finally:
        cursor.close()
        conn.close()

# Returns a list with the description of the previous instruction of a recipe
def getPreviousInstruction(recipe_id, step):
    """
    @brief Procura a instrução anterior.
    @details Procura a descrição da instrução anterior de uma receita dado o seu ID e o número do passo.
    
    @param recipe_id ID da receita.
    @param step Número do passo atual.
    
    @return Descrição da instrução anterior; None se não encontrada ou primeiro passo.
    """

    #btém a descrição do passo anterior para um recipe_id e step dado.
    conn = create_connection()
    if step == 1:  # Não existe instrução anterior ao primeiro passo
        return None
    previous_step = step - 1
    query = """
    SELECT description FROM recipe_instructions
    WHERE recipe_id = %s AND step_number = %s
    """
    try:
        cursor = conn.cursor()
        cursor.execute(query, (recipe_id, previous_step))
        instruction = cursor.fetchone()
        return instruction[0] if instruction else None
    except Error as e:
        print(f"Erro: {e}")
        return None
    finally:
        cursor.close()
        conn.close()
        
# Returns a list with the actual instruction of a recipe
def getActualInstruction(recipe_id, step):
    """
    @brief Procura a instrução atual.
    @details Obtém a descrição da instrução atual de uma receita dado o seu ID e o número do passo.
    
    @param recipe_id ID da receita.
    @param step Número do passo atual.
    
    @return Descrição da instrução atual; None se não encontrada ou passo zero.
    """
    #Obtém a descrição do passo anterior para um recipe_id e step dado.
    conn = create_connection()
    if step == 0:  # Não existe instrução anterior ao primeiro passo
        return None
    query = """
    SELECT description FROM recipe_instructions
    WHERE recipe_id = %s AND step_number = %s
    """
    try:
        cursor = conn.cursor()
        cursor.execute(query, (recipe_id, step))
        instruction = cursor.fetchone()
        return instruction[0] if instruction else None
    except Error as e:
        print(f"Erro: {e}")
        return None
    finally:
        cursor.close()
        conn.close()

def getImg_url(recipe_id):
    """
    @brief Procura a URL da imagem de uma receita.
    @details Procura a URL da imagem de uma receita pelo seu ID.
    
    @param recipe_id ID da receita.
    
    @return URL da imagem se encontrada; None caso contrário.
    """
    conn = create_connection()
    if conn is None:
        return None
    query = "SELECT image_url FROM recipe_images WHERE recipe_id = %s"
    try:
        cursor = conn.cursor()
        cursor.execute(query, (recipe_id,))
        img_url = cursor.fetchone()
        return img_url[0] if img_url else None
    except Error as e:
        print(f"Erro: {e}")
        return None
    finally:
        cursor.close()
        conn.close()
        
# Exemplo de como utilizar as funções modificadas
# recipes = getRecipes()
# print("Receitas:", recipes)
# print("\n")
# recipe_id = getRecipe("Arroz de Pato")

# ingredients = getIngredients(recipe_id)
# print("Ingredientes:", ingredients)
# print("\n")
# tools = getTools(recipe_id)
# print("Utensílios:", tools)
# print("\n")

# numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8]

# print("TESTING getNextInstruction")
# for step in numbers: 
#     step_description = getNextInstruction(recipe_id, step)
#     real_step = step + 1
#     if step_description is None:
#         continue
#     print(f"Passo atual {step} e o  PROXIMO PASSO {(real_step)}: {step_description}")
# print("\n")
# print("TESTING getPreviousInstruction")
# for step in reversed(numbers): 
#     step_description = getPreviousInstruction(recipe_id, step)
#     real_step = step - 1
#     if step_description is None:
#         continue
#     print(f"Passo atual {step} e o PASSO ANTERIOR {(real_step)}: {step_description}")
# print("\n")


#random_recipe_id = getRandomRecipe()
#random_recipe_name = getRecipeName(random_recipe_id)
#print("Receita aleatória:", random_recipe_name)
#print("\n")
#random_recipe_img_url = getImg_url(random_recipe_id)
#print("Imagem:", random_recipe_img_url)
#print("\n")
# random_recipe_ingredients = getIngredients(random_recipe_id)
# print("Ingredientes:", random_recipe_ingredients)
# print("\n")
# random_recipe_tools = getTools(random_recipe_id)
# print("Utensílios:", random_recipe_tools)
# print("\n")

# print("TESTING getRecipeByTag")
# #print(getRecipeByTag("Salmão"))
# #print(getRecipeName(getRecipeByTag("Salmão")[0]))