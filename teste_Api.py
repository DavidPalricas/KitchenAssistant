import requests

  #Link da documentação da API: https://spoonacular.com/food-api/docs

API_KEY = "ef6f2279b7864bad8ff9a04de2180657"





def Recipe_instructions(recipe):
    equipaments = []
    oven = False
    ingredients = []
    recipe_id = recipe[1]
    query_recipe_info = f"https://api.spoonacular.com/recipes/{recipe_id}/analyzedInstructions?apiKey={API_KEY}"
    response_info = requests.get(query_recipe_info) #Informações da receita selecionada
                                                    #Contém os passos , o número de cada passo, ingredientes e equipamentos necessários
                  
    
    if response_info.json() == []: #Se a receita não tiver informação sobre os passos, ingredientes e equipamentos necessários
        print("Informação da receita indisponível")
        print("Programa terminado")
        exit(1)

    for steps in response_info.json():
        for step in steps["steps"]:
            print(f"\tPasso nº{step['number']} : {step['step']}")
            if step["equipment"] == []:
                print("Não existe informação sobre equipamentos necessários")
            else:
         
               for equipament in step["equipment"]:
                   equipaments.append(equipament["name"])
                   if equipament["name"] == "oven":
                       oven = True
    
               print(f"Equipamentos: {equipaments}")
         
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

            print("\n")
    


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
            if recipe_number < 0 or recipe_number >= len(recipes):
                print("Número inválido, tente novamente")
            else:
                break
        except ValueError:
            print("Dado inválido, tente novamente")
            print("Digite o número da receita desejada: ")
 
    return recipes[recipe_number]


def Number_of_recipes():
    while True:
        try:
            print("Digite o número de receitas que deseja ver: ")
            number_recipes = int(input())
            if number_recipes < 1 or number_recipes > 100:
                print("Número inválido, tente novamente")
            else:
                break
        except ValueError:
            print("Dado inválido, tente novamente")
    
    return number_recipes

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
    random = True #Variável que indica se a dá receitas aleatórias ou não
                  #Considerei verdadeira para que o utilizador não receba sempre as mesmas receitas

    while True:
        try:
            print("Digite o número mínimo de calorias: ")
            min_calories = int(input())
            print("Digite o número máximo de calorias: ")
            max_calories = int(input())
            if min_calories < 0  or max_calories < 0:
                print("Número inválido, tente novamente")
            else:
                 break
        except ValueError:
            print("Dado inválido, tente novamente")
    
    number_recipes = Number_of_recipes()

    return f"&minCalories={min_calories}&maxCalories={max_calories}&number={number_recipes}&random={random}" #query_params

  
def Category():
    categories = {"Ingredientes": 0,"Calorias":1}
    print("Escolha uma categoria para pesquisar a receita: ")
    for category in categories:
        print(f"{categories[category]} : {category}")

    user_choice = int(input())


    while True:
        try:
            if user_choice == 0 or user_choice == 1:
                break
            else:
                print("Opção inválida, tente novamente")
                user_choice = int(input())

        except ValueError:
            print("Dado inválido, tente novamente")
            print("Escolha uma categoria para pesquisar a receita: ")
            
    if user_choice == 0:
        query_params = Ingredients()
    else:
        query_params = Calories()


    for category in categories:
        if categories[category] == user_choice:
            tag = category
    
    return tag,query_params

def Query():
    recipes = []
  
    tag,query_params = Category()


    if tag == "Ingredientes":
        query = f"https://api.spoonacular.com/recipes/findByIngredients?apiKey={API_KEY}" + query_params
    else:
        query = f"https://api.spoonacular.com/recipes/findByNutrients?apiKey={API_KEY}" + query_params

    response = requests.get(query) #Lista de receitas e suas informações



    if response.json() == []:
        print("Nenhuma receita encontrada")
        print("Tente novamente\n")
        Query() 


     

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
    Recipe_instructions(recipe)
    
   
    
if __name__ == "__main__":
    main()