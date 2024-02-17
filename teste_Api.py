import requests
import random

  #Link da documentação da API: https://spoonacular.com/food-api/docs

API_KEY = "ef6f2279b7864bad8ff9a04de2180657"
RANDOM = True #Variável que indica se a dá receitas aleatórias ou não
                  #Considerei verdadeira para que o utilizador não receba sempre as mesmas receitas
MAX_CALORIES = 1286 #Número máximo de calorias que econtrei por engenharia reversa

MAX_OFFSET = 900 #Número máximo de skips que a API permite


def Show(image,meal_type,Ingredients,description,equipments):
    print(f"Imagem da receita: {image}\n")
    print(f"Tipo de refeição: {meal_type}\n")
    print(f"Ingredientes necessários para a receita: {Ingredients}\n")
    print(f"Todos os passos da receita : {description}\n")
    print(f"Todos os equipamentos necessário para a receita : {equipments}\n")



def Get_and_Show_Recipe_instructions(recipe):
    description = {} #Dicionário com o número do passo e a descrição do passo
    all_equipaments = set() #Conjunto com todos os equipamentos necessários para a receita
   
    equipaments = [] #Lista com os equipamentos necessários para cada passo da receita
    oven = False
    ingredients = [] #Lista com os ingredientes necessários para cada passo da receita
    recipe_id = recipe[1]
    query = f"https://api.spoonacular.com/recipes/{recipe_id}/analyzedInstructions?apiKey={API_KEY}"
    response_info = requests.get(query) #Informações da receita selecionada
                                                    #Contém os passos , o número de cada passo, ingredientes e equipamentos necessários
                  
    
    if response_info.json() == []: #Se a receita não tiver informação sobre os passos, ingredientes e equipamentos necessários
        print("Informação da receita indisponível")
        print("Programa terminado")
        exit(1)

    for steps in response_info.json():
        for step in steps["steps"]:
            print(f"\tPasso nº{step['number']} : {step['step']}")

            description[f"Passo nº {step['number']}"] = step["step"] #Dicionário com o número do passo e a descrição do passo

            if step["equipment"] == []:
                print("Não existe informação sobre equipamentos necessários")
            else:
         
               for equipament in step["equipment"]:
                   equipaments.append(equipament["name"]) #Adiciona o equipamento à lista de equipamentos necessários para o passo
                   all_equipaments.add(equipament["name"]) #Adiciona o equipamento ao conjunto de  todos equipamentos  necessários para a receita
                   if equipament["name"] == "oven":
                       oven = True
    
               print(f"Equipamentos: {equipaments}")
               equipaments = [] #Reinicia a lista de equipamentos para o próximo passo da receita
         
               if "temparture" in step and oven == True:  #Notei nos exemplos da documentação que o forno pode ter especificações próprias
                   print("Configurações do forno")  
                   degrees = step["temperature"]["number"]
                   if step["unit"] == "Fahrenheit":
                       degrees = (degrees - 32) * 5/9 #Conversão de Fahrenheit para Celsius
                       
                   print(f"Temperatura: {degrees} Cº") #Temperatura do forno e unidades
            
            if step["ingredients"] == []:
                print("Não existe informação sobre ingredientes")
            else:
                for ingredient in step["ingredients"]:
                    ingredients.append(ingredient["name"])
                print(f"Ingredientes: {ingredients}")
                ingredients = [] #Reinicia a lista de ingredientes para o proíxmo passso da receita


            print("\n")

    return description,all_equipaments
        
    
def Get_Recipe_information(recipe_id):
    Ingredients_info= {} #Dicionário com os ingredientes e as quantidades necessárias para a receita
    query = f"https://api.spoonacular.com/recipes/{recipe_id}/information?apiKey={API_KEY}"
    response = requests.get(query) #Informações da receita selecionada

    if response.json() == []: #Se a receita não tiver informação sobre os ingredientes necessários
        print("Informação da receita indisponível")
        print("Programa terminado")
        exit(1)
    
    image = response.json()["image"] # Url da imagem da receita

    meal_type = response.json()["dishTypes"] #Tipo de refeição


    for ingredient in response.json()["extendedIngredients"]:
        Ingredients_info[ingredient["name"]] = f"Quantidade {ingredient['measures']['metric']['amount']} {ingredient['measures']['metric']['unitShort']}"




    return image,meal_type,Ingredients_info
        


def Ask_for_recipe(tag,recipes):
    if tag == "Calorias":
        recipes.sort(key = lambda c: c[2]) #Ordena as receitas por ordem crescente de calorias

    print("Digite o número da receita desejada: ")
    if tag == "Calorias":
        for i in range(0,len(recipes)):
            print(f"{i+1} : {recipes[i][0]} (Calorias: {recipes[i][2]})")
    else:
        for i in range(0,len(recipes)):
            print(f"{i+1} : {recipes[i][0]}") #Mostra o nome das receitas
    
    while True:
        try:
            recipe_number = int(input())
            if recipe_number < 0 or recipe_number > len(recipes):
                print("Número inválido, tente novamente")
            else:
                break
        except ValueError:
            print("Dado inválido, tente novamente")
            print("Digite o número da receita desejada: ")
 
    return recipes[recipe_number-1]


def Number_of_recipes():
    while True:
        try:
            print("\033[91m\tAVISO!\033[0m")
            print("1. O número de receitas máximo e receitas é 100 e o número mínimo é 1")
            print("Digite o número de receitas que deseja ver: ")
         
            number_recipes = int(input())
            if number_recipes < 1 or number_recipes > 100:
                print("Número inválido, tente novamente")
            else:
                break
        except ValueError:
            print("Dado inválido, tente novamente")
    
    return number_recipes

def Meal_type():
    meal_type = ["main course","side dish","dessert","appetizer","salad","bread","breakfast","soup","beverage","sauce","marinade","fingerfood","snack","drink"]

    print("\033[91m\tAVISOS!\033[0m")
    print("1. O tipo de refeições têm de ser escritos em inglês (Fase de teste)")
    print("2. Os tipos de refeições suportados")
    for meal in meal_type:
        print(f"\t.{meal}")

    print("Digite o tipo de refeição que deseja pesquisar: ")

    while True:
        try:
            meal = input()
            if meal.lower() not in meal_type:
                print("Tipo de refeição inválido, tente novamente")
            else:
                break
        except ValueError:
            print("Dado inválido, tente novamente")
            print("Digite o tipo de refeição que deseja pesquisar: ")

    number_recipes = Number_of_recipes()

        #Como neste tipo de pesquisa não existe o parãmetro random, decidi adicionar um offset aleatório
        #para que o utilizador não receba sempre as mesmas receitas
    offset = random.randint(0,MAX_OFFSET) #Número aleatório entre 0 e 900
    return f"&type={meal}&number={number_recipes}&offset={offset}" #query_params
    

def Random():
    offset = random.randint(0,MAX_OFFSET) #Número aleatório entre 0 e 900
    number_recipes = Number_of_recipes()

    return f"&number={number_recipes}&offset={offset}" #query_params


def Ingredients():
    query_params = "&ingredients="
    ingredients = []
    ingredient_counter = 1
    ignorePantry = True #Variável que permite ignorar os itens típicos de uma despensa, como sal, açúcar, pimenta, etc na pesquisa de receitas
    print("\033[91m\tAVISOS!\033[0m")
    print("1. Os ingredientes têm de ser escritos em inglês (Fase de teste)")
    print("2. Itens típicos de uma despensa, como sal, açúcar, pimenta, etc, não são considerados nesta pesquisa de receitas,escusa de indicá-los.\n")

    print("Digite os  ingrediente, quando quiser terminar digite 'parar':") #Os ingredientes têm de ser escritos em inglês

    while True:
        try:
            print(f"Ingrediente nº{ingredient_counter}: ")
            ingredient = input()
            if ingredient.lower() == "parar":
                break
            else:
                ingredients.append(ingredient.lower())
                ingredient_counter += 1
        except ValueError:
            print("Dado inválido, tente novamente")
            print(f"Ingrediente nº{ingredient_counter}: ")
        
        for i in range(0,len(ingredients)):
            if  i == 0:
                query_params += ingredients[i] #Primeiro ingrediente
            else:
                query_params += f",+{ingredients[i]}" #Restantes ingredientes tem de ser separados por uma vírgula e um sinal de adição
    
    number_recipes = Number_of_recipes()
    return query_params + f"&number={number_recipes}&ignorePantry={ignorePantry}" 


def Calories():
    while True:
        try:
            print("Digite o número mínimo de calorias: ")
            min_calories = int(input())
           
            
            print("Digite o número máximo de calorias: ")
            max_calories = int(input())
            if min_calories < 0  or max_calories < 0 or max_calories > MAX_CALORIES or min_calories >= MAX_CALORIES:
                print("Número inválido, tente novamente")
            elif min_calories >= max_calories:
                print("Os números de calorias mínimimo têm de ser menor ou diferentes do valor máximo, tente novamente")
            else:
                 break
        except ValueError:
            print("Dado inválido, tente novamente")
    
    number_recipes = Number_of_recipes()

    return f"&minCalories={min_calories}&maxCalories={max_calories}&number={number_recipes}&random={RANDOM}" #query_params

  
def Category():
    categories = {"Ingredientes": 1,"Calorias":2,"Receitas aleatórias":3,"Tipo de refeição":4}
    print("Escolha uma categoria para pesquisar a receita: ")
    for category in categories:
        print(f"{categories[category]} : {category}")

    user_choice = int(input())


    while True:
        try:
            if user_choice in range(1,len(categories) +1): #Se a escolha do utilizador estiver entre 1 e 2
                break
            else:
                print("Opção inválida, tente novamente")
                user_choice = int(input())

        except ValueError:
            print("Dado inválido, tente novamente")
            print("Escolha uma categoria para pesquisar a receita: ")
          

    match user_choice:
        case 1:
            query_params = Ingredients()
        case 2:
            query_params = Calories()
        case 3:
            query_params = Random()
        case 4:
            query_params = Meal_type()
    



    for category in categories:
        if categories[category] == user_choice:
            tag = category
    
    return tag,query_params

def Query():
    recipes = []
  
    tag,query_params = Category()


    if tag == "Ingredientes":
        query = f"https://api.spoonacular.com/recipes/findByIngredients?apiKey={API_KEY}" + query_params

    elif tag == "Calorias":
        query = f"https://api.spoonacular.com/recipes/findByNutrients?apiKey={API_KEY}" + query_params

    else:
        query = f"https://api.spoonacular.com/recipes/complexSearch?apiKey={API_KEY}" + query_params

    response = requests.get(query) #Lista de receitas e suas informações



    if response.json() == []:
        print("Nenhuma receita encontrada")
        print("Tente novamente\n")
        Query() 


    if tag== "Tipo de refeição" or tag == "Receitas aleatórias": #Pesquisas feita por ComplexSearch
        for recipe in response.json()["results"]: 
         recipes.append((recipe["title"],recipe["id"])) #Lista de tuplos com o nome e id da receita

    else:
        for recipe in response.json():
            if tag == "Calorias":
                recipes.append((recipe["title"],recipe["id"],recipe["calories"])) #Lista de tuplos com o nome e id da receita
            else:
                recipes.append((recipe["title"],recipe["id"])) #Lista de tuplos com o nome e id da receita



    return tag,recipes


def Status():
    query_base = f"https://api.spoonacular.com/recipes/complexSearch?apiKey={API_KEY}"
    response= requests.get(query_base)
    status = response.status_code
    if status== 200: #Código 200 indica que a conexão foi realizada com sucesso
        print("\033[92mConexão realizada com sucesso\033[0m\n") #Código de cor verde para indicar que a conexão foi realizada com sucesso
    else:
        print("\033[91mErro na conexão\033[0m") #Código de cor vermelha para indicar que houve um erro na conexão
        exit(1) #Encerra o programa com erro



def main():
    Status()
    tag,recipes = Query()
    recipe = Ask_for_recipe(tag,recipes)
    image,meal_type,Ingredients = Get_Recipe_information(recipe[1]) #Informações sobre a receita selecionada através do id da receita
    description,equipments = Get_and_Show_Recipe_instructions(recipe)

        #Função que mostra as informações da receita selecionada
        #É uma função de fase teste para ver as informações que vão ser armazenadas na base de dados
    Show(image,meal_type,Ingredients,description,equipments)


  
   
    
if __name__ == "__main__":
    main()