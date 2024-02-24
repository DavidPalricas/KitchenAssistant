# FICHEIRO PARA INSERIR DADOS NA BASE DE DADOS

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

    
def insertRecipe(recipeID,name):
    conn, cursor = connectDatabase()
    if conn is not None and cursor is not None:
        try:
            cursor.execute("INSERT INTO recipe (recipe_id, name, source_url) VALUES (%s, %s)", (recipeID, name, "https://api.spoonacular.com"))
            conn.commit()
            print("Recipe inserted")
        except Error as e:
            print(e)
            print("Failed to insert recipe")
        finally:
            cursor.close()
            conn.close()
            print("Connection closed")
    else:
        print("Failed to insert recipe")      
        
def insertCategories():
    conn, cursor = connectDatabase()
    categories = ["maincourse", "dessert", "appetizer"]
    if conn is not None and cursor is not None:
        try:
            for category in categories:
                cursor.execute("INSERT INTO categories (name) VALUES (%s)", (category,))
            conn.commit()
            print("Categories inserted")
        except Error as e:
            print(e)
            print("Failed to insert categories")
        finally:
            cursor.close()
            conn.close()
            print("Connection closed")
    else:
        print("Failed to insert categories")

def insertRecipeImage(recipeID):
    conn, cursor = connectDatabase()
    imageURL = data.recipeImage(recipeID)
    sourceURL = "https://api.spoonacular.com"
    if conn is not None and cursor is not None:
        try:
            cursor.execute("INSERT INTO recipe_image (recipe_id, image_url, source_url) VALUES (%s, %s, %s)", (recipeID, imageURL, sourceURL))
            conn.commit()
            print("Recipe image inserted")
        except Error as e:
            print(e)
            print("Failed to insert recipe image")
        finally:
            cursor.close()
            conn.close()
            print("Connection closed")
    else:
        print("Failed to insert recipe image")
        
def insertTools(recipeID):
    conn, cursor = connectDatabase()
    tools = data.recipeTools(recipeID)
    sourceURL = "https://api.spoonacular.com"
    if conn is not None and cursor is not None:
        try:
            for tool in tools:
                cursor.execute("INSERT INTO tool (name,source_url) VALUES (%s, %s)", (tool, sourceURL))
            conn.commit()
            print("Tools inserted")
        except Error as e:
            print(e)
            print("Failed to insert tools")
        finally:
            cursor.close()
            conn.close()
            print("Connection closed")
    else:
        print("Failed to insert tools")
        
dataTest = data.randomRecipes(1,"main course")
recipeID = dataTest[0][0]
print(recipeID)
name = dataTest[0][1]
print(name)

insertCategories()
#insertRecipe(recipeID, name)
