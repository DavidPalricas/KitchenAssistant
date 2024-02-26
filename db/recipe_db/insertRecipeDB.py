
import mysql.connector
from mysql.connector import Error
from getData import GetData
import translators as ts
import re

# conda install mysql-connector-python
# pip install mysql-connector-python

class InsertRecipeDB:
    def __init__(self, recipe):
        self.name = recipe['NAME']
        #print("NAME",self.name)
        self.ingredients = recipe['INGREDIENTS']
        #print("INGREDIENTS",self.ingredients)
        self.tools = recipe['TOOLS']
        #print("TOOLS",self.tools)
        self.instructions = recipe['INSTRUCTIONS']
        #print("INSTRUCTIONS",self.instructions)
        self.cook_time = recipe['COOKING_TIME']
        #print("COOKING_TIME",self.cook_time)
        self.servings = recipe['NUMBER_OF_SERVINGS']
        #print("NUMBER_OF_SERVINGS",self.servings)
        self.img_url = recipe['IMAGE_URL']
        if isinstance(self.img_url, tuple):
            self.img_url = self.img_url[0]
        #print("IMAGE_URL",self.img_url)
        self.tags = recipe['TAGS']
        #print("TAGS",self.tags)
        #print("\n")
        self.data = GetData()
    
    def connectDatabase(self):
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
    
    def insertRecipe(self):
        conn, cursor = self.connectDatabase()
        if conn is not None and cursor is not None:
            try:
                # Verificar se a receita já existe
                cursor.execute("SELECT recipe_id FROM recipes WHERE name = %s", (self.name,))
                existing_recipe = cursor.fetchone()
                
                if existing_recipe:
                    recipeID = existing_recipe
                    print(f"Recipe '{self.name}' already exits.")
                else:
                    
                    cursor.execute("INSERT INTO recipes (name, number_of_servings, cooking_time, source_url) VALUES (%s, %s, %s, %s)", (self.name, self.servings, self.cook_time, "https://www.saborintenso.com/"))
                    recipeID = cursor.lastrowid # get the last inserted id
                    conn.commit()
                    print(f"Recipe '{self.name}' inserted sucefully.")
                
                # insert tags
                self.insertTags()
                
                # Associate recipe with tags
                #tags = data.categories(recipeID)
                tags_id = self.getTagIdsByName()
                for tag in tags_id:
                    self.associateRecipeTags(recipeID, tag)
                
                # insert on recipe_images
                self.insertRecipeImage(recipeID)
                
                # insert on recepi_ingredients
                self.insertRecipeIngredients(recipeID)

                # insert on tools
                self.insertTools(recipeID)
                
                # insert instructions [and associate(instructions, tools)]
                self.insertRecipeInstructions(recipeID)
            
            except Error as e:
                print(e)
                print("Failed to insert recipe")
            finally:
                cursor.close()
                conn.close()
                print("Connection closed")
        else:
            print("Failed to insert recipe")      
    
    def insertTags(self):
        conn, cursor = self.connectDatabase()
        #categories = data.recipeCategory() # get categories
        if conn is not None and cursor is not None:
            try:
                for tag in self.tags:
                    # Verificar se a tag já existe
                    cursor.execute("SELECT name FROM tags WHERE name = %s", (tag,))
                    result = cursor.fetchone()
                    if not result:
                        # Somente insere se a tag não existir
                        cursor.execute("INSERT INTO tags (name) VALUES (%s)", (tag,))
                        print(f"Tag '{tag}' inserted")
                        conn.commit()
                print("Tags inserted ----------------- D O N E")
                print("\n")
            except Error as e:
                print(e)
                print("Failed to insert tags")
            finally:
                cursor.close()
                conn.close()
                print("Connection closed")
        else:
            print("Failed to insert tags")
            
    def getTagIdsByName(self):
        conn, cursor = self.connectDatabase()
        tags_id = []
        if conn is not None and cursor is not None:
            try:
                for tag in self.tags:
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
    
    def associateRecipeTags(self, recipeID, tagID):
        conn, cursor = self.connectDatabase()
        if conn is not None and cursor is not None:
            try:
                cursor.execute("INSERT INTO recipe_tags (recipe_id, tag_id) VALUES (%s, %s)", (recipeID, tagID,))
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
    
    def insertRecipeImage(self, recipeID):
        conn, cursor = self.connectDatabase()
        sourceURL = "https://www.saborintenso.com/"
        if conn is not None and cursor is not None:
            try:
                # Verificar se a imagem já existe para esta receita
                cursor.execute("SELECT image_id FROM recipe_images WHERE recipe_id = %s AND image_url = %s", (recipeID, self.img_url,))
                existing_image = cursor.fetchone()

                if existing_image:
                    #recipeID = existing_image[0]
                    print(f"Recipe {recipeID} already have an image associated.")
                else:
                    # A imagem não existe, insira-a
                    cursor.execute("INSERT INTO recipe_images (recipe_id, image_url, source_url) VALUES (%s, %s, %s)", (recipeID, self.img_url, sourceURL))
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
            
    def insertRecipeIngredients(self, recipeID):
        conn, cursor = self.connectDatabase()
        sourceURL = "https://api.spoonacular.com"
        
        if conn is not None and cursor is not None:
            try:
                for name, quantity_unit in self.ingredients.items(): 
                    en_name = ts.translate_text(name, "bing", "pt", "en")
                    tmp_calories = self.data.get_calories_by_ingredient_name(en_name)
                    if 'Calories' in tmp_calories:
                        calories_str = tmp_calories['Calories']
                        # Extract numeric value from calories_str as before
                        numbers = re.findall(r"[\d.]+", calories_str)
                        calories = float(''.join(numbers)) if numbers else 0
                    else:
                        calories = 0
                    quantity, unit = quantity_unit.split()
                    #print("QUANTITY",quantity)
                    #print("UNIT",unit)
                    #quantity = quantity.replace(',', '.')  # Converter vírgula em ponto para padronizar o formato decimal
                    cursor.execute("INSERT INTO recipe_ingredients (recipe_id, name, quantity, unit, calories, source_url) VALUES (%s, %s, %s, %s, %s, %s)", 
                                (recipeID, name, quantity, unit, calories, sourceURL))
                    print(f"Ingredient '{name}' inserted with quantity: {quantity} and unit: {unit}")
                    conn.commit()
                    #else:
                    #    print(f"Failed to insert ingredient: {name} ")
                #conn.commit()
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
            
    def insertTools(self, recipeID):
        conn, cursor = self.connectDatabase()
        sourceURL = "https://www.saborintenso.com/"
        if conn is not None and cursor is not None:
            try:
                for tool in self.tools:
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
            
    def insertRecipeInstructions(self, recipeID):
        conn, cursor = self.connectDatabase()
        if conn is not None and cursor is not None:
            try:
                for step, data in self.instructions.items():
                    # Verificar se a instrução já existe para esta receita e passo
                    cursor.execute("SELECT recipe_instruction_id FROM recipe_instructions WHERE recipe_id = %s AND step_number = %s", (recipeID, step))
                    existing_instruction = cursor.fetchone()
                    
                    if not existing_instruction:
                        # Instrução não existe, inserir nova instrução
                        cursor.execute("INSERT INTO recipe_instructions (recipe_id, step_number, description) VALUES (%s, %s, %s)", 
                                    (recipeID, step, data['description']))
                        conn.commit()
                        print(f"Instruction '{data['description']}' inserted for step {step}")
                        instructions_id = cursor.lastrowid
                    else:
                        # Instrução já existe, você pode escolher atualizar ou simplesmente ignorar
                        instructions_id = existing_instruction[0]
                        print("Instruction already exists. ID:", instructions_id)
                    
                    # Associar ferramentas à instrução (assumindo que getToolsIdsByName e associateRecipeTools estão corretamente implementadas)
                    for tool_name in data['tools']:
                        tool_id = self.getToolsIdsByName(tool_name)
                        if tool_id:
                            self.associateRecipeTools(instructions_id, tool_id)
                    
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
            
    def getToolsIdsByName(self, tool_name):
        conn, cursor = self.connectDatabase()
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
    
    def associateRecipeTools(self, recipe_instruction_ID, toolID):
        conn, cursor = self.connectDatabase()
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
            
            
from read_recipe import read_recipe_from_txt
     
            
if __name__ == "__main__":
    
    #    
    file_path = 'recipes/Pica-Pau de Entremeada.txt'
    recipe_data = read_recipe_from_txt(file_path)
    
    insertVector = InsertRecipeDB(recipe_data)
    insertVector.insertRecipe()
    #print(f"Recipe {insertVector.name} inserted successfully")

    #
    file_path = 'recipes/Amêijoas à Bulhão Pato.txt'
    recipe_data = read_recipe_from_txt(file_path)
    
    insertVector = InsertRecipeDB(recipe_data)
    insertVector.insertRecipe()
    #print(f"Recipe {insertVector.name} inserted successfully")
    
    #
    file_path = 'recipes/Cogumelos Recheados com Alheira.txt'
    recipe_data = read_recipe_from_txt(file_path)
    
    insertVector = InsertRecipeDB(recipe_data)
    insertVector.insertRecipe()
    #print(f"Recipe {insertVector.name} inserted successfully")
    
    #
    file_path = 'recipes/Gambas ao alho.txt'
    recipe_data = read_recipe_from_txt(file_path)
    
    insertVector = InsertRecipeDB(recipe_data)
    insertVector.insertRecipe()
    #print(f"Recipe {insertVector.name} inserted successfully")
    
    
    #
    #file_path = 'recipes/Pica-Pau de Entremeada.txt'
    #recipe_data = read_recipe_from_txt(file_path)
    
    #insertVector = InsertRecipeDB(recipe_data)
    #insertVector.insertRecipe()
    #print(f"Recipe {insertVector.name} inserted successfully")