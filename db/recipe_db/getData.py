import random
import requests

class GetData:
    def __init__(self):
        # Chave do 1
        #self.api_key = "ef6f2279b7864bad8ff9a04de2180657"
        # Chave do 2
        #self.api_key = "34af4d2879884e459a8b2e5bb71d410e"
        # Chave da 3
        #self.api_key = "d20575f54b404530829032207847afdb"
        # Chave do 4
        self.api_key = "2971e205092f42268a2a1ab1e372124b"
        # Chave do 5
        #self.api_key = "ac793bb9af8340debe7e6145de267050"
        # Chave do 6
        #self.api_key = "af1671b748fb4583b803624de57fea7b"

        self.base_url = "https://api.spoonacular.com"

    def convert_units(self, quantity, unit):
        # Converte unidades para o sistema métrico (kg, g, etc.) e atualiza o texto da unidade
        converted_quantity = quantity
        converted_unit = unit
        if unit.lower() in ["pounds", "pound"]:
            converted_quantity = quantity * 0.453592    # Converte pounds para kg
            converted_unit = "kg"
        elif unit.lower() in ["ounces", "ounce"]:
            converted_quantity = quantity * 28.3495     # Converte ounces para g
            converted_unit = "g"
        # Formata a quantidade para 3 casas decimais para legibilidade
        formatted_quantity = round(converted_quantity, 3)
        return formatted_quantity, converted_unit

    def getCategories(self,recipeId):
        # Retorna uma lista de categorias para uma receita
        query = f"{self.base_url}/recipes/{recipeId}/information?apiKey={self.api_key}"
        response = requests.get(query)
        data = response.json()
        return data.get('dishTypes', [])

    def getRecipeNameByTag(self, tag="main course"):
        # Retorna um nome de receita com base em uma tag (main course, dessert, appetizer)
        query = f"{self.base_url}/recipes/complexSearch?apiKey={self.api_key}&query={tag}&number=1"
        response = requests.get(query)
        data = response.json()
        if data['results']:
            return data['results'][0]['title']
        else:
            return None
        
    def getRecipe(self, tag="main course"):
        # Retorna um ID de receita com base em uma tag (main course, dessert, appetizer)
        query = f"{self.base_url}/recipes/complexSearch?apiKey={self.api_key}&query={tag}&number=1"
        response = requests.get(query)
        data = response.json()
        print(data)
        if data['results']:
            return data['results'][0]['id']
        else:
            return None

    # def getRandomRecipes(self, number="20"):
    #     offset = random.ranint(0, 900)
    #     query = f"{self.base_url}/recipes/random?apiKey={self.api_key}&number={number}&offset={offset}"
    #     response = requests.get(query)
    #     data = response.json()
        
    def getRandomRecipes(self, number="20", tag="main course"):
        # Retorna uma lista de receitas com base no número e tag fornecidos, com uma tag padrão de "main course"
        query = f"{self.base_url}/recipes/complexSearch?apiKey={self.api_key}&number={number}&type={tag}"
        response = requests.get(query)
        recipe_list = []
        if response.status_code == 200:
            data = response.json()
            recipes = data.get('results', [])
            for recipe in recipes:
                recipe_id = recipe.get('id')
                recipe_name = recipe.get('title')
                recipe_list.append((recipe_id, recipe_name))
            return recipe_list
        else:
            return "Failed to fetch recipes"
    
    def getRecipeName(self, recipeId):
        # Retorna o nome da receita com base no ID da receita fornecido
        query = f"{self.base_url}/recipes/{recipeId}/information?apiKey={self.api_key}"
        response = requests.get(query)
        if response.status_code == 200:
            data = response.json()
            return data.get('title', 'Name not specified')  # 'title' contains the recipe name
        else:
            return "Failed to fetch recipe name"
    
    def getRecipeImage(self, recipeId):
        # Retorna a URL da imagem de uma receita
        query = f"{self.base_url}/recipes/{recipeId}/information?apiKey={self.api_key}"
        response = requests.get(query)
        data = response.json()
        return data.get('image')

    def getRecipeIngredients(self, recipeId):
        # Retorna um dicionário de ingredientes e suas quantidades para uma receita
        query = f"{self.base_url}/recipes/{recipeId}/information?apiKey={self.api_key}"
        response = requests.get(query)
        data = response.json()
        ingredients_info = {}
        for ingredient in data.get('extendedIngredients', []):
            quantity, unit = self.convert_units(ingredient['amount'], ingredient['unit'])
            ingredients_info[ingredient['name']] = f"{quantity} {unit}"
        return ingredients_info

    def getRecipeTools(self, recipeId):
        # Retorna um dicionário de todas os utensilios necessárias para a receita
        query = f"{self.base_url}/recipes/{recipeId}/analyzedInstructions?apiKey={self.api_key}"
        response = requests.get(query)
        data = response.json()
        tools = set()
        if data:
            for instruction in data[0]['steps']:
                for equipment in instruction.get('equipment', []):
                    tools.add(equipment['name'])
        return {tool: None for tool in tools} 

    def getRecipeSteps(self, recipeId):
        # Retorna um dicionário com a descrição, utensilios e ingredientes de cada etapa da receita
        query = f"{self.base_url}/recipes/{recipeId}/analyzedInstructions?apiKey={self.api_key}"
        response = requests.get(query)
        data = response.json()
        steps_info = {}
        if data:
            for step in data[0]['steps']:
                step_num = step['number']
                ingredients = [ingredient['name'] for ingredient in step.get('ingredients', [])]
                equipments = [equipment['name'] for equipment in step.get('equipment', [])]
                steps_info[step_num] = {
                    'description': step['step'],
                    'ingredients': ingredients,
                    'tools': equipments
                }
        return steps_info

    def getRecipeServings(self, recipeId):
        # Retorna o número de porções que uma receita faz
        query = f"{self.base_url}/recipes/{recipeId}/information?apiKey={self.api_key}"
        response = requests.get(query)
        data = response.json()
        return data.get('servings', 'Not specified')
    
    def getRecipeTime(self, recipeId):
        # Retorna o tempo de preparação de uma receita
        query = f"{self.base_url}/recipes/{recipeId}/information?apiKey={self.api_key}"
        response = requests.get(query)
        data = response.json()
        return data.get('readyInMinutes', 'Not specified')

    def getRecipeHealthScore(self, recipeId):
        # Retorna a pontuação de saúde de uma receita
        query = f"{self.base_url}/recipes/{recipeId}/information?apiKey={self.api_key}"
        response = requests.get(query)
        data = response.json()
        return data.get('healthScore', 'Not specified')
    
    def getRecipeCard(self, recipeId, mask='potMask', backgroundImage='none', backgroundColor='ffffff', fontColor='333333'):
        # Construir a URL da consulta para gerar o cartão da receita
        query = f"{self.base_url}/recipes/{recipeId}/card?apiKey={self.api_key}&mask={mask}&backgroundImage={backgroundImage}&backgroundColor={backgroundColor}&fontColor={fontColor}"
        
        # Fazer a requisição GET ao endpoint para obter o cartão da receita
        response = requests.get(query)
        
        if response.status_code == 200:
            # Se a requisição for bem-sucedida, extrair a URL do cartão da receita da resposta
            data = response.json()
            return data.get('url', 'URL do cartão da receita não encontrada')
        else:
            # Se ocorrer um erro na requisição, retornar uma mensagem de erro
            return f"Erro ao obter o cartão da receita: {response.status_code}"


#
# GET INGRIDIENT FACTS
#
    def search_ingredient_by_name(self, name):
        """
        Searches for an ingredient by name and returns its ID.

        :param name: The name of the ingredient to search for.
        :return: The ID of the first matching ingredient or None if not found.
        """
        search_url = f"{self.base_url}/food/ingredients/search?apiKey={self.api_key}&query={name}"
        response = requests.get(search_url)
        if response.status_code == 200:
            results = response.json().get('results', [])
            if results:
                # Assuming you want the first result
                return results[0]['id']
        return None

    def get_ingredient_info_by_name(self, name, amount=100, unit='grams'):
        """
        Gets detailed information about an ingredient by name.

        :param name: The name of the ingredient.
        :param amount: The amount of the ingredient (optional, default is 100).
        :param unit: The unit of measure for the amount (optional, default is 'grams').
        :return: A dictionary containing detailed information about the ingredient.
        """
        ingredient_id = self.search_ingredient_by_name(name)
        if ingredient_id:
            info_url = f"{self.base_url}/food/ingredients/{ingredient_id}/information?apiKey={self.api_key}&amount={amount}&unit={unit}"
            response = requests.get(info_url)
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": "Failed to fetch ingredient information"}
        else:
            return {"error": "Ingredient not found"}
    
    def get_calories_by_ingredient_name(self, name, amount=100, unit='grams'):
        """
        Gets the calories value for an ingredient by name.

        :param name: The name of the ingredient.
        :return: The calories value of the ingredient or a message if not found.
        """
        ingredient_id = self.search_ingredient_by_name(name)
        if ingredient_id:
            info_url = f"{self.base_url}/food/ingredients/{ingredient_id}/information?apiKey={self.api_key}&amount=100&unit=grams"
            response = requests.get(info_url)
            if response.status_code == 200:
                data = response.json()
                nutrition = data.get('nutrition', {})
                nutrients = nutrition.get('nutrients', [])
                for nutrient in nutrients:
                    if nutrient['name'] == "Calories":
                        return {
                            "Calories": f"{nutrient['amount']} {nutrient['unit']}"
                        }
                return {"error": "Calories information not found"}
            else:
                return {"error": "Failed to fetch ingredient information"}
        else:
            return {"error": "Ingredient not found"}
        
# Exemplo

import translators as ts

if __name__ == "__main__":
    data = GetData()
    
    
    #recipeId = data.getRecipe("main course")
    #print("Recipe ID:", recipeId)
    #recipeCardUrl = data.createRecipeCard("Baked Chicken", "Chicken, Salt, Pepper", "1. Preheat the oven to 350 degrees F. 2. Season the chicken with salt and pepper. 3. Bake for 30 minutes, or until the chicken is cooked through.", 30, 4, "https://spoonacular.com/recipeImages/123.jpg")
    
    print("\n")
    pt_name = "maçã"
    print("portuguese name:", pt_name)
    en_name = ts.translate_text(pt_name, "bing", "pt", "en")
    print("english name:", en_name)
    print("Ingredient information:", data.get_calories_by_ingredient_name("apple"))
    print("\n")
    # print("\n")
    # print("Random Recipes:", data.getRandomRecipes(10, "main course"))
    # print("\n")
    # print("Recipe ID:", recipeId)
    # print("\n")
    # print("Recipe Name:", data.getRecipeName(recipeId))
    # print("\n")
    # print("Image URL:", data.getRecipeImage(recipeId))
    # print("\n")
    # print("Ingredients:", data.getRecipeIngredients(recipeId))
    # print("\n")
    # print("Tools:", data.getRecipeTools(recipeId))
    # print("\n")
    # print("Steps:", data.getRecipeSteps(recipeId))
    # print("\n")
    # print("Categories:", data.getCategories(recipeId))
    # print("\n")
    # print("Servings:", data.getRecipeServings(recipeId))
    # print("\n")
    # print("Time:", data.getRecipeTime(recipeId))
    # print("\n")
    # print("Recipe Card:", data.getRecipeCard(recipeId))
    # print("\n")
    # print("Recipe Name:", data.getRecipeNameByTag("dessert")) 
    
    #print("Recipe Card:", recipeCardUrl)
    #print("\n")