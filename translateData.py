import translators as ts
from getData import GetData

# ts.translate_text(q_text, "google", "auto", "pt") 

data = GetData()

recipeId = data.getRecipe("main course")

def randomRecipes(self, number="20", tag="main course"):
    randomRecipes = data.getRandomRecipes(number, tag)
    for key,value in randomRecipes:
        pt_randomRecipes = ts.translate_text(value, "google", "auto", "pt")
        key = pt_randomRecipes
    return key,value

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