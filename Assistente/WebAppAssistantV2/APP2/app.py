from flask import Flask, render_template,request, jsonify
import recipedb_queries as db
import convert_numbers_to_digit as convert
from flask_cors import CORS
import barcode_scanner as bs



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




@app.route('/scanner', methods=['POST'])
def get_product_barcode():
    frame = request.json.get('frameData')

    product_barcode = bs.barcode_scanner(frame)
   
    return jsonify(product_barcode)
    

    


# ----------------------------------------------------------------------------------------- ENDPOINT TO FETCH ALL RECIPES
@app.route('/recipes', methods=['GET'])
def fetch_recipes():
    """Fetch all recipes."""
    recipes = db.getRecipes()
    # Format each recipe to include only the desired fields
    formatted_recipes = [
        {
            'recipe_name': recipe['name'],
            'recipe_servings': recipe['number_of_servings'],
            'recipe_time': recipe['cooking_time']
        }
        for recipe in recipes
    ]
    return jsonify(formatted_recipes)

# ----------------------------------------------------------------------------------------- ENDPOINT TO FETCH RECIPE BY TAG
@app.route('/recipe/tag/<tag>', methods=['GET'])
def fetch_recipe_by_tag(tag):
    """Fetch recipes by tag."""
    recipe_ids = db.getRecipeByTag(tag)
    return jsonify({'recipe_ids': recipe_ids})

# ----------------------------------------------------------------------------------------- ENDPOINT TO FETCH RECIPE BY NAME
@app.route('/recipe/name/<name>', methods=['GET'])
def fetch_recipe_by_name(name):
    """Fetch a recipe by name."""
    recipe_id = db.getRecipe(name)
    if recipe_id:
        return jsonify({'recipe_id': recipe_id})
    else:
        return jsonify({'error': 'Recipe not found'}), 404

# ----------------------------------------------------------------------------------------- ENDPOINT TO FETCH INGREDIENTS FOR A GIVEN RECIPE ID
@app.route('/recipe/<int:recipe_id>/ingredients', methods=['GET'])
def fetch_ingredients(recipe_id):
    """Fetch ingredients for a given recipe ID."""
    ingredients = db.getIngredients(recipe_id)
    return jsonify(ingredients)

# ----------------------------------------------------------------------------------------- ENDPOINT TO FETCH TOOLS FOR A GIVEN RECIPE ID
@app.route('/recipe/<int:recipe_id>/tools', methods=['GET'])
def fetch_tools(recipe_id):
    """Fetch tools for a given recipe ID."""
    tools = db.getTools(recipe_id)
    return jsonify(tools)

# ----------------------------------------------------------------------------------------- ENDPOINT TO FETCH A RANDOM RECIPE
@app.route('/recipe/random', methods=['GET'])
def fetch_random_recipe():
    """Fetch a random recipe."""
    recipe_id = db.getRandomRecipe()
    #print("recipe_id", recipe_id)
    recipe_name = db.getRecipeName(recipe_id) if recipe_id else None
    recipe_img = db.getImg_url(recipe_id) if recipe_id else None
    #print("recipe_name", recipe_name)
    return jsonify({'recipe_id': recipe_id, 'recipe_name': recipe_name, 'recipe_img': recipe_img})

# ----------------------------------------------------------------------------------------- ENDPOINT TO FETCH NEXT INSTRUCTION FOR A GIVEN RECIPE ID AND CURRENT STEP
@app.route('/recipe/<int:recipe_id>/next-instruction/<int:step>', methods=['GET'])
def fetch_next_instruction(recipe_id, step):
    """Fetch the next instruction for a given recipe ID and current step."""
    next_instruction = db.getNextInstruction(recipe_id, step)
    return jsonify({'next_instruction': next_instruction})

# ----------------------------------------------------------------------------------------- ENDPOINT TO FETCH PREVIOUS INSTRUCTION FOR A GIVEN RECIPE ID AND CURRENT STEP
@app.route('/recipe/<int:recipe_id>/previous-instruction/<int:step>', methods=['GET'])
def fetch_previous_instruction(recipe_id, step):
    """Fetch the previous instruction for a given recipe ID and current step."""
    previous_instruction = db.getPreviousInstruction(recipe_id, step)
    return jsonify({'previous_instruction': previous_instruction})

# ----------------------------------------------------------------------------------------- ENDPOINT TO FETCH ACTUAL INSTRUCTION FOR A GIVEN RECIPE ID AND CURRENT STEP
@app.route('/recipe/<int:recipe_id>/actual-instruction/<int:step>', methods=['GET'])
def fetch_actual_instruction(recipe_id, step):
    """Fetch the previous instruction for a given recipe ID and current step."""
    actual_instruction = db.getActualInstruction(recipe_id, step)
    return jsonify({'actual_instruction': actual_instruction})

# ----------------------------------------------------------------------------------------- ENDPOINT TO FETCH RECIPE NAME BY ID
@app.route('/recipe/<int:recipe_id>/name', methods=['GET'])
def fetch_recipe_name(recipe_id):
    """Fetch the name for a given recipe ID."""
    recipe_name = db.getRecipeName(recipe_id)
    if recipe_name:
        return jsonify({'recipe_name': recipe_name})
    else:
        return jsonify({'error': 'Recipe not found'}), 404

# ----------------------------------------------------------------------------------------- ENDPOINT TO FETCH RECIPE IMAGE
@app.route('/recipe/<int:recipe_id>/image', methods=['GET'])
def fetch_recipe_image(recipe_id):
    """Fetch the image URL for a given recipe ID."""
    img_url = db.getImg_url(recipe_id)
    if img_url:
        return jsonify({'img_url': img_url})
    else:
        return jsonify({'error': 'Image not found for the specified recipe'}), 404

# ----------------------------------------------------------------------------------------- ENDPOINT TO CONVERT TEXT NUMBERS TO DIGITS    
@app.route('/convert-text', methods=['POST'])
def convert_text():
    # Check if the request contains JSON data
    if not request.json or 'text' not in request.json:
        return jsonify({'error': 'Request must be JSON and contain a "text" field.'}), 400

    text_to_convert = request.json['text']
    
    # Use the conversion function from your module
    converted_text = convert.extract_and_convert_numeric_phrases(text_to_convert, convert.numbers_dict)
    
    if converted_text is not None:
        return jsonify(converted_text)
    else:
        return jsonify({'error': 'Failed to convert text.'}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)