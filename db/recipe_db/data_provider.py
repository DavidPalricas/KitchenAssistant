# FICHEIRO PARA IRBUSCAR OS DADOS AO getDATA.py e trata-los para inserir na base de dados

import translators as ts
# pt_randomRecipes = ts.translate_text(value, "google", "auto", "pt")
from getData import GetData

def categoryData():
    # INSERT INTO categories (name, description) VALUES
    # ('Sobremesas', 'Doces e deliciosos pratos para finalizar a refeição'),
    # dados = [
    #     {"name": "Produto 1", "description": 10.99},
    #     {"name": "Produto 1", "description": 10.99},
    #     {"name": "Produto 1", "description": 10.99},
    #     # Adicione mais itens conforme necessário
    # ]
    # return dados
    data = []
    name1 = ts.translate_text("main course", "google", "auto", "pt")
    name2 = ts.translate_text("dessert", "google", "auto", "pt")
    name3 = ts.translate_text("appetizer", "google", "auto", "pt")
    data = [name1, name2, name3]
    
    return data

def getAllData():
    # get all data on a single dictionary
    
    dataApi = GetData()
    numberOFrecipes = 10
    recipes = dataApi.getRandomRecipes(numberOFrecipes, "main course")    
    category_id = 1 # main course
    data = []
    
    for recipe in recipes:
        recipe_id = recipe[0] # id da receita
        recipe_name = ts.translate_text(recipe[1] , "google", "auto", "pt") # nome da receita traduzido
        recipe_description = ""
        number_of_servings = ""
        prep_time = ""
        cook_time = ""
        source_url = "www.spooacular.com"
        image_url = dataApi.getRecipeImage(recipe_id)
        tools = getTools(recipe_id)
        
        
        data = {
            "name": recipe_name,
            "category_id": category_id,
            "description": recipe_description, 
            "number_of_servings": number_of_servings, 
            "prep_time": prep_time, 
            "cook_time": cook_time,
            "source_url": source_url,
            "image_url": image_url,
            "tools": tools,
            "ingredients": ingridients
            }
    pass
    
def dados_tools():
    pass


name1 = ts.translate_text("main course", "google", "auto", "pt")
name2 = ts.translate_text("dessert", "google", "auto", "pt")
name3 = ts.translate_text("appetizer", "google", "auto", "pt")
names = [name1, name2, name3]
print(names)