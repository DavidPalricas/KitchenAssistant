"""
@brief Este módulo configura e executa um servidor Flask que serve como backend para o Assistente Virtual., 
manipulando receitas, despensa, lista de compras, conversão de texto e digitalização de códigos de barras.

Este servidor fornece uma API REST para interagir com bases de dados de receitas e despensa, 
permitindo operações como consulta, inserção e remoção de receitas, ingredientes e itens de despensa. 
Também inclui funcionalidades para conversão de texto em números e datas, 
além de descodificação de códigos de barras e envio de e-mails.

@details Este arquivo organiza os endpoints em seções distintas para cada tipo de funcionalidade:
- Base de dados de receitas
- Base de dados da despensa
- Lista de compras
- Conversões e formatações
- Digitalização de códigos de barras
- Envio de e-mails

Os endpoints interagem com módulos externos importados para acessar dados e executar lógicas específicas, 
como consultas à base de dados, análises de texto e imagem, e comunicações de rede. 
Os módulos externos:
- @ref recipedb_queries: Funções para acessar e manipular o banco de dados de receitas.
- @ref pantrydb_queries: Funções para gerenciar o banco de dados da despensa.
- @ref convert_numbers_to_digit: Funções para converter números escritos em texto para formato digital.
- @ref barcode_scanner: Funções para decodificar códigos de barras de imagens.
- @ref email_service: Funções para configurar e enviar e-mails.
- @ref API_OpenFoodFacts: Funções para interagir com a API Open Food Facts e obter dados de produtos.
- @ref format_date: Funções para formatar datas expressas em texto para um formato padrão.
- @ref get_product: Funções para extrair informações de produtos a partir de sentenças.

@note A maioria dos endpoints inclui tratamento de erros que retorna mensagens de erro adequadas como respostas JSON 
quando ocorrem exceções ou dados de entrada estão faltando ou são inválidos.

"""

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
# ----------------------------------------------------------------------------------------- MODULE: format_date
import format_date as fd
# ----------------------------------------------------------------------------------------- MODULE: get_product
import get_product as gp
# ----------------------------------------------------------------------------------------- MODULE: requests
import json

from decimal import Decimal
from flask_cors import CORS
 
"""@var app
    @brief This is the Flask app instance that handles all the web service routes.
"""
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
    """
    @brief Obtém todas as receitas da base de dados.

    @details Este endpoint recupera todas as receitas armazenadas na base de dados e formata cada receita
    para incluir apenas o nome, número de porções e tempo de confeção. A função chama a
    função `getRecipes()` do módulo `recipedb_queries`, que se espera que retorne
    um dicionário onde cada key representa uma receita.

    O endpoint formata a resposta num objeto JSON que inclui apenas (nome, número de porções e tempo de confeção).
    Isto é projetado para fornecer uma visão simplificada das receitas.

    @return JSON Uma resposta JSON contendo um array de receitas, onde cada receita é um dicionário
    com as chaves 'recipe_name', 'recipe_servings' e 'recipe_time'.

    @par Exemplo de como utilizar este endpoint:
    \verbatim
        curl -X GET http://127.0.0.1:5000/recipes
    \endverbatim
    
    @retval JSON Exemplo de uma resposta bem-sucedida:
    @code
    [
        {
            "recipe_name": "Esparguete à Carbonara",
            "recipe_servings": 4,
            "recipe_time": "30 minutos"
        },
        {
            "recipe_name": "Pizza Margherita",
            "recipe_servings": 2,
            "recipe_time": "20 minutos"
        }
    ]
    @endcode

    @note Este endpoint não requer quaisquer argumentos e não lida internamente com quaisquer exceções.
    Quaisquer erros na camada de acesso à base de dados (como problemas de conexão ou erros SQL)
    precisam ser tratados pela função `getRecipes()` e devem ser registrados adequadamente.

    @see recipedb_queries.getRecipes()
    """
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
    """
    @brief Obtém as IDs das receitas associadas a uma tag.

    @details Este endpoint é utilizado para obter todas os IDs de receitas que estão associadas a uma
    tag. A tag é passada como parte do URL. A função chama `getRecipeByTag(tag)` do módulo
    `recipedb_queries`, que deve buscar na base de dados e retornar uma lista de IDs de receitas que correspondem
    à tag fornecida.

    @param tag A tag pela qual as receitas serão pesquisadas na base de dados.

    @return JSON Uma resposta JSON contendo um objeto que inclui uma chave 'recipe_ids', cujo valor é uma lista
    dos IDs das receitas associadas à tag fornecida.

    @par Exemplo de como utilizar este endpoint:
    \verbatim
        curl -X GET http://127.0.0.1:5000/recipe/tag/mousse
    \endverbatim
    
    @retval JSON Exemplo de uma resposta bem-sucedida:
    @code
    {
        "recipe_ids": [76]
    }
    @endcode

    @retval JSON Exemplo de uma resposta mal-sucedida:
    @code
    {
        "recipe_ids": null
    }
    @endcode

    @see recipedb_queries.getRecipeByTag(`tag`)
    """
    recipe_ids = db.getRecipeByTag(tag)
    return jsonify({'recipe_ids': recipe_ids})

# ----------------------------------------------------------------------------------------- > FETCH RECIPE BY NAME
@app.route('/recipe/name/<name>', methods=['GET'])
def fetch_recipe_by_name(name):
    """
    @brief Obtém a ID de uma receita pelo seu nome.

    @details Este endpoint é utilizado para recuperar a ID de uma receita baseada no seu nome.
    O nome é passado como parte do URL. A função consulta a base de dados através da função `getRecipe(name)`
    do módulo `recipedb_queries`, que retorna a ID da receita se encontrada.

    @param name O nome da receita a ser pesquisada. O nome deve ser passado na URL como uma string.

    @return JSON Retorna um objeto JSON contendo a ID da receita encontrada, ou uma mensagem de erro se a receita
    não for encontrada na base de dados.

    @par Exemplo de como utilizar este endpoint:
    \verbatim
        curl -X GET http://127.0.0.1:5000/recipe/name/Amêijoas à Bulhão Pato
    \endverbatim
    
    @warning NOT WORKING
    
    @retval JSON Exemplo de uma resposta bem-sucedida:
    @code
    {
        "recipe_id": 123
    }
    @endcode

    @retval JSON Exemplo de uma resposta quando a receita não é encontrada:
    @code
    {
        "error": "Recipe not found"
    }
    @endcode

    @note O nome da receita é case-sensitive e deve corresponder exatamente ao valor na base de dados para que a ID
    seja retornada. Este endpoint retorna um status HTTP 404 se a receita não for encontrada.

    @see recipedb_queries.getRecipe(`name`)
    """
    recipe_id = db.getRecipe(name)
    if recipe_id:
        return jsonify({'recipe_id': recipe_id})
    else:
        return jsonify({'error': 'Recipe not found'}), 404

# ----------------------------------------------------------------------------------------- > FETCH INGREDIENTS FOR A GIVEN RECIPE ID
@app.route('/recipe/<int:recipe_id>/ingredients', methods=['GET'])
def fetch_ingredients(recipe_id):
    """
    @brief Obtém os ingredientes para uma dada ID de receita.

    @details Este endpoint é utilizado para recuperar a lista de ingredientes de uma receita específica.
    A função consulta a base de dados através da função `getIngredients(recipe_id)` do módulo `recipedb_queries`,
    que retorna uma lista de ingredientes associados à ID da receita.

    @param recipe_id A ID da receita para a qual os ingredientes são solicitados. A ID é passada na URL como um inteiro.

    @par Exemplo de como utilizar este endpoint:
    \verbatim
        curl -X POST http://127.0.0.1:5000/recipe/62/ingredients
    \endverbatim
    
    @return JSON Retorna um array de objetos JSON, cada um representando um ingrediente com nome, quantidade e unidade.
    
    @retval JSON Exemplo de uma resposta bem-sucedida:
    @code
        [
            {
                "name": "Amêijoas",
                "quantity": "1.00",
                "unit": "kg"
            },
            {
                "name": "Azeite",
                "quantity": "1.00",
                "unit": "dl"
            },
            ...
        ]
    @endcode
    
    @note Se a receita não for encontrada, o endpoint retorna um array vazio.
    
    @see recipedb_queries.getIngredients(`recipe_id`)
    """
    ingredients = db.getIngredients(recipe_id)
    return jsonify(ingredients)

# ----------------------------------------------------------------------------------------- > FETCH TOOLS FOR A GIVEN RECIPE ID
@app.route('/recipe/<int:recipe_id>/tools', methods=['GET'])
def fetch_tools(recipe_id):
    """
    @brief Obtém as ferramentas para uma dada ID de receita.

    @details Este endpoint é utilizado para recuperar a lista de ferramentas necessárias para preparar uma receita.
    A função consulta a base de dados através da função `getTools(recipe_id)` do módulo `recipedb_queries`,
    que retorna uma lista de ferramentas associadas à ID da receita.

    @param recipe_id A ID da receita para a qual as ferramentas são solicitadas. A ID é passada na URL como um inteiro.

    @return JSON Retorna um array de strings, cada uma representando uma ferramenta necessária para a receita.

    @par Exemplo de como utilizar este endpoint:
    \verbatim
        curl -X POST http://127.0.0.1:5000/recipe/62/tools
    \endverbatim
    
    @retval JSON Exemplo de uma resposta bem-sucedida:
    @code
        [
            [
                "Recipiente grande"
            ],
            [
                "Tacho largo"
            ],
            ...
        ]            
    @endcode
    
    @note Se a receita não for encontrada, o endpoint retorna um array vazio.
    
    @see recipedb_queries.getTools(`recipe_id`)
    """
    tools = db.getTools(recipe_id)
    return jsonify(tools)

# ----------------------------------------------------------------------------------------- > FETCH A RANDOM RECIPE
@app.route('/recipe/random', methods=['GET'])
def fetch_random_recipe():
    """
    @brief Obtém uma receita aleatória.

    @details Este endpoint seleciona uma receita aleatória da base de dados e retorna a sua ID, nome e imagem associada.
    A função utiliza a `getRandomRecipe()` para obter uma ID de receita aleatória e posteriormente recupera o nome e a imagem usando
    `getRecipeName(recipe_id)` e `getImg_url(recipe_id)` respectivamente, do módulo `recipedb_queries`.

    @return JSON Retorna um objeto JSON contendo a ID da receita, nome e URL da imagem. Se nenhuma receita for encontrada, retorna nulo.
    
    @par Exemplo de como utilizar este endpoint:
    \verbatim
        curl -X POST http://127.0.0.1:5000/recipe/random
    \endverbatim
    
    @retval JSON Exemplo de uma resposta bem-sucedida:
    @code
        {
            "recipe_id": 79,
            "recipe_img": "https://www.saborintenso.com/images/receitas/Sopa-de-Alho-Frances-e-Cenoura-SI-2.jpg",
            "recipe_name": "Sopa de Alho Francês e Cenoura"
        }
    @endcode
    
    @note Se a receita não for encontrada, o endpoint retorna um objeto JSON com valores nulos, apenas quando não existem receitas na base de dados.
    
    @see recipedb_queries.getRandomRecipe()
    @see recipedb_queries.getRecipeName(`recipe_id`)
    @see recipedb_queries.getImg_url(`recipe_id`)
    """
    recipe_id = db.getRandomRecipe()
    #print("recipe_id", recipe_id)
    recipe_name = db.getRecipeName(recipe_id) if recipe_id else None
    recipe_img = db.getImg_url(recipe_id) if recipe_id else None
    #print("recipe_name", recipe_name)
    return jsonify({'recipe_id': recipe_id, 'recipe_name': recipe_name, 'recipe_img': recipe_img})

# ----------------------------------------------------------------------------------------- > FETCH NEXT INSTRUCTION FOR A GIVEN RECIPE ID AND CURRENT STEP
@app.route('/recipe/<int:recipe_id>/next-instruction/<int:step>', methods=['GET'])
def fetch_next_instruction(recipe_id, step):
    """
    @brief Obtém a próxima instrução para uma dada ID de receita e passo atual.

    @details Este endpoint é usado para obter a descrição do próximo passo de uma receita específica.
    Utiliza a função `getNextInstruction(recipe_id, step)` do módulo `recipedb_queries` para recuperar a próxima instrução com base no passo atual.

    @param recipe_id A ID da receita cuja próxima instrução é solicitada.
    @param step O número do passo atual dentro da receita.

    @return JSON Retorna um objeto JSON contendo a descrição do próximo passo.
    
    @par Exemplo de como utilizar este endpoint:
    \verbatim
        curl -X POST http://127.0.0.1:5000/recipe/62/next-instruction/2
    \endverbatim
    
    @retval JSON Exemplo de uma resposta bem-sucedida:
    @code
        {
            "next_instruction": "Depois de todas as am\êijoas abertas, coloque-as numa taça grande.  Deixe o molho apurar mais 2 minutos.  Regue as amêijoas com o molho e tempere com sumo de limão.  Por fim, decore com gomos de limão e está pronto a ser consumido."
        }
    @endcode
    
    @retval JSON Exemplo de uma resposta mal-sucedida:
    @code
        {
            "next_instruction": null
        }
    @endcode
    
    @see recipedb_queries.getNextInstruction(`recipe_id`, `step`)
    """
    next_instruction = db.getNextInstruction(recipe_id, step)
    return jsonify({'next_instruction': next_instruction})

# ----------------------------------------------------------------------------------------- > FETCH PREVIOUS INSTRUCTION FOR A GIVEN RECIPE ID AND CURRENT STEP
@app.route('/recipe/<int:recipe_id>/previous-instruction/<int:step>', methods=['GET'])
def fetch_previous_instruction(recipe_id, step):
    """
    @brief Obtém a instrução anterior para uma dada ID de receita e passo atual.

    @details Este endpoint é usado para obter a descrição do passo anterior de uma receita específica.
    Utiliza a função `getPreviousInstruction(recipe_id, step)` do módulo `recipedb_queries` para recuperar a instrução anterior com base no passo atual.

    @param recipe_id A ID da receita cuja instrução anterior é solicitada.
    @param step O número do passo atual dentro da receita.

    @return JSON Retorna um objeto JSON contendo a descrição do passo anterior.
    
    @par Exemplo de como utilizar este endpoint:
    \verbatim
        curl -X POST http://127.0.0.1:5000/recipe/62/previous-instruction/2
    \endverbatim
    
    @retval JSON Exemplo de uma resposta bem-sucedida:
    @code
        {
            "previous_instruction": "Deite as amêijoas num recipiente grande, encha de água e coloque sal, deixe repousar pelo menos 3 horas para perderem a areia.  Passadas as três horas lave bem as amêijoas."
        }
    @endcode
    
    @retval JSON Exemplo de uma resposta mal-sucedida:
    @code
        {
            "previous_instruction": null
        }
    @endcode
    
    @see recipedb_queries.getPreviousInstruction(`recipe_id`, `step`)
    """
    previous_instruction = db.getPreviousInstruction(recipe_id, step)
    return jsonify({'previous_instruction': previous_instruction})

# ----------------------------------------------------------------------------------------- > FETCH ACTUAL INSTRUCTION FOR A GIVEN RECIPE ID AND CURRENT STEP
@app.route('/recipe/<int:recipe_id>/actual-instruction/<int:step>', methods=['GET'])
def fetch_actual_instruction(recipe_id, step):
    """
    @brief Obtém a instrução atual para uma dada ID de receita e passo atual.

    @details Este endpoint é usado para obter a descrição do passo atual de uma receita específica.
    Utiliza a função `getActualInstruction(recipe_id, step)` do módulo `recipedb_queries` para recuperar a instrução atual com base no passo fornecido.

    @param recipe_id A ID da receita cuja instrução atual é solicitada.
    @param step O número do passo atual dentro da receita.

    @return JSON Retorna um objeto JSON contendo a descrição do passo atual.
    
    @par Exemplo de como utilizar este endpoint:
    \verbatim
        curl -X POST http://127.0.0.1:5000/recipe/62/actual-instruction/2
    \endverbatim
    
    @retval JSON Exemplo de uma resposta bem-sucedida:
    @code
        {
            "actual_instruction": "Deite as amêijoas num recipiente grande, encha de àgua e coloque sal, deixe repousar pelo menos 3 horas para perderem a areia.  Passadas as três horas lave bem as amêijoas."
        }
    @endcode
    
    @retval JSON Exemplo de uma resposta mal-sucedida:
    @code
        {
            "actual_instruction": null
        }
    @endcode
    
    @see recipedb_queries.getActualInstruction(`recipe_id`, `step`)
    """
    actual_instruction = db.getActualInstruction(recipe_id, step)
    return jsonify({'actual_instruction': actual_instruction})

# ----------------------------------------------------------------------------------------- > FETCH RECIPE NAME BY ID
@app.route('/recipe/<int:recipe_id>/name', methods=['GET'])
def fetch_recipe_name(recipe_id):
    """
    @brief Obtém o nome de uma receita dado o seu ID.

    @details Este endpoint é usado para obter o nome de uma receita específica utilizando a sua ID.
    Utiliza a função `getRecipeName(recipe_id)` do módulo `recipedb_queries`. Se o nome da receita for encontrado,
    ele será retornado, caso contrário, uma mensagem de erro será retornada indicando que a receita não foi encontrada.

    @param recipe_id A ID da receita cujo nome é solicitado.

    @return JSON Retorna um objeto JSON contendo o nome da receita. Se a receita não for encontrada, retorna um erro com status 404.

    @par Exemplo de como utilizar este endpoint:
    \verbatim
        curl -X POST http://127.0.0.1:5000/recipe/62/name
    \endverbatim
    
    @retval JSON Exemplo de uma resposta bem-sucedida:
    @code
        {
            "recipe_name": "Amêijoas à Bulhãoo Pato"
        }
    @endcode
    
    @retval JSON Exemplo de uma resposta mal-sucedida:
    @code
        {
            "recipe_name": "Recipe not found"
        }
    @endcode
    
    @see recipedb_queries.getRecipeName(`recipe_id`)
    """
    recipe_name = db.getRecipeName(recipe_id)
    if recipe_name:
        return jsonify({'recipe_name': recipe_name})
    else:
        return jsonify({'error': 'Recipe not found'}), 404

# ----------------------------------------------------------------------------------------- > FETCH RECIPE IMAGE
@app.route('/recipe/<int:recipe_id>/image', methods=['GET'])
def fetch_recipe_image(recipe_id):
    """
    @brief Obtém a URL da imagem para uma dada ID de receita.

    @details Este endpoint é usado para obter a URL da imagem associada a uma receita específica, utilizando a função `getImg_url(recipe_id)` do módulo `recipedb_queries`. Se a imagem estiver disponível, a URL é retornada, caso contrário, retorna um erro indicando que a imagem não foi encontrada.

    @param recipe_id A ID da receita cuja imagem é solicitada.

    @return JSON Retorna um objeto JSON contendo a URL da imagem ou um erro se a imagem não for encontrada.

    @par Exemplo de como utilizar este endpoint:
    \verbatim
        curl -X POST http://127.0.0.1:5000/recipe/62/image
    \endverbatim
    
    @retval JSON Exemplo de uma resposta bem-sucedida:
    @code
        {
            "img_url": "https://www.saborintenso.com/attachments/videos-entradas-petiscos/240d1246564553-ameijoas-bulhao-pato-ameijoas-bulhao-pato-1.jpg"
        }
    @endcode
    
    @retval JSON Exemplo de uma resposta mal-sucedida:
    @code
        {
            "img_url": "Image not found for the specified recipe"
        }
    @endcode
    
    @see recipedb_queries.getImg_url(`recipe_id`)
    """
    img_url = db.getImg_url(recipe_id)
    if img_url:
        return jsonify({'img_url': img_url})
    else:
        return jsonify({'error': 'Image not found for the specified recipe'}), 404

# ----------------------------------------------------------------------------------------- > CONVERT TEXT NUMBERS TO DIGITS    
@app.route('/convert-text', methods=['POST'])
def convert_text():
    """
    @brief Converte texto contendo números por extenso para dígitos.

    @details Este endpoint processa texto recebido em JSON, utilizando a função `extract_and_convert_numeric_phrases` do módulo `convert_numbers_to_digit`, para converter números por extenso e unidades de medida em seu texto correspondente em dígitos.

    @return JSON Retorna um objeto JSON com o texto convertido ou um erro se a conversão falhar.
    
    @par Exemplo de como utilizar este endpoint:
    \verbatim
        curl -X POST http://127.0.0.1:5000/convert-text \         
            -H "Content-Type: application/json" \
            -d '{"text": "Tenho quarenta e três kg de porco"}'
    \endverbatim
    
    @retval JSON Exemplo de uma resposta bem-sucedida:
    @code
        "Tenho 43 kg de porco" 
    @endcode
    
    @exception Retorna um erro se o texto não for fornecido ou se houver falha na conversão.
    
    @see convert_numbers_to_digit.extract_and_convert_numeric_phrases(`text`)
    """
    if not request.json or 'text' not in request.json:
        return jsonify({'error': 'Request must be JSON and contain a "text" field.'}), 400

    text_to_convert = request.json['text']
    
    # Use the conversion function from your module
    converted_text = convert.extract_and_convert_numeric_phrases(text_to_convert)
    
    if converted_text is not None:
        response =  jsonify(converted_text)
        response.data = json.dumps(converted_text, ensure_ascii=False)  # Use ensure_ascii=False
        print(response)
        return response
    else:
        return jsonify({'error': 'Failed to convert text.'}), 500

# ----------------------------------------------------------------------------------------- > FORMAT DATE
@app.route('/format-date', methods=['POST'])
def format_date():
    """
    @brief Formata uma data fornecida para o padrão ISO 8601.

    @details Recebe uma data em texto através de um pedido JSON e utiliza a função `parse_date` do módulo `format_date` para converter a data para o formato ISO 8601.

    @return JSON Retorna a data formatada em JSON ou um erro se a formatação falhar.

    @par Exemplo de como utilizar este endpoint:
    \verbatim
        curl -X POST http://127.0.0.1:5000/format-date \
        -H "Content-Type: application/json" \
        -d '{"text": "25 de Maio de 2050"}'
    \endverbatim
    
    @retval JSON Exemplo de uma resposta bem-sucedida:
    @code
        "2050-05-25"
    @endcode
    
    @retval JSON Exemplo de uma resposta mal-sucedida:
    @code
        {
            "error": "Failed to format date."
        }
    @endcode
    
    @see format_date.parse_date(`date`)
    """
    if not request.json or 'text' not in request.json:
        return jsonify({'error': 'Request must be JSON and contain a "date" field.'}), 400

    date_to_format = request.json['text']
    print("DATE TO FORMAT: " + date_to_format)
    
    # Use the format_date function from your module
    formatted_date = fd.parse_date(date_to_format)
    print("FORMATED DATE: " + formatted_date)
    
    if formatted_date != "Invalid date format":
        return jsonify(formatted_date)
    else:
        return jsonify({'error': 'Failed to format date.'}), 500

# ----------------------------------------------------------------------------------------- > FETCH INGRIDIENT FROM A SENTENCE
@app.route('/get-ingredient', methods=['POST'])
def get_ingredient():
    """
    @brief Obtém um ingrediente de uma frase fornecida.

    @details Este endpoint analisa uma frase recebida via JSON para identificar e extrair um ingrediente utilizando a função `get_ingredient` do módulo `get_product`.

    @return JSON Retorna o ingrediente identificado ou um erro se não conseguir identificar.
    
    @par Exemplo de como utilizar este endpoint:
    \verbatim
        curl -X POST http://127.0.0.1:5000/get-ingredient \
        -H "Content-Type: application/json" \
        -d '{"sentence": "adiciona 5 kg de massa"}'
    \endverbatim

    @retval JSON Exemplo de uma resposta bem-sucedida:
    @code
        {
            "message": "massa"
        }
    @endcode
    
    @retval JSON Exemplo de uma resposta mal-sucedida:
    @code
        {
            "message": null
        }
    @endcode
    
    @note We are using this because RASA wasnt working as expected, and in order to get the unit of a product we need to use this endpoint.
    
    app.get_product.get_ingredient(`sentence`)
    """
    lista = []
    data = request.json
    
    sentence = data.get('sentence')
    print(sentence)
    sentence = sentence.lower()
    
    if not sentence:
        return jsonify({'error': 'Missing required fields.'}), 400
    
    try:
        wanted_ingridient = gp.get_ingredient(sentence)
        return jsonify({'message': wanted_ingridient}), 200
    except Exception as e:
        return jsonify({'error': f'Failed to get ingridient: {e}'}), 500
    
# ----------------------------------------------------------------------------------------- > FETCH UNIT FROM A SENTENCE
@app.route('/get-unit', methods=['POST'])
def get_unit():
    """
    @brief Obtém uma unidade de uma frase fornecida.
    
    @details Este endpoint analisa uma frase recebida via JSON para identificar e extrair uma unidade utilizando a função `get_unit` do módulo `get_product`.
    
    @return JSON Retorna a unidade identificada ou um erro se não conseguir identificar.
    
    @par Exemplo de como utilizar este endpoint:
    \verbatim
        curl -X POST http://127.0.0.1:5000/get-unit \      
        -H "Content-Type: application/json" \
        -d '{"sentence": "adiciona 5 kg de massa"}'
    \endverbatim
    
    @retval JSON Exemplo de uma resposta bem-sucedida:
    @code
        {
            "message": "kg"
        }
    @endcode
    
    @retval JSON Exemplo de uma resposta mal-sucedida:
    @code
        {
            "message": null
        }
    @endcode
    
    @note We are using this because RASA wasnt working as expected, and in order to get the unit of a product we need to use this endpoint.
    
    @see get_product.get_unit(`sentence`)
    """
    lista = []
    data = request.json
    
    sentence = data.get('sentence')
    print(sentence)
    sentence = sentence.lower()
    
    if not sentence:
        return jsonify({'error': 'Missing required fields.'}), 400
    
    try:
        wanted_unit = gp.get_unit(sentence)
        return jsonify({'message': wanted_unit}), 200
    except Exception as e:
        return jsonify({'error': f'Failed to get unit: {e}'}), 500

# ----------------------------------- > [ PANTRY DATABASE -> ENDPOINTS]

# ----------------------------------------------------------------------------------------- > INSERT PRODUCT INTO PANTRY
@app.route('/pantry/insert-stock', methods=['POST'])
def insert_stock():
    """
    @brief Insere um produto na despensa.
    
    @details Este endpoint insere um produto na despensa utilizando os dados fornecidos no corpo do pedido JSON.
    Os dados necessários são o nome do produto, a quantidade, a unidade e a data de validade.
    A função chama a função `insertStock(name, quantity, unit, expiration_date)` do módulo `pantrydb_queries` para inserir o produto na base de dados.
    
    @return JSON Retorna uma mensagem de sucesso ou um erro se a inserção falhar.
    
    @par Exemplo de como utilizar este endpoint:
    \verbatim
        curl -X POST http://127.0.0.1:5000/pantry/insert-stock \
        -H "Content-Type: application/json" \
        -d '{
            "name": "Azeite",
            "quantity": "1",
            "unit": "l",
            "expiration_date": "2024-04-23"
        }'
    \endverbatim
    
    @retval JSON Exemplo de uma resposta bem-sucedida:
    @code
        {
            "message": "Stock inserted successfully."
        }
    @endcode
    
    @retval JSON Exemplo de uma resposta mal-sucedida:
    @code
        {
            "error": "Failed to insert stock: <error message>"
        }
    @endcode
    
    @note Se algum dos campos obrigatórios estiver em falta, o endpoint retorna um erro com status 400.
    
    @see pantrydb_queries.insertStock(`name`, `quantity`, `unit`, `expiration_date`)
    """   
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
    """
    @brief Remove um produto da despensa.
    
    @details Este endpoint remove um produto da despensa utilizando os dados fornecidos no corpo do pedido JSON.
    Os dados necessários são o nome do produto, a quantidade e a unidade.
    A função chama a função `removeStock(name, quantity, unit)` do módulo `pantrydb_queries` para remover o produto da base de dados.
    
    @return JSON Retorna uma mensagem de sucesso ou um erro se a remoção falhar.
    
    @par Exemplo de como utilizar este endpoint:
    \verbatim
        curl -X POST http://127.0.0.1:5000/pantry/remove-stock \
        -H "Content-Type: application/json" \
        -d '{
            "name": "Azeite",
            "quantity": "1",
            "unit": "l",
            "expiration_date": "2024-04-23"
        }'
    \endverbatim
    
    @retval JSON Exemplo de uma resposta bem-sucedida:
    @code
        {
            "message": "Stock removed successfully."
        }
    @endcode
    
    @retval JSON Exemplo de uma resposta mal-sucedida:
    @code
        {
            "error": "Failed to remove stock: <error message>"
        }
    @endcode
    
    @note Se algum dos campos obrigatórios estiver em falta, o endpoint retorna um erro com status 400.
    
    @see pantrydb_queries.removeStock(`name`, `quantity`, `unit`)
    """
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
    """
    @brief Obtém todos os produtos na despensa.
    
    @details Este endpoint recupera todos os produtos na despensa chamando a função `getStockDetails()` do módulo `pantrydb_queries`.
    
    @return JSON Retorna uma lista de produtos na despensa.
    
    @par Exemplo de como utilizar este endpoint:
    \verbatim
        curl -X GET http://127.0.0.1:5000/pantry/stock
    \endverbatim
    
    @retval JSON Exemplo de uma resposta bem-sucedida:
    @code
        [
            "Arroz 3.0 kg, Data de Validade : 2025/08/07",
            "Bacalhau 1.0 kg, Data de Validade : 2025/09/27",
            "Bananas 2.0 kg, Data de Validade : 2025/11/01",
            "bife de vaca 2.0 kg, Data de Validade : 2025/08/24",
            ...
        ]
    @endcode
    
    @note Se a despensa estiver vazia, o endpoint retorna uma lista vazia.
    
    @see pantrydb_queries.getStockDetails()
    """
    pantry_list = pdb.getStockDetails()
    return jsonify(pantry_list)

# ----------------------------------------------------------------------------------------- > REMOVE ALL <GIVEN PRODUCT> FROM PANTRY
@app.route('/pantry/remove-all-stock/<name>', methods=['DELETE'])
def remove_all_stock(name):
    """
    @brief Remove todos os produtos de um determinado tipo da despensa.
    
    @details Este endpoint remove todos os produtos de um determinado tipo da despensa, utilizando o nome do produto fornecido no URL.
    A função chama a função `removeAllStock(name)` do módulo `pantrydb_queries` para remover todos os produtos do tipo especificado da base de dados.
    
    @param name O nome do produto a ser removido da despensa.
    
    @return JSON Retorna uma mensagem de sucesso ou um erro se a remoção falhar.
    
    @par Exemplo de como utilizar este endpoint:
    \verbatim
        curl -X DELETE http://127.0.0.1:5000/pantry/remove-all-stock/azeite
    \endverbatim
    
    @retval JSON Exemplo de uma resposta bem-sucedida:
    @code
        {
            "message": "Removed all stock details for 'azeite' from stock_details."
        }
    @endcode
    
    @retval JSON Exemplo de uma resposta mal-sucedida:
    @code
        {
            "message": "Stock item 'aze' does not exist in the database."
        }
    @endcode
    
    @see pantrydb_queries.removeAllStock(`name`)
    """
    try:
        result = pdb.removeAllStock(name)
        return jsonify({'message': result}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ----------------------------------------------------------------------------------------- > CLEAR PANTRY
@app.route('/pantry/clear', methods=['DELETE'])
def clear_pantry():
    """
    @brief Limpa a despensa.
    
    @details Este endpoint limpa a despensa, removendo todos os produtos da base de dados.
    A função chama a função `clearStock()` do módulo `pantrydb_queries` para limpar a base de dados.
    
    @return JSON Retorna uma mensagem de sucesso ou um erro se a limpeza falhar.
    
    @par Exemplo de como utilizar este endpoint:
    \verbatim
        curl -X DELETE http://127.0.0.1:5000/pantry/remove-all-stock/azeite
    \endverbatim
    
    @retval JSON Exemplo de uma resposta bem-sucedida:
    @code
        {
            "message": "Cleared all stock details from stock_details."
        }
    @endcode
    
    @retval JSON Exemplo de uma resposta mal-sucedida:
    @code
        {
            "error": ("Failed to clear all stock details from stock_details."
        }
    @endcode
    
    @see pantrydb_queries.clearStock()
    """
    try:
        result = pdb.clearStock()
        return jsonify({'message': result}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ----------------------------------------------------------------------------------------- > CHECK IF A <GIVEN PRODUCT> EXISTS IN GROCERY LIST
@app.route('/pantry/check-grocery/<product_name>', methods=['GET'])
def check_grocery(product_name):
    """
    @brief Verifica se um produto existe na lista de compras.
    
    @details Este endpoint verifica se um produto existe na lista de compras, utilizando o nome do produto fornecido na URL.
    A função chama a função `checkGrocery(product_name)` do módulo `pantrydb_queries` para verificar se o produto existe na base de dados.
    
    @param product_name O nome do produto a ser verificado na lista de compras.
    
    @return JSON Retorna uma mensagem de sucesso ou um erro se a verificação falhar.
    
    @par Exemplo de como utilizar este endpoint:
    \verbatim
        curl -X GET http://127.0.0.1:5000/pantry/check-grocery/vinho
    \endverbatim
    
    @retval JSON Exemplo de uma resposta bem-sucedida:
    @code
        {
            "message": "0 None"
        }
    @endcode
    
    @retval JSON Exemplo de uma resposta mal-sucedida:
    @code
        {
            "message": "No stock found for 'vinhos'."
        }
    @endcode
    
    @note Esta implementado a possibilidade de retornar o valor do produto. De momento apenas temos a lista de compras(base de dados) com nome do produto mas temos a possibilidade de retornar o valor do produto também.
    
    @see pantrydb_queries.checkGrocery(`product_name`)
    """
    try:
        result = pdb.searchStock(product_name)
        return jsonify({'message': result}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500



# ----------------------------------- > [ SHOPPING LIST DATABASE -> ENDPOINTS]

# ----------------------------------------------------------------------------------------- > ADD PRODUCT INTO GROCERY LIST
@app.route('/pantry/insert-grocery', methods=['POST'])
def insert_grocery():
    """
    @brief Insere um produto na lista de compras.
    
    @details Este endpoint insere um produto na lista de compras utilizando os dados fornecidos no corpo do pedido JSON.
    Os dados necessários são o nome do produto.
    A função chama a função `insertGrocery(name)` do módulo `pantrydb_queries` para inserir o produto na base de dados.
    
    @return JSON Retorna uma mensagem de sucesso ou um erro se a inserção falhar.
    
    @par Exemplo de como utilizar este endpoint:
    \verbatim
        curl -X POST http://127.0.0.1:5000/pantry/insert-grocery \
        -H "Content-Type: application/json" \
        -d '{"name": "azeite"}'
    \endverbatim
    
    @retval JSON Exemplo de uma resposta bem-sucedida:
    @code
        {
            "message": " Stock item 'azeite' inserted successfully in the GROCERY LIST."
        }
    @endcode
    
    @retval JSON Exemplo de uma resposta mal-sucedida:
    @code
        {
            "error": "Missing required field: \"name\"."
        }
    @endcode
    
    @note Se algum dos campos obrigatórios estiver em falta, o endpoint retorna um erro com status 400.
    
    @see pantrydb_queries.insertGrocery(`name`)    
    """
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
    """
    @brief Remove um produto da lista de compras.
    
    @details Este endpoint remove um produto da lista de compras utilizando os dados fornecidos no corpo do pedido JSON.
    Os dados necessários são o nome do produto.
    A função chama a função `removeGrocery(name)` do módulo `pantrydb_queries` para remover o produto da base de dados.
    
    @return JSON Retorna uma mensagem de sucesso ou um erro se a remoção falhar.
    
    @par Exemplo de como utilizar este endpoint:
    \verbatim
        curl -X DELETE http://127.0.0.1:5000/pantry/remove-grocery \
        -H "Content-Type: application/json" \
        -d '{"name": "azeite"}'
    \endverbatim
    
    @retval JSON Exemplo de uma resposta bem-sucedida:
    @code
        {
            "message": "Stock item 'azeite' removed successfully from the GROCERY LIST."
        }
    @endcode
    
    @note Se algum dos campos obrigatórios estiver em falta, o endpoint retorna um erro com status 400.
    
    @see pantrydb_queries.removeGrocery(`name`)
    """
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
    """
    @brief Obtém todos os produtos na lista de compras.
    
    @details Este endpoint recupera todos os produtos na lista de compras chamando a função `showAllGrocery()` do módulo `pantrydb_queries`.
    
    @return JSON Retorna uma lista de produtos na lista de compras.
    
    @par Exemplo de como utilizar este endpoint:
    \verbatim
        curl -X GET http://127.0.0.1:5000/pantry/shopping-list
    \endverbatim
    
    @retval JSON Exemplo de uma resposta bem-sucedida:
    @code
        [
            "Arroz",
            "Bacalhau",
            "Bananas",
            "Bife de vaca",
            ...
        ]
    @endcode
    
    @note Se a lista de compras estiver vazia, o endpoint retorna uma lista vazia.
    
    @see pantrydb_queries.showAllGrocery()
    """
    try:
        grocery_list = pdb.showAllGrocery()
        return jsonify(grocery_list), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ----------------------------------------------------------------------------------------- > CLEAR GROCERY LIST
@app.route('/pantry/clear-grocery', methods=['DELETE'])
def clear_grocery():
    """
    @brief Limpa a lista de compras.
    
    @details Este endpoint limpa a lista de compras, removendo todos os produtos da base de dados.
    A função chama a função `clearGrocery()` do módulo `pantrydb_queries` para limpar a base de dados.
    
    @return JSON Retorna uma mensagem de sucesso ou um erro se a limpeza falhar.
    
    @par Exemplo de como utilizar este endpoint:
    \verbatim
        curl -X GET http://127.0.0.1:5000/pantry/clear-grocery
    \endverbatim
    
    @retval JSON Exemplo de uma resposta bem-sucedida:
    @code
        {
            "message": "Cleared all stock details from grocerylist."
        }
    @endcode
    
    @retval JSON Exemplo de uma resposta mal-sucedida:
    @code
        {
            "error": "Failed to clear all stock details from grocerylist."
        }
    @endcode
    
    @see pantrydb_queries.clearGrocery()
    """
    try:
        result = pdb.clearGrocery()
        return jsonify({'message': result}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500



# ----------------------------------- > [ BARCODE -> ENDPOINTS]

# ----------------------------------------------------------------------------------------- > GET PRODUCT NAME, QUANTITY AND UNIT FROM BARCODE
@app.route('/scanner', methods=['POST'])
def get_product_barcode():
    """
    @brief Obtém o nome, a quantidade e a unidade de um produto a partir de um código de barras.
    
    @details Este endpoint recebe um código de barras de um produto e chama a função `get_product_name(product_barcode)` do módulo `api_operations` para obter o nome, a quantidade e a unidade do produto.
    
    @return JSON Retorna o nome, a quantidade e a unidade do produto ou um erro se o produto não for encontrado.
    
    @par Exemplo de como utilizar este endpoint:
    \verbatim
        curl -X POST http://
    \endverbatim
    
    @retval JSON Exemplo de uma resposta bem-sucedida:
    @code
        "Código de barras do produto: {barcode}"
    @endcode
    
    @note Se o produto não for encontrado, o endpoint retorna um erro com status 404.
    
    @see api_operations.get_product_name(`product_barcode`)
    """
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
    """
    @brief Envia um email utilizando os dados fornecidos.
    
    @details Este endpoint envia um email utilizando os dados fornecidos no corpo do pedido JSON.
    Os dados necessários são o endereço de email do remetente, o endereço de email
    do destinatário, o assunto, o corpo do email, o servidor SMTP, a porta SMTP e a senha.
    A função chama a função `send_email(from_addr, to_addr, subject, body, smtp_server, smtp_port, password)` do módulo `email_service` para enviar o email.
    
    @return JSON Retorna uma mensagem de sucesso ou um erro se o envio falhar.
    
    @par Exemplo de como utilizar este endpoint:
    \verbatim
        curl -X POST http://127.0.0.1:5000/send-email \
        -H "Content-Type: application/json" \
        -d '{
            "from_addr": "kitchen_assistant@outlook.com",
            "to_addr": "<EMAIL PARA ONDE ENVIAR>",
            "subject": "Aviso de Produtos Próximos da Data de Expiração",
            "body": "This is a test email sent from the Flask application.",
            "smtp_server": "smtp-mail.outlook.com",
            "smtp_port": 587,
            "password": "<PASSWORD DO EMAIL : kitchen_assistant@outlook.com >"
        }'
    \endverbatim
    
    @retval JSON Exemplo de uma resposta bem-sucedida:
    @code
        {
            "message": "Email sent successfully."
        }
    @endcode
    
    @retval JSON Exemplo de uma resposta mal-sucedida:
    
    @note Se algum dos campos obrigatórios estiver em falta, o endpoint retorna um erro com status 400.
    
    @see email_service.send_email(`from_addr`, `to_addr`, `subject`, `body`, `smtp_server`, `smtp_port`, `password`)
    """
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
    """
    @brief Função principal que inicia o servidor Flask.
    
    @details Este bloco de código verifica se o módulo é o módulo principal sendo executado,
    isto é, não está sendo importado. Se for o caso, o servidor Flask é iniciado
    com a configuração de depuração ativada no porto 5000. Isso permite que o servidor
    reinicie automaticamente a cada mudança no código e forneça informações de depuração detalhadas.
    
    Utilizar o modo de depuração em ambiente de produção não é recomendado devido a questões de segurança.
    
    @par Exemplo de como utilizar este endpoint:
    \verbatim
        python app.py
    \endverbatim
    
    @note A configuração do servidor pode ser ajustada conforme a necessidade do ambiente,
    modificando os parâmetros dentro do método app.run().
    
    @par Comandos para iniciar o servidor:
    @code
        if __name__ == '__main__':
            app.run(debug=True, port=5000)
    @endcode
    
    """
    app.run(debug=True, port=5000)
    
    