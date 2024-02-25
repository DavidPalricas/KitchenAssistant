# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from .consts import * # O "." é o caminho relativo para o arquivo consts.py
                                        # É necessário meter este "."  caso contrário o rasa não consegue encontrar o arquivo consts.py
import random
import requests



class ActionRandomRecipe(Action):
 
    def name(self) -> Text:
        return "action_random_recipe" 
    
    def Get_Recipe_instructions(self, recipe,api_key):
        description = {} #Dicionário com o número do passo e a descrição do passo
        all_equipaments = set() #Conjunto com todos os equipamentos necessários para a receita

        recipe_id = recipe[1]
        query = f"https://api.spoonacular.com/recipes/{recipe_id}/analyzedInstructions?apiKey={api_key}"
        response_info = requests.get(query) #Informações da receita selecionada
                                                    #Contém os passos , o número de cada passo, ingredientes e equipamentos necessários
                  
    
        if response_info.json() == []: #Se a receita não tiver informação sobre os passos, ingredientes e equipamentos necessários
         return None

        for steps in response_info.json():
            for step in steps["steps"]:
                description[f"Passo nº {step['number']}"] = step["step"] #Dicionário com o número do passo e a descrição do passo

          
                for equipament in step["equipment"]:                   
                    all_equipaments.add(equipament["name"]) #Adiciona o equipamento ao conjunto de  todos equipamentos  necessários para a receita
                    
        return description,all_equipaments
    

    def Get_Recipe_Info(self, recipe_id,api_key):
        ingredients_info = {}
        query = f"https://api.spoonacular.com/recipes/{recipe_id}/information?apiKey={api_key}"

        response = requests.get(query) #Informações da receita selecionada

        if response.json() == []: #Se a receita não tiver informação sobre os ingredientes necessários
            return None
    
        image = response.json()["image"] # Url da imagem da receita

        meal_type = response.json()["dishTypes"] #Tipo de refeição


        for ingredient in response.json()["extendedIngredients"]:
            ingredients_info[ingredient["name"]] = f"Quantidade {ingredient['measures']['metric']['amount']} {ingredient['measures']['metric']['unitShort']}"




        return image,meal_type,ingredients_info


    
    def Query(self, params,api_key):
         query = "https://api.spoonacular.com/recipes/complexSearch?apiKey=" + api_key + params
         response = requests.get(query)
         return response.json()
    
    def Random(self):
        offset = random.randint(0, MAX_OFFSET)
        number = 1 #Número de receitas que serão retornadas
        return f"&offset={offset}&number={number}"
    
    def Status(self,api_key):
        query_base = f"https://api.spoonacular.com/recipes/complexSearch?apiKey={api_key}"
        response= requests.get(query_base)
        status = response.status_code
        if status== 200: #Código 200 indica que a conexão foi realizada com sucesso
            print("\033[92mConexão realizada com sucesso\033[0m\n") #Código de cor verde para indicar que a conexão foi realizada com sucesso
        elif status == 402: #Código 402 indica que a chave de API atingiu o limite de uso
            i = API_KEYS.index(api_key)
            
            if i == len(API_KEYS)-1:
                return None
            else:
                api_key = API_KEYS[i+1] #Muda a chave de API
                self.Status(api_key) #Chama a função novamente para verificar se a nova chave de API está funcionando
        else:
            print("\033[91mErro na conexão\033[0m") #Código de cor vermelha para indicar que houve um erro na conexão
            api_key = None
            
        return api_key

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker, 
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
         
         api_key = API_KEYS[0]
         message = "Nehuma receita encontrada"
         api_key = self.Status(api_key)

         if api_key == None:
             message = "Erro na conexão"
             dispatcher.utter_message(text=message)
             return []
         

         params = self.Random() #Parâmetros da receita aleatória

         response = self.Query(params,api_key)

         if response == []:
            self.Random() #Se a API não retornar nenhuma receita, uma nova receita será selecionada
         

         for r in response["results"]:
             recipe = (r["title"], r["id"]) 
          
                

         if self.Get_Recipe_Info(recipe[1],api_key) == None or self.Get_Recipe_instructions(recipe,api_key) == None:
               self.Random() #Se a receita não tiver informações suficientes, uma nova receita será selecionada
         else:
                image,meal_type,ingredients_info = self.Get_Recipe_Info(recipe[1],api_key)
                description,all_equipaments = self.Get_Recipe_instructions(recipe,api_key)


                message = f"\tReceita: {recipe[0]}\n\n\nImagem: {image}\n\n\nTipo de refeição: {meal_type}\n\n\nIngredientes: {ingredients_info}\n\n\nPassos: {description}\n\n\nEquipamentos: {all_equipaments}"

         dispatcher.utter_message(text=message)
         return []





class ActionSpecifRecipe(Action):
     
        def name(self) -> Text:
            return "action_specific_recipe" 
        

        def Get_Recipe_instructions(self, recipe,api_key):
            description = {} #Dicionário com o número do passo e a descrição do passo
            all_equipaments = set() #Conjunto com todos os equipamentos necessários para a receita

            recipe_id = recipe[1]
            query = f"https://api.spoonacular.com/recipes/{recipe_id}/analyzedInstructions?apiKey={api_key}"
            response_info = requests.get(query) #Informações da receita selecionada
                                                        #Contém os passos , o número de cada passo, ingredientes e equipamentos necessários
                    
        
            if response_info.json() == []: #Se a receita não tiver informação sobre os passos, ingredientes e equipamentos necessários
                return None

            for steps in response_info.json():
                for step in steps["steps"]:
                    description[f"Passo nº {step['number']}"] = step["step"] #Dicionário com o número do passo e a descrição do passo

            
                    for equipament in step["equipment"]:                   
                        all_equipaments.add(equipament["name"]) #Adiciona o equipamento ao conjunto de  todos equipamentos  necessários para a receita
                        
            return description,all_equipaments
    

        def Get_Recipe_Info(self, recipe_id,api_key):
            ingredients_info = {}
            query = f"https://api.spoonacular.com/recipes/{recipe_id}/information?apiKey={api_key}"

            response = requests.get(query) #Informações da receita selecionada

            if response.json() == []: #Se a receita não tiver informação sobre os ingredientes necessários
                return None
        
            image = response.json()["image"] # Url da imagem da receita

            meal_type = response.json()["dishTypes"] #Tipo de refeição


            for ingredient in response.json()["extendedIngredients"]:
                ingredients_info[ingredient["name"]] = f"Quantidade {ingredient['measures']['metric']['amount']} {ingredient['measures']['metric']['unitShort']}"




            return image,meal_type,ingredients_info


        
        def Query(self, params,api_key,recipe_name):
            query = "https://api.spoonacular.com/recipes/complexSearch?apiKey=" + api_key + params
            response = requests.get(query)
            response = response.json()

            if response == [] or response["results"] == []:
                params = self.Recipe_Name(recipe_name)
                self.Query(params,api_key,recipe_name) #Se a API não retornar nenhuma receita, uma nova receita será selecionada

            return response
        
        def Recipe_Name(self,recipe_name):
             #Nome da receita caso o usuário não tenha especificado totalemente o nome da receita
             # Por exemplo se o usário escrver "bolo" assim pode lhe aparecer no resultado "bolo de chocolate" ou "bolo de cenoura", etc.
            offset = random.randint(0, MAX_OFFSET)
            number = 1 #Número de receitas que serão retornadas
            return f"&query={recipe_name.lower()}&offset={offset}&number={number}"
        
        def Status(self,api_key):
            query_base = f"https://api.spoonacular.com/recipes/complexSearch?apiKey={api_key}"
            response= requests.get(query_base)
            status = response.status_code
            if status== 200: #Código 200 indica que a conexão foi realizada com sucesso
                print("\033[92mConexão realizada com sucesso\033[0m\n") #Código de cor verde para indicar que a conexão foi realizada com sucesso
            elif status == 402: #Código 402 indica que a chave de API atingiu o limite de uso
                i = API_KEYS.index(api_key)
                
                if i == len(API_KEYS)-1:
                    return None
                else:
                    api_key = API_KEYS[i+1] #Muda a chave de API
                    self.Status(api_key) #Chama a função novamente para verificar se a nova chave de API está funcionando
            else:
                print("\033[91mErro na conexão\033[0m") #Código de cor vermelha para indicar que houve um erro na conexão
                api_key = None
                
            return api_key

        def run(self, dispatcher: CollectingDispatcher,
                tracker: Tracker, 
                domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            
            api_key = API_KEYS[0]
            message = "Nehuma receita encontrada"
            api_key = self.Status(api_key)

            if api_key == None:
                message = "Erro na conexão"
                dispatcher.utter_message(text=message)
                return []
            
            #recipe_name = next(tracker.get_latest_entity_values("receita"), None) #Nome da receita que o usuário deseja

            recipe_name = "pasta"

            params = self.Recipe_Name(recipe_name) #Parâmetros da receita aleatória

            response = self.Query(params,api_key,recipe_name)

            for r in response["results"]:
                recipe = (r["title"], r["id"]) 
                

                if self.Get_Recipe_Info(recipe[1],api_key) != None or self.Get_Recipe_instructions(recipe,api_key) != None:
                    image,meal_type,ingredients_info = self.Get_Recipe_Info(recipe[1],api_key)
                    description,all_equipaments = self.Get_Recipe_instructions(recipe,api_key)
                    message = f"\tReceita: {recipe[0]}\n\n\nImagem: {image}\n\n\nTipo de refeição: {meal_type}\n\n\nIngredientes: {ingredients_info}\n\n\nPassos: {description}\n\n\nEquipamentos: {all_equipaments}"

            dispatcher.utter_message(text=message)
            return []
            
       
