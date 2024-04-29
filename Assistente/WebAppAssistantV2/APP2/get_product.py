"""
@file get_product.py
@brief Módulo para extrair ingredientes e unidades de medida de sentenças em português utilizando o modelo linguístico do spaCy.

Este módulo define funções para identificar ingredientes e unidades de medida em sentenças, baseando-se em listas predefinidas de alimentos e unidades comuns na culinária. O módulo utiliza o processamento de linguagem natural com o modelo "pt_core_news_sm" do spaCy para lematização e tokenização, aumentando a precisão na identificação de ingredientes em diferentes formas flexionadas.

@details As funções principais do módulo são:
- `get_ingredient(sentence)`: Identifica e retorna o ingrediente presente na sentença, se houver.
- `get_unit(sentence)`: Identifica e retorna a unidade de medida presente na sentença, se houver.

Os ingredientes e unidades são identificados mesmo que estejam flexionados, graças à lematização feita pelo spaCy, o que permite que o módulo funcione de maneira eficaz em textos reais e variados.

@example
    sentence = "Adicione 200g de açúcar e 500ml de leite ao preparo."
    ingredient = get_ingredient(sentence)
    unit = get_unit(sentence)
    print(f"Ingrediente: {ingredient}, Unidade: {unit}")
    # Output: Ingrediente: açúcar, Unidade: g

@note É necessário instalar o spaCy e baixar o modelo de linguagem português para o funcionamento adequado deste módulo.
    - pip install spacy
    - python -m spacy download pt_core_news_sm
"""
import spacy
# pip install spacy
# python -m spacy download pt_core_news_sm

# List of common units of measure in Portuguese
unit_list = [
    "l", "ml", "cl", "dl", "kg", "g", "mg", 
    "uni", "lata", "colher de sopa", 
    "colher de chá", "copo", "garrafa", 
    "tablete", "pacote", "cápsula",
    "saqueta", "dente", "folha", 
    "ramo", "talo"
]

# Comprehensive list of food items categorized by type (e.g., Seafood, Meats, Dairy)
food_list = [
    # Seafood
    "bacalhau", "sardinhas", "polvo", "amêijoas", "lulas", "robalo", "dourada",
    "truta", "atum", "cavala", "salmão", "peixe-espada", "pescada", "linguado",
    "carapau", "enguias", "lagosta", "camarões", "lagostim", "sapateira",
    "caranguejo", "berbigão", "búzios", "congro", "salmonete", "filetes de pescada",
    "bife de atum", "lombos de salmão", "medalhões de pescada",
    
    # Meats
    "frango", "peito de frango", "coxa de frango", "perna de frango", "asas de frango",
    "peru", "peito de peru", "coxa de peru", "perna de peru", "lombo de porco",
    "porco", "cachaço", "rojões", "entremeada", "costeleta de porco", "feveras",
    "bife", "bife da vazia", "bife do lombo", "bife da alcatra", "bife da pá",
    "bife de peru", "bife de frango", "bife de vitela", "lombo de vitela", "vitela",
    "lombo de novilho", "novilho", "lombo de vaca", "vaca", "lombo de boi", "boi",
    "lombo de cabrito", "cabrito", "lombo de borrego", "borrego", "chouriço", "presunto",
    "entrecosto", "pato", "coelho", "perdiz", "codorniz", "picanha", "alheira", "farinheira",
    "chouriça", "linguiça",
    

    # Dairy
    "queijo da serra", "queijo flamengo", "queijo de cabra", "queijo de ovelha",
    "queijo fresco", "queijo curado", "queijo ralado", "queijo emmental", "queijo mozzarella",
    "queijo cheddar", "queijo de barrar", "queijo creme", "leite", "manteiga",
    "manteiga de alho", "manteiga de ervas", "manteiga de amendoim", "manteiga de caju",
    "requeijão", "iogurte", "natas", "natas de soja", "mascarpone", "ricotta", "ovos",

    # Vegetables
    "batata", "cenoura", "tomates", "alho", "cebola", "courgette", "abóbora",
    "espinafres", "pimento", "ervilhas", "beterraba", "alface", "pepino", "brócolos",
    "couve-flor", "couve", "repolho", "nabo", "rabanete", "azeitonas", "milho",
    "feijão verde", "feijão", "feijão preto", "feijão encarnado", "feijão manteiga",
    "feijão frade", "grão de bico", "lentilhas", "favas", "espargos", "beringela",
    "abacate", "couve-de-bruxelas", "chuchu", "funcho", "gengibre", "alho-francês",
    "tremoços", "tomate-cereja", "cenoura baby", "espargos verdes", "espargos brancos",
    "cogumelos", "cogumelos shitake", "cogumelos portobello", "cogumelos paris",
    "cogumelos shimeji", "cogumelos enoki", "cogumelos maitake", "cogumelos chanterelle",
    "cogumelos morel", "grelos", "nabiças", "agrião","rucula", "rucula selvagem", "mostarda", "alface romana", "alface iceberg",

    # FRUITS
    "laranja", "tangerina", "limão", "lima", "maçã", "pera", "figo", "uvas",
    "morangos", "framboesas", "mirtilos", "amoras", "frutos vermelhos",
    "kiwi", "bananas", "ananás", "abacaxi", "maracujá", "manga", "papaia",
    "melão", "meloa", "melancia", "cereja", "nectarina", "pêssego", "damascos",
    "ameixa", "ameixa seca", "passas", "tâmaras", "alperce", "cocos",
    
    # Grains
    "arroz", "feijão", "grão de bico", "lentilha", "aveia", "milho", "trigo",
    "centeio", "cevada", "quinoa", "farinha de trigo", "farinha de centeio",
    "farinha",
    

    # Herbs and spices
    "salsa", "coentros", "louro", "pimenta", "sal", "alecrim", "manjericão",
    "orégãos", "hortelã", "tomilho", "pimentão", "colorau", "cominhos",
    "caril", "cebola em pó", "alho em pó", "paprika", "noz-moscada", "canela",
    "cravinho", "piri-piri", "coco ralado", "açafrão", "mostarda",

    # Nuts
    "amêndoa", "noz", "castanha", "avelã", "pinhão", "pistácio", "noz-pecã",
    "noz-macadâmia", "amendoim", "caju",

    # Oils and others
    "azeite", "vinagre", "massa", "farinha", "sal", "óleo", "manteiga", "vinho",
    "chá", "café", "açúcar mascavado", "açúcar branco", "açúcar amarelo",
    "açúcar em pó", "margarina", "pão de forma", "pão de mistura", "pão de cereais",
    "pão de centeio", "pão de milho", "pão de água", "pão de alho", "pão de leite",
    "pão de ló", "molho de soja", "molho inglês", "molho de tomate", "ketchup",
    "mostarda", "maionese", "picles", "polpa de tomate"
]


# Load the Portuguese language model
nlp = spacy.load("pt_core_news_sm")

#def get_ingredient(sentence, lista):
#    str = sentence.split(" ")
#
#    # ---------------------------------------------------------------- Check for multi-word ingredients
#    for food_product in str:
#        if food_product in lista:
#            return food_product
def get_ingredient(sentence):
    """
    Processa uma frase para identificar e retornar o ingrediente mencionado, se houver.
    
    @param sentence <string> contendo a sentença a ser analisada.
    @return <string> com o ingrediente identificado ou None se nenhum ingrediente for encontrado.
    """
    
    # Process the sentence using spaCy to tokenize and lemmatize the text
    doc = nlp(sentence.lower())

    # Convert list to lemmas
    lemmatized_list = {nlp(word)[0].lemma_ for word in food_list}
    original_list = set(food_list)
    
    # Check for multi-word units first (assumes lista is already lemmatized if necessary)
    for unit in [unit for unit in food_list if ' ' in unit]:
        if unit in sentence:
            return unit

    # Check for single-word units using lemmatization
    for token in doc:
        if token.lemma_ in lemmatized_list or token.text in original_list:
            return token.text  # return the original text

    return None  # If no unit is found
            
def get_unit(sentence):
    """
    Processa uma frase para identificar e retornar a unidade de medida mencionada, se houver.
    
    @param sentence <string> contendo a sentença a ser analisada.
    @return <string> com a unidade de medida identificada ou None se nenhuma unidade for encontrada.
    """
    words = sentence.split() # --------------------------------------- Split the sentence into words
    multi_word_units = [unit for unit in unit_list if ' ' in unit] # ----- Get multi-word units

    # ---------------------------------------------------------------- Check for multi-word units
    for unit in multi_word_units:
        if unit in sentence:
            return unit

    # ---------------------------------------------------------------- Check for single-word units
    for word in words:
        if word in [unit for unit in unit_list if ' ' not in unit]:
            return word