from flask import Flask, render_template,request, jsonify
import recipedb_queries as db
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# CODE TO WORK WITH RASA DIRECTLY
# RASA_API = "http://localhost:5005/webhooks/rest/webhook" # Url da API do Rasa
# @app.route("/")
# def index():
#     return  render_template("index.html")

# @app.route("/webhook", methods=["POST"])

# def webhook(): 
#     user_message = request.json["message"]
#     print(f"Messangem do usuário: {user_message}")

#     response = requests.post(RASA_API, json={"message": user_message})
#     response = response.json()
#     print(f"Resposta do Rasa: {response}")
    
#     rasa_response = ""
#     for r in response:
#         rasa_response += r["text"] + "\n\n\n" #Caso a mensagem tenha mais de uma linha


#     return jsonify({"response": rasa_response})


# if __name__ == "__main__":
#     app.run(debug=True) # Para mostrar os erros no browser



@app.route('/recipes', methods=['GET'])
def fetch_recipes():
    """Fetch all recipes."""
    recipes = db.getRecipes()
    return jsonify(recipes)

@app.route('/recipe/tag/<tag>', methods=['GET'])
def fetch_recipe_by_tag(tag):
    """Fetch recipes by tag."""
    recipe_ids = db.getRecipeByTag(tag)
    return jsonify({'recipe_ids': recipe_ids})

@app.route('/recipe/name/<name>', methods=['GET'])
def fetch_recipe_by_name(name):
    """Fetch a recipe by name."""
    recipe_id = db.getRecipe(name)
    if recipe_id:
        return jsonify({'recipe_id': recipe_id})
    else:
        return jsonify({'error': 'Recipe not found'}), 404

@app.route('/recipe/<int:recipe_id>/ingredients', methods=['GET'])
def fetch_ingredients(recipe_id):
    """Fetch ingredients for a given recipe ID."""
    ingredients = db.getIngredients(recipe_id)
    return jsonify(ingredients)

@app.route('/recipe/<int:recipe_id>/tools', methods=['GET'])
def fetch_tools(recipe_id):
    """Fetch tools for a given recipe ID."""
    tools = db.getTools(recipe_id)
    return jsonify(tools)

@app.route('/recipe/random', methods=['GET'])
def fetch_random_recipe():
    """Fetch a random recipe."""
    recipe_id = db.getRandomRecipe()
    #print("recipe_id", recipe_id)
    recipe_name = db.getRecipeName(recipe_id) if recipe_id else None
    recipe_img = db.getImg_url(recipe_id) if recipe_id else None
    #print("recipe_name", recipe_name)
    return jsonify({'recipe_id': recipe_id, 'recipe_name': recipe_name, 'recipe_img': recipe_img})

@app.route('/recipe/<int:recipe_id>/next-instruction/<int:step>', methods=['GET'])
def fetch_next_instruction(recipe_id, step):
    """Fetch the next instruction for a given recipe ID and current step."""
    next_instruction = db.getNextInstruction(recipe_id, step)
    return jsonify({'next_instruction': next_instruction})

@app.route('/recipe/<int:recipe_id>/previous-instruction/<int:step>', methods=['GET'])
def fetch_previous_instruction(recipe_id, step):
    """Fetch the previous instruction for a given recipe ID and current step."""
    previous_instruction = db.getPreviousInstruction(recipe_id, step)
    return jsonify({'previous_instruction': previous_instruction})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
    
    print("RANDOM RECIPE: ", db.getRandomRecipe())