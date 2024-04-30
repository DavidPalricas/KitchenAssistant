"""
@brief Este módulo contém funções para converter palavras em números e unidades de medida do Português para os seus respectivos dígitos e abreviações.

Este módulo é útil para processar texto em Português que contenha números por extenso e unidades de medida, convertendo-os para uma forma mais compacta e padronizada. 
Este processo facilita outras tarefas de processamento de texto que dependam de valores numéricos ou medidas padronizadas.

@details As funções principais deste módulo lidam com a conversão de palavras para números e de unidades completas para as suas abreviações. 
Os dicionários `numbers_dict` e `uni_dict` contêm as correspondências usadas nas conversões.

@note Este módulo pode ser utilizado em conjunto com outros módulos ou scripts que envolvam processamento de texto em Português,
para facilitar a manipulação de números e unidades de medida em diferentes contextos.
"""
import re
import sys
# working with numbers in Portuguese based on a exercicie made in the course "Compiladores"

def convert_number_words_to_digits(words):
    """
    @brief Converte uma lista de palavras que representam números por extenso em Português para um valor numérico inteiro.
    @details Esta função itera sobre cada palavra na lista, somando os valores conforme necessário para construir o número final. A função ignora a palavra 'e'. 
    Se uma palavra inválida for encontrada, a função imprime uma mensagem de erro e retorna None.
    
    @param words Lista de strings, onde cada string é uma palavra representando um número ou a conjunção 'e'.
    
    @return Um inteiro representando o valor numérico das palavras, ou None se alguma palavra não puder ser convertida.
    """
    result = 0
    temp_number = 0
    for word in words:
        if word == "e":
            continue
        if word in numbers_dict:
            number = numbers_dict[word]
            if number >= 100:
                if temp_number == 0:
                    temp_number = 1
                result += temp_number * number
                temp_number = 0
            else:
                temp_number += number
        else:
            print(f"Palavra inválida: {word}")
            return None
    return result + temp_number

def convert_units(word):
    """
    @brief Converte palavras que representam unidades de medida para suas respectivas abreviações.
    @details Utiliza o dicionário `uni_dict` para encontrar a abreviação correspondente para a unidade de medida fornecida. 
    Se a unidade não estiver no dicionário, a palavra original é retornada.
    
    @param word Uma string que representa uma unidade de medida.
    
    @return A abreviação correspondente da unidade de medida, se disponível; caso contrário, retorna a palavra original.
    """
    if word in uni_dict:
        return uni_dict[word]
    return word
    
def extract_and_convert_numeric_phrases(sentence):
    """
    @brief Extrai frases numéricas de uma frase e converte as palavras numéricas e unidades de medida para seus respectivos valores numéricos e abreviações.
    @details Esta função divide a frase em palavras e processa-as individualmente. 
    As palavras reconhecidas como parte de uma frase numérica são acumuladas e convertidas num conjunto.
    
    @param sentence Uma string com a frase em Português.
    
    @return Uma string com os números e unidades de medida convertidos.
    """
    words = sentence.split()
    converted_words = []
    number_phrase = []
    for word in words:
        lower_word = word.lower()
        if lower_word in numbers_dict or lower_word == "e":
            number_phrase.append(lower_word)
        else:
            if number_phrase:
                converted_number = convert_number_words_to_digits(number_phrase)
                if converted_number is not None:
                    converted_words.append(str(converted_number))
                number_phrase = []
            converted_words.append(convert_units(word))
    
    # Check if sentence ends with a number phrase
    if number_phrase:
        converted_number = convert_number_words_to_digits(number_phrase)
        if converted_number is not None:
            converted_words.append(str(converted_number))
    
    return ' '.join(converted_words)


## @var numbers_dict
#  @brief Dicionário que mapeia palavras em Português para seus valores numéricos correspondentes.
#  @details Este dicionário contém as correspondências entre palavras em Português e seus valores numéricos correspondentes.
#   - As palavras são escritas em minúsculas para facilitar a comparação.
#
#   - As palavras que representam números de 100 ou mais são tratadas separadamente para permitir a construção de números maiores.
#  
#   - As palavras "um" e "uma" são tratadas como 1, e "cem" e "cento" são tratadas como 100.
#
#   - As palavras "mil" e "milhão" são tratadas como 1000 e 1000000, respetivamente.
#  
#   - As palavras "milhares" e "milhar" são tratadas como 1000.
#
#  @note Este dicionário pode ser expandido para incluir mais palavras e números conforme necessário.
numbers_dict = {
    "zero": 0, "um": 1, "uma": 1, "dois": 2, "duas": 2, "três": 3, "tres": 3, "quatro": 4, "cinco": 5,
    "seis": 6, "sete": 7, "oito": 8, "nove": 9, "dez": 10, "onze": 11,
    "doze": 12, "treze": 13, "quatorze": 14, "catorze": 14, "quinze": 15, "dezesseis": 16, "dezasseis": 16,
    "dezessete": 17, "dezassete": 17, "dezoito": 18, "dezenove": 19, "dezanove": 19, "vinte": 20, "trinta": 30,
    "quarenta": 40, "cinquenta": 50, "sessenta": 60, "setenta": 70, "oitenta": 80,
    "noventa": 90, "cem": 100, "cento": 100, 
    "duzentos": 200, "duzentas": 200, "trezentos": 300, "trezentas": 300,
    "quatrocentos": 400, "quatrocentas": 400, "quinhentos": 500, "quinhentas": 500,
    "seiscentos": 600, "seiscentas": 600, "setecentos": 700, "setecentas": 700,
    "oitocentos": 800, "oitocentas": 800, "novecentos": 900, "novecentas": 900,
    "mil": 1000, "milhão": 1000000, "milhões": 1000000,
    "milhares": 1000, "milhar": 1000
}

## @var uni_dict
#  @brief Dicionário que mapeia palavras em Português para suas abreviações de unidades de medida correspondentes.
#  @details Este dicionário contém as correspondências entre palavras em Português e suas abreviações de unidades de medida correspondentes.
#   - As palavras são escritas em minúsculas para facilitar a comparação.
#
#   - As abreviações são escritas no singular para simplificar a conversão.
#
#  @note Este dicionário pode ser expandido para incluir mais palavras e abreviações conforme necessário.
uni_dict = {
    "litros" : "l", "mililitros" : "ml", "centilitros" : "cl", "decilitros" : "dl",
    "gramas" : "g", "quilogramas" : "kg", "quilos" : "kg", "miligramas" : "mg", 
    "unidades" : "uni", "latas" : "lata", "pacotes" : "pacote", "tabletes" : "tablete",
    "dentes" : "dente", "folhas" : "folha", "ramos" : "ramo", "talos" : "talo",
    "copos" : "copo", "garrafas" : "garrafa", "capsulas" : "capsula", "saquetas" : "saqueta",
    "colheres de sopa" : "colher de sopa", "colheres de chá" : "colher de chá"
}

def main(argv):
    """
    @brief Função principal que processa a linha de comando para converter frases.
    @details Esta função lê a frase fornecida na linha de comando e chama a função `extract_and_convert_numeric_phrases` para processá-la.
    
    @param argv Lista de argumentos da linha de comando.
    
    @code
    // Exemplo de uso:
    python convert_text_to_digit.py 'Adicionei quarenta e cinco kg de açúcar.'
    // return
    Adicionei 45 kg de açúcar.
    @endcode
    
    @note O main está feito para chamar a função `extract_and_convert_numeric_phrases` com a frase fornecida na linha de comando.
    Mas pode ser adaptado para chamar a função `convert_units` ou `convert_number_words_to_digits` diretamente.
    """
    if len(argv) != 2:
        print("Usage: python convert_text_to_digit.py 'sentence with number words'")
        return

    input_sentence = argv[1]
    converted_sentence = extract_and_convert_numeric_phrases(input_sentence)
    print(converted_sentence)

if __name__ == "__main__":
    main(sys.argv)
