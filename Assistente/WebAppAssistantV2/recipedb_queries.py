import mysql.connector
from mysql.connector import Error
import random

def create_connection():
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
    conn = create_connection()
    if conn is None:
        return []
    query = "SELECT name, number_of_servings, cooking_time FROM recipes"
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        recipes = cursor.fetchall()
        return recipes
    except Error as e:
        print(f"Erro: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

# Returns the recipe_id of a recipe given its tag
def getRecipeByTag(tag):
    """Obtém IDs de receitas pelo nome da tag."""
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
    conn = create_connection()
    if conn is None:
        return []
    query = "SELECT name, quantity, unit FROM recipe_ingredients WHERE recipe_id = %s"
    try:
        cursor = conn.cursor()
        cursor.execute(query, (recipe_id,))
        ingredients = cursor.fetchall()
        return ingredients
    except Error as e:
        print(f"Erro: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

# Returns a list of tuples with the name of all tools used in a recipe
def getTools(recipe_id):
    conn = create_connection()
    if conn is None:
        return []
    query = """
    SELECT t.name FROM tools t
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

# Returns a list of tuples with the description of all instructions of a recipe
def getNextInstruction(recipe_id, step):
    """Obtém a descrição do próximo passo para um recipe_id e step dado."""
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

# Returns a list of tuples with the description of all instructions of a recipe
def getPreviousInstruction(recipe_id, step):
    """Obtém a descrição do passo anterior para um recipe_id e step dado."""
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


# random_recipe_id = getRandomRecipe()
# random_recipe_name = getRecipeName(random_recipe_id)
# print("Receita aleatória:", random_recipe_name)
# print("\n")
# random_recipe_ingredients = getIngredients(random_recipe_id)
# print("Ingredientes:", random_recipe_ingredients)
# print("\n")
# random_recipe_tools = getTools(random_recipe_id)
# print("Utensílios:", random_recipe_tools)
# print("\n")

# print("TESTING getRecipeByTag")
# #print(getRecipeByTag("Salmão"))
# #print(getRecipeName(getRecipeByTag("Salmão")[0]))