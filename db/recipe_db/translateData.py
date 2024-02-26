import translators as ts
from getData import GetData

# ts.translate_text(q_text, "google", "auto", "pt") 

data = GetData()

#recipeId = data.getRecipe("main course")

# get random recipes translated to portuguese
def randomRecipes(number="10", tag="main course"):
    #[ (RecipeID, name), (RecipeID, name), ...]
    randomRecipes = data.getRandomRecipes(number,tag)
    #print(randomRecipes)
    # Criar uma nova lista com os nomes das receitas modificados
    pt_recipes = [(key, ts.translate_text(value, "google", "auto", "pt")) for key, value in randomRecipes]

    return pt_recipes

def recipe(tag):
    recipe = data.getRecipeNameByTag(tag)
    #print(recipe)
    pt_recipe = ts.translate_text(recipe, "google", "auto", "pt")
    return pt_recipe
    
def recipeImage(recipeId):
    # 'https://spoonacular.com/recipeImages/595736-556x370.jpg'
    image_URL = data.getRecipeImage(recipeId)
    
    return image_URL

def categories(recipeId):
    # ['salad', 'lunch', 'main course', 'main dish', 'dinner']
    categories = data.getCategories(recipeId)
    pt_categories = [ts.translate_text(category, "google", "auto", "pt").lower() for category in categories]
    pt_tags = []
    
    for tag in pt_categories:
        pt_tags.append(tag) if tag not in pt_tags else None
    return pt_tags

def recipeCategory():
    categories = ["main course", "side dish", "dessert","appetizer","salad","bread","breakfast","soup","beverage","sauce","marinade","fingerfood","snack","drink"]
    pt_categories = [ts.translate_text(category, "google", "auto", "pt").lower() for category in categories]
    
    return pt_categories

def recipeTime(recipeId):
    # [20]
    cookingTime = data.getRecipeTime(recipeId)
    
    return cookingTime

def recipeServings(recipeId):
    # [4]
    servings = data.getRecipeServings(recipeId)
    
    return servings

def recipeHealthScore(recipeId):
    # [4]
    healthScore = data.getRecipeHealthScore(recipeId)
    
    return healthScore

def recipeIngredients(recipeId):
    # {
    #   'bacon': '0,227 kg', 
    #   'vinagre balsâmico': '0,5 xícara', 
    #   'queijo': '0,5 xícara', 
    #   'pimenta moída': '2.0 porções', 
    #   'sal kosher': '2.0 porções', 
    #   'azeite': '2.0 porções', 'cebola': 
    #   '0,5 xícara', 'alface': 
    #   '3.0 Cabeça'
    # }
    ingredients = data.getRecipeIngredients(recipeId)
    pt_ingredients = {ts.translate_text(key, "google", "auto", "pt"): ts.translate_text(value, "google", "auto", "pt") for key, value in ingredients.items()}
    
    return pt_ingredients

def recipeTools(recipeId):
    # ['frigideira', 'grelha']
    pt_tools = []
    for tool in (data.getRecipeTools(recipeId)).keys():
        if tool == "grill":
            pt_tools.append("grelha")
        else:
            pt_tools.append(ts.translate_text(tool, "google", "auto", "pt"))
    return pt_tools

def recipeSteps(recipeId):
    # {1: 
    #   {'description': 'Aqueça 1 colher de sopa de azeitona e cozinhe o bacon e a cebola até o bacon ficar crocante.', 
    #   'ingredients': ['bacon', 'azeitonas', 'cebola'], 
    #   'tools': []}, 
    # 2: 
    #   {'description': 'Remova a cebola e o bacon da panela.', 
    #   'ingredients': ['bacon', 'cebola'], 
    #   'tools': ['frigideira']}, 
    # 3: 
    #   {'description': 'Adicione mais 1 colher de sopa de azeite e vinagre balsâmico.', 
    #   'ingredients': ['vinagre balsâmico', 'azeite'], 
    #   'tools': []}, 
    # ...
    steps = data.getRecipeSteps(recipeId)
    pt_steps = {}
    for step_number, step_details in steps.items():
        # Traduz a descrição do passo
        pt_step_description = ts.translate_text(step_details['description'], "google", "auto", "pt")
        # Inicializa um dicionário para este passo
        pt_steps[step_number] = {
            'description': pt_step_description,
            'ingredients': [],
            'tools': []
        }
        
        # Traduz os ingredientes se existirem
        if step_details['ingredients']:
            pt_steps[step_number]['ingredients'] = [ts.translate_text(ingredient, "google", "auto", "pt") for ingredient in step_details['ingredients']]
        
        # Traduz os utensílios se existirem
        if step_details['tools']:
            pt_steps[step_number]['tools'] = [ts.translate_text(tool, "google", "auto", "pt") for tool in step_details['tools']]
    
    return pt_steps

# TESTS
#test_randomRecipes = randomRecipes(10, "main course")
#test_recipeImage = recipeImage(recipeId)
#test_recipeIngrients = recipeIngredients(recipeId)
#test_tools = recipeTools(recipeId)
#test_steps = recipeSteps(recipeId)
#test_categories = categories(recipeId)
#print(test_categories)
test_recipe = recipe("main course")
print(test_recipe)
# --------------------------------------------------------------------------------------------
#
# INITIAL TESTS
#
#
# print("\n")
# print("------------------------------------")
# print(" --- RECEITAS RANDOM --- ")
# print("------------------------------------")
# randomRecipes = data.getRandomRecipes(10, "main course")
# for key,value in randomRecipes:
#     print("Random Recipes:", value)
#     pt_randomRecipes = ts.translate_text(value, "google", "auto", "pt")
#     print("[pt]_randomRecipes", pt_randomRecipes)
#     print("----------------------------------------------------------------------")
# print("\n")    

# print("------------------------------------")
# print(" --- NOME DA RECEITA --- ")
# print("------------------------------------")    
# recipeName = data.getRecipeName(recipeId)
# pt_recipeName = ts.translate_text(recipeName, "google", "auto", "pt")
# print("recipeName:", recipeName)
# print("[pt]_recipeName", pt_recipeName)
# print("\n")

# print("------------------------------------")
# print(" --- URL IMAGEM DA RECEITA --- ")
# print("------------------------------------") 
# image_URL = data.getRecipeImage(recipeId)
# print("Image URL:", image_URL)
# print("\n")

# print("------------------------------------")
# print(" --- INGREDIENTES DA RECEITA --- ")
# print("------------------------------------") 
# ingredients = data.getRecipeIngredients(recipeId)
# for key,value in ingredients.items():
#     print("Ingridient:", key, "- Quantity:", value)
#     #print("Quantity:", value)
#     pt_key = ts.translate_text(key, "google", "auto", "pt")
#     pt_value = ts.translate_text(value, "google", "auto", "pt")
#     print("[pt]_Ingridient:", pt_key, "- Quantity:", pt_value)
#     print("----------------------------------------------------------------------")
# print("\n")   
    
# print("------------------------------------")
# print(" --- UTENSILIOS DA RECEITA --- ")
# print("------------------------------------") 
# tools = data.getRecipeTools(recipeId)
# for key,value in tools.items():
#     print("Tool:", key)
#     pt_key = ts.translate_text(key, "google", "auto", "pt")
#     print("[pt]_Tool:", pt_key)
#     print("----------------------------------------------------------------------")
# #trans_tools = ts.translate_text(tools, "google", "auto", "pt")
# print("\n")

# print("------------------------------------")
# print(" --- PASSOS DA RECEITA --- ")
# print("------------------------------------") 
# steps = data.getRecipeSteps(recipeId)
# for step_number, step_details in steps.items():
#     pt_step_details = ts.translate_text(step_details['description'], "google", "auto", "pt")
#     print(f"Step {step_number}: \n{step_details['description']} /\n[pt]", pt_step_details)
#     if step_details['ingredients']:
#         print("  Ingredients:")
#         for ingredient in step_details['ingredients']:
#             pt_ingredient = ts.translate_text(ingredient, "google", "auto", "pt")
#             print(f"    - {ingredient} /[pt]", pt_ingredient)
#     if step_details['tools']:
#         print("  Tools:")
#         for tool in step_details['tools']:
#             pt_tool = ts.translate_text(tool, "google", "auto", "pt")
#             print(f"    - {tool} /[pt]", pt_tool)
#     print()  # Print a newline for better readability between steps
#     print("----------------------------------------------------------------------")

# #trans_steps = ts.translate_text(steps, "google", "auto", "pt")
# print("\n")

# print("------------------------------------")
# print(" --- TEMPO PREPARAÇÃO DA RECEITA --- ")
# print("------------------------------------") 
# preparationTime = data.getPrepTime(recipeId)
# print("Preparation Time:", preparationTime)
# print("\n")

# print("------------------------------------")
# print(" --- TEMPO CONFEÇÃO DA RECEITA --- ")
# print("------------------------------------") 
# cookingTime = data.getCookTime(recipeId)
# print("Cooking Time:", cookingTime)
# print("\n")