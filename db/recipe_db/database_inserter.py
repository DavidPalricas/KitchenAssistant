# FICHEIRO PARA INSERIR DADOS NA BASE DE DADOS

import re
import mysql.connector
from mysql.connector import Error
# conda install mysql-connector-python
# pip install mysql-connector-python

import translators as ts
import translateData as data

# Connect to database
def connectDatabase():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='admin',
            password='admin',
            database='recipe_database'
        )
        if conn.is_connected():
            print("Connected to database")
            cursor = conn.cursor()
            return conn, cursor
    except Error as e:
        print(e)
        print("Failed to connect to database")
        return None, None

def insertRecipe(name):
    conn, cursor = connectDatabase()
    if conn is not None and cursor is not None:
        try:
            # Verificar se a receita já existe
            cursor.execute("SELECT recipe_id FROM recipes WHERE name = %s", (name,))
            existing_recipe = cursor.fetchone()
            
            if existing_recipe:
                recipeID = existing_recipe[0]
                print(f"Receita com o nome '{name}' já existe.")
            else:
                
                cursor.execute("INSERT INTO recipes (name, source_url) VALUES (%s, %s)", (name, "https://api.spoonacular.com"))
                recipeID = cursor.lastrowid # get the last inserted id
                conn.commit()
                cook_time = data.recipeTime(recipeID)
                servings = data.recipeServings(recipeID)
                health_score = data.recipeHealthScore(recipeID)
                cursor.execute("UPDATE recipes SET number_of_servings = %s, cooking_time = %s, health_score = %s WHERE recipe_id = %s", (servings, cook_time, health_score, recipeID))
                conn.commit()
                print(f"Recipe '{name}'inserted with number of servings: {servings}, cooking time: {cook_time} and health score: {health_score} ---------- D O N E")
                print("\n")
                
            # insert tags deveria ser feito fora desta função porque elas tem de ser inicialializadas automaticamente
            tags = data.categories(recipeID)
            insertTags(tags)
            
            # Associate recipe with tags
            #tags = data.categories(recipeID)
            tags_id = getTagIdsByName(tags)
            for tag in tags_id:
                associateRecipeTags(recipeID, tag)
            
            # insert on recipe_images
            insertRecipeImage(recipeID)
            
            # insert on recepi_ingredients
            ingredients = data.recipeIngredients(recipeID)
            insertRecipeIngredients(recipeID, ingredients)

            # insert on tools
            insertTools(recipeID)
            
            # insert instructions [and associate(instructions, tools)]
            instructions = data.recipeSteps(recipeID)
            print("INSERT RECIPE - Instructions: ",instructions)
            insertRecipeInstructions(recipeID, instructions)
        
        except Error as e:
            print(e)
            print("Failed to insert recipe")
        finally:
            cursor.close()
            conn.close()
            print("Connection closed")
    else:
        print("Failed to insert recipe")      

def associateRecipeTags(recipeID, tagID):
    conn, cursor = connectDatabase()
    if conn is not None and cursor is not None:
        try:
            cursor.execute("INSERT INTO recipe_tags (recipe_id, tag_id) VALUES (%s, %s)", (recipeID, tagID))
            conn.commit()
            print(f"(Recipe '{recipeID}', tag '{tagID}') Association inserted ----------------- D O N E")
            print("\n")
        except Error as e:
            print(e)
            print("Failed to insert recipe tags")
        finally:
            cursor.close()
            conn.close()
            print("Connection closed")
    else:
        print("Failed to insert recipe tags")
        
def insertTags(tags):
    conn, cursor = connectDatabase()
    #categories = data.recipeCategory() # get categories
    if conn is not None and cursor is not None:
        try:
            for category in tags:
                # Verificar se a tag já existe
                cursor.execute("SELECT name FROM tags WHERE name = %s", (category,))
                result = cursor.fetchone()
                if not result:
                    # Somente insere se a tag não existir
                    cursor.execute("INSERT INTO tags (name) VALUES (%s)", (category,))
                    print(f"Tag '{category}' inserted")
                    conn.commit()
            print("Tags inserted ----------------- D O N E")
            print("\n")
        except Error as e:
            print(e)
            print("Failed to insert categories")
        finally:
            cursor.close()
            conn.close()
            print("Connection closed")
    else:
        print("Failed to insert categories")

def getTagIdsByName(tags):
    conn, cursor = connectDatabase()
    tags_id = []
    if conn is not None and cursor is not None:
        try:
            for tag in tags:
                cursor.execute("SELECT tag_id FROM tags WHERE name = %s", (tag,))
                result = cursor.fetchone()
                if result:
                    tags_id.append(result[0])
        except Error as e:
            print(e)
            print("Failed to fetch tag ids")
        finally:
            cursor.close()
            conn.close()
            print("Connection closed")
    return tags_id

def insertRecipeImage(recipeID):
    conn, cursor = connectDatabase()
    imageURL = data.recipeImage(recipeID)
    sourceURL = "https://api.spoonacular.com"
    if conn is not None and cursor is not None:
        try:
            # Verificar se a imagem já existe para esta receita
            cursor.execute("SELECT image_id FROM recipe_images WHERE recipe_id = %s AND image_url = %s", (recipeID, imageURL))
            existing_image = cursor.fetchone()

            if existing_image:
                print("Imagem já associada à receita.")
            else:
                # A imagem não existe, insira-a
                cursor.execute("INSERT INTO recipe_images (recipe_id, image_url, source_url) VALUES (%s, %s, %s)", (recipeID, imageURL, sourceURL))
                conn.commit()
                print("Recipe image inserted ----------------- D O N E")
                print("\n")

        except Error as e:
            print(e)
            print("Failed to insert recipe image")
        finally:
            cursor.close()
            conn.close()
            print("Connection closed")
    else:
        print("Failed to insert recipe image")

def insertRecipeIngredients(recipeID, ingredients):
    conn, cursor = connectDatabase()
    sourceURL = "https://api.nutriscore.com"
    nutri_score = "A"  # for testing purposes
    if conn is not None and cursor is not None:
        try:
            for name, quantity_unit in ingredients.items(): 
                # Usar expressão regular para separar quantidade da unidade
                match = re.match(r"([0-9,.]+)\s*(.*)", quantity_unit)
                if match:
                    quantity, unit = match.groups()
                    quantity = quantity.replace(',', '.')  # Converter vírgula em ponto para padronizar o formato decimal
                    cursor.execute("INSERT INTO recipe_ingredients (recipe_id, name, quantity, unit, nutri_score_value, source_url) VALUES (%s, %s, %s, %s, %s, %s)", 
                                   (recipeID, name, quantity, unit, nutri_score, sourceURL))
                    print(f"Ingredient '{name}' inserted with quantity: {quantity} and unit: {unit}")
                else:
                    print(f"Não foi possível processar o ingrediente: {name} com quantidade e unidade: {quantity_unit}")
            conn.commit()
            print("Ingredients inserted ----------------- D O N E")
            print("\n")
        except Error as e:
            print(e)
            print("Failed to insert ingredients")
        finally:
            cursor.close()
            conn.close()
            print("Connection closed")
    else:
        print("Failed to insert ingredients")
        
def insertRecipeInstructions(recipeID, instructions):
    conn, cursor = connectDatabase()
    time = 0  # for testing purposes
    if conn is not None and cursor is not None:
        try:
            for step, data in instructions.items():
                # Verificar se a instrução já existe para esta receita e passo
                cursor.execute("SELECT recipe_instruction_id FROM recipe_instructions WHERE recipe_id = %s AND step_number = %s", (recipeID, step))
                existing_instruction = cursor.fetchone()
                
                if not existing_instruction:
                    # Instrução não existe, inserir nova instrução
                    cursor.execute("INSERT INTO recipe_instructions (recipe_id, step_number, description, time) VALUES (%s, %s, %s, %s)", 
                                   (recipeID, step, data['description'], time))
                    conn.commit()
                    print(f"Instruction '{data['description']}' inserted for step {step}")
                    instructions_id = cursor.lastrowid
                else:
                    # Instrução já existe, você pode escolher atualizar ou simplesmente ignorar
                    instructions_id = existing_instruction[0]
                    print("Instruction already exists. ID:", instructions_id)
                
                # Associar ferramentas à instrução (assumindo que getToolsIdsByName e associateRecipeTools estão corretamente implementadas)
                for tool_name in data['tools']:
                    tool_id = getToolsIdsByName(tool_name)
                    if tool_id:
                        associateRecipeTools(instructions_id, tool_id)
                
            print("Recipe Instructions inserted")
            print("--------------------------------- DONE")
        except Error as e:
            print(e)
            print("Failed to process instructions")
            conn.rollback()
        finally:
            cursor.close()
            conn.close()
            print("Connection closed")
    else:
        print("Failed to process instructions")

def associateRecipeTools(recipe_instruction_ID, toolID):
    conn, cursor = connectDatabase()
    if conn is not None and cursor is not None:
        try:
            cursor.execute("INSERT INTO instructions_tools (recipe_instruction_id, tool_id) VALUES (%s, %s)", (recipe_instruction_ID, toolID))
            conn.commit()
            print(f"(Instruction '{recipe_instruction_ID}', tool '{toolID}') Association inserted ----------------- D O N E")
            print("\n")
        except Error as e:
            print(e)
            print("Failed to insert recipe tools")
        finally:
            cursor.close()
            conn.close()
            print("Connection closed")
    else:
        print("Failed to insert recipe tools")

def getToolsIdsByName(tool_name):
    conn, cursor = connectDatabase()
    #tools_id = []
    if conn is not None and cursor is not None:
        try:
            cursor.execute("SELECT tool_id FROM tools WHERE name = %s", (tool_name,))
            result = cursor.fetchone()
            if result:
                return (result[0])
        except Error as e:
            print(e)
            print("Failed to fetch tool ids")
        finally:
            cursor.close()
            conn.close()
            print("Connection closed")
    return None
    
def insertTools(recipeID):
    conn, cursor = connectDatabase()
    tools = data.recipeTools(recipeID)
    print("INSERT_TOOLS - Tools: ",tools)
    sourceURL = "https://api.spoonacular.com"
    if conn is not None and cursor is not None:
        try:
            for tool in tools:
                # Verificar se a ferramenta já existe
                cursor.execute("SELECT * FROM tools WHERE name = %s", (tool,))
                result = cursor.fetchone()
                # Se a ferramenta não existir, inserir
                if result is None:
                    cursor.execute("INSERT INTO tools (name,source_url) VALUES (%s, %s)", (tool, sourceURL))
                    conn.commit()
                    print(f"Tool '{tool}' inserted")
            print("Tools inserted ----------------- D O N E")
            print("\n")
        except Error as e:
            print(e)
            print("Failed to insert tools")
        finally:
            cursor.close()
            conn.close()
            print("Connection closed")
    else:
        print("Failed to insert tools")
        
dataTest = data.randomRecipes(2,"main course")
#print("DataTest: ",dataTest)

for key,value in dataTest:
    recipeID = key
    name = value
    print("Inserting recipe",name," into database: [ID ", recipeID, "]")
    #for key,value in data.recipeSteps(recipeID).items():
    #    print("Step: ",key," - ",value)
    print("Recipe",name," inserted into database ------------------------------------------")
    print("\n")
    insertRecipe(name)
    print("Recipe inserted")

#recipeID = dataTest[0][0]
#print(recipeID)
#name = dataTest[0][1]
#print(name)
#print("Inserting recipe into database")
#insertRecipe(name)
#print("Recipe inserted")
#print("---------------------------------")
#print("Inserting tags into database")
#insertTags()
#print("Tags inserted")


#insertCategories()
#insertRecipeImage(recipeID)
#insertTools(recipeID)
#insertRecipe(recipeID, name)
