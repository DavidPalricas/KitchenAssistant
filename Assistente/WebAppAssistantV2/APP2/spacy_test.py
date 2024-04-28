import spacy

# Load the Portuguese language model
nlp = spacy.load("pt_core_news_sm")

def get_unit(sentence, lista):
    # Process the sentence using spaCy to tokenize and lemmatize the text
    doc = nlp(sentence.lower())

    # Convert list to a set of lemmas and original text to improve matching chances
    lemmatized_list = {nlp(word.lower())[0].lemma_ for word in lista}
    original_list = set(lista)

    # Check for multi-word units first
    for unit in [unit for unit in lista if ' ' in unit]:
        if unit.lower() in sentence.lower():
            return unit

    # Check for single-word units using lemmatization and direct match
    for token in doc:
        if token.lemma_ in lemmatized_list or token.text in original_list:
            return token.text  # return the original text from the doc

    return None  # If no unit is found

# Example usage with your food list
food_list = [
    # Seafood
    "bacalhau", "sardinhas", "polvo", "amêijoas", "lulas", "robalo", "dourada",
    "truta", "atum", "cavala", "salmão", "peixe-espada", "pescada", "linguado",
    "carapau", "enguias", "lagosta", "camarões", "lagostim", "sapateira",
    "caranguejo", "berbigão", "búzios", "congro", "salmonete", "filetes de pescada",
    "bife de atum", "lombos de salmão", "medalhões de pescada","pescada",
    
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
    "mostarda", "maionese", "picles", "polpa de tomate", "biscoitos"
]

sentence = "confirma se tenho vinagre"
print(get_unit(sentence, food_list))  
