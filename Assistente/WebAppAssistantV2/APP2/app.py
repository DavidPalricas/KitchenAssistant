from flask import Flask, render_template,request, jsonify
# ----------------------------------------------------------------------------------------- MODULE: Recipedb_queries
import recipedb_queries as db
# ----------------------------------------------------------------------------------------- MODULE: Pantrydb_queries
import pantrydb_queries as pdb
# ----------------------------------------------------------------------------------------- MODULE: convert_numbers_to_digit
import convert_numbers_to_digit as convert
# ----------------------------------------------------------------------------------------- MODULE: barcode_scanner
import barcode_scanner as bs
# ----------------------------------------------------------------------------------------- MODULE: email_service
import email_service as es
# ----------------------------------------------------------------------------------------- MODULE: API_OpenFoodFacts
import API_OpenFoodFacts as api_op


from decimal import Decimal
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



# ----------------------------------- > [ RECIPES DATABASE -> ENDPOINTS]

# ----------------------------------------------------------------------------------------- > FETCH ALL RECIPES
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

# ----------------------------------------------------------------------------------------- > FETCH RECIPE BY TAG
@app.route('/recipe/tag/<tag>', methods=['GET'])
def fetch_recipe_by_tag(tag):
    """Fetch recipes by tag."""
    recipe_ids = db.getRecipeByTag(tag)
    return jsonify({'recipe_ids': recipe_ids})

# ----------------------------------------------------------------------------------------- > FETCH RECIPE BY NAME
@app.route('/recipe/name/<name>', methods=['GET'])
def fetch_recipe_by_name(name):
    """Fetch a recipe by name."""
    recipe_id = db.getRecipe(name)
    if recipe_id:
        return jsonify({'recipe_id': recipe_id})
    else:
        return jsonify({'error': 'Recipe not found'}), 404

# ----------------------------------------------------------------------------------------- > FETCH INGREDIENTS FOR A GIVEN RECIPE ID
@app.route('/recipe/<int:recipe_id>/ingredients', methods=['GET'])
def fetch_ingredients(recipe_id):
    """Fetch ingredients for a given recipe ID."""
    ingredients = db.getIngredients(recipe_id)
    return jsonify(ingredients)

# ----------------------------------------------------------------------------------------- > FETCH TOOLS FOR A GIVEN RECIPE ID
@app.route('/recipe/<int:recipe_id>/tools', methods=['GET'])
def fetch_tools(recipe_id):
    """Fetch tools for a given recipe ID."""
    tools = db.getTools(recipe_id)
    return jsonify(tools)

# ----------------------------------------------------------------------------------------- > FETCH A RANDOM RECIPE
@app.route('/recipe/random', methods=['GET'])
def fetch_random_recipe():
    """Fetch a random recipe."""
    recipe_id = db.getRandomRecipe()
    #print("recipe_id", recipe_id)
    recipe_name = db.getRecipeName(recipe_id) if recipe_id else None
    recipe_img = db.getImg_url(recipe_id) if recipe_id else None
    #print("recipe_name", recipe_name)
    return jsonify({'recipe_id': recipe_id, 'recipe_name': recipe_name, 'recipe_img': recipe_img})

# ----------------------------------------------------------------------------------------- > FETCH NEXT INSTRUCTION FOR A GIVEN RECIPE ID AND CURRENT STEP
@app.route('/recipe/<int:recipe_id>/next-instruction/<int:step>', methods=['GET'])
def fetch_next_instruction(recipe_id, step):
    """Fetch the next instruction for a given recipe ID and current step."""
    next_instruction = db.getNextInstruction(recipe_id, step)
    return jsonify({'next_instruction': next_instruction})

# ----------------------------------------------------------------------------------------- > FETCH PREVIOUS INSTRUCTION FOR A GIVEN RECIPE ID AND CURRENT STEP
@app.route('/recipe/<int:recipe_id>/previous-instruction/<int:step>', methods=['GET'])
def fetch_previous_instruction(recipe_id, step):
    """Fetch the previous instruction for a given recipe ID and current step."""
    previous_instruction = db.getPreviousInstruction(recipe_id, step)
    return jsonify({'previous_instruction': previous_instruction})

# ----------------------------------------------------------------------------------------- > FETCH ACTUAL INSTRUCTION FOR A GIVEN RECIPE ID AND CURRENT STEP
@app.route('/recipe/<int:recipe_id>/actual-instruction/<int:step>', methods=['GET'])
def fetch_actual_instruction(recipe_id, step):
    """Fetch the previous instruction for a given recipe ID and current step."""
    actual_instruction = db.getActualInstruction(recipe_id, step)
    return jsonify({'actual_instruction': actual_instruction})

# ----------------------------------------------------------------------------------------- > FETCH RECIPE NAME BY ID
@app.route('/recipe/<int:recipe_id>/name', methods=['GET'])
def fetch_recipe_name(recipe_id):
    """Fetch the name for a given recipe ID."""
    recipe_name = db.getRecipeName(recipe_id)
    if recipe_name:
        return jsonify({'recipe_name': recipe_name})
    else:
        return jsonify({'error': 'Recipe not found'}), 404

# ----------------------------------------------------------------------------------------- > FETCH RECIPE IMAGE
@app.route('/recipe/<int:recipe_id>/image', methods=['GET'])
def fetch_recipe_image(recipe_id):
    """Fetch the image URL for a given recipe ID."""
    img_url = db.getImg_url(recipe_id)
    if img_url:
        return jsonify({'img_url': img_url})
    else:
        return jsonify({'error': 'Image not found for the specified recipe'}), 404

# ----------------------------------------------------------------------------------------- > CONVERT TEXT NUMBERS TO DIGITS    
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



# ----------------------------------- > [ PANTRY DATABASE -> ENDPOINTS]

# ----------------------------------------------------------------------------------------- > INSERT PRODUCT INTO PANTRY
@app.route('/pantry/insert-stock', methods=['POST'])
def insert_stock():    
    data = request.json
    name = data.get('name')
    quantity = data.get('quantity')
    unit = data.get('unit')
    expiration_date = data.get('expiration_date')
    
    # ensure all required fields are present
    if not all([name, quantity, unit, expiration_date]):
        return jsonify({'error': 'Missing required fields.'}), 400
    
    try:
        pdb.insertStock(name, quantity, unit, expiration_date)
        return jsonify({'message': 'Stock inserted successfully.'}), 201
    except Exception as e:
        return jsonify({'error': f'Failed to insert stock: {e}'}), 500

# ----------------------------------------------------------------------------------------- > REMOVE PRODUCT FROM PANTRY
@app.route('/pantry/remove-stock', methods=['POST'])
def remove_stock():
    data = request.json
    name = data.get('name')
    quantity = data.get('quantity')
    unit = data.get('unit')
    
    if not all([name, quantity, unit]):
        return jsonify({'error': 'Missing required field: "name".'}), 400
    
    try:
        if not isinstance(quantity, Decimal):
            quantity = Decimal(quantity)
            
        pdb.removeStock(name, quantity, unit)
        return jsonify({'message': 'Stock removed successfully.'}), 200
    except Exception as e:
        return jsonify({'error': f'Failed to remove stock: {e}'}), 500

# ----------------------------------------------------------------------------------------- > FETCH ALL PRODUCTS IN PANTRY
@app.route('/pantry/stock', methods=['GET'])
def get_pantry_stock():
    pantry_list = pdb.getStockDetails()
    return jsonify(pantry_list)



# ----------------------------------- > [ SHOPPING LIST DATABASE -> ENDPOINTS]

# ----------------------------------------------------------------------------------------- > ADD PRODUCT INTO GROCERY LIST
@app.route('/pantry/insert-grocery', methods=['POST'])
def insert_grocery():
    data = request.json
    name = data.get('name')
    
    if not name:
        return jsonify({'error': 'Missing required field: "name".'}), 400

    try:
        result = pdb.insertGrocery(name)
        if 'already exists in the GROCERY LIST' in result:
            return jsonify({'message': result}), 409
        else:
            return jsonify({'message': result}), 201
    except Exception as e:
        return jsonify({'error': f'Failed to insert grocery item: {str(e)}'}), 500

# ----------------------------------------------------------------------------------------- > REMOVE PRODUCT FROM GROCERY LIST
@app.route('/pantry/remove-grocery', methods=['DELETE'])
def remove_grocery():
    data = request.json
    name = data.get('name')
    
    if not name:
        return jsonify({'error': 'Missing required field: "name".'}), 400

    try:
        result = pdb.removeGrocery(name)
        return jsonify({'message': result}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
 
# ----------------------------------------------------------------------------------------- > FETCH ALL GROCERY LIST
@app.route('/pantry/shopping-list', methods=['GET'])
def get_grocery_list():
    grocery_list = pdb.showAllGrocery()
    return jsonify(grocery_list)



# ----------------------------------- > [ BARCODE -> ENDPOINTS]

# ----------------------------------------------------------------------------------------- > GET PRODUCT NAME, QUANTITY AND UNIT FROM BARCODE
@app.route('/scanner', methods=['POST'])
def get_product_barcode():
    frame = request.json.get('frameData')

    product_barcode = bs.barcode_scanner(frame)

    if product_barcode:
        prodcut_name,product_quantity,product_img_url= api_op.get_product_name(product_barcode)
        return jsonify(prodcut_name,product_quantity,product_img_url)
    else:
        return jsonify(None)


   
# ----------------------------------- > [ EMAIL -> ENDPOINTS]

# ----------------------------------------------------------------------------------------- > SEND EMAIL
@app.route('/send-email', methods=['POST'])
def send_email():
    data = request.json  # Get data from POST request
    
    # Extract data from POST request
    from_addr = data.get('from_addr')
    to_addr = data.get('to_addr')
    subject = data.get('subject')
    body = data.get('body')
    smtp_server = data.get('smtp_server', 'smtp-mail.outlook.com')
    smtp_port = data.get('smtp_port', 587)
    password = data.get('password')

    # Call the send_email function from the email_service module
    result = es.send_email(from_addr, to_addr, subject, body, smtp_server, smtp_port, password)
    
    # Return result as JSON
    if "successfully" in result:
        return jsonify({'message': result}), 200
    else:
        return jsonify({'error': result}), 500
    

if __name__ == '__main__':
    app.run(debug=True, port=5000)
    
    