import re
import sys
# working with numbers in Portuguese

def convert_number_words_to_digits(words, numbers_dict):
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

def extract_and_convert_numeric_phrases(sentence, numbers_dict):
    # Simplified approach: directly replace words with their numeric equivalents
    words = sentence.split()
    converted_words = []
    number_phrase = []
    for word in words:
        if word.lower() in numbers_dict or word.lower() == "e":
            number_phrase.append(word.lower())
        else:
            if number_phrase:
                converted_number = convert_number_words_to_digits(number_phrase, numbers_dict)
                if converted_number is not None:
                    converted_words.append(str(converted_number))
                number_phrase = []
            converted_words.append(word)
    
    # Check if sentence ends with a number phrase
    if number_phrase:
        converted_number = convert_number_words_to_digits(number_phrase, numbers_dict)
        if converted_number is not None:
            converted_words.append(str(converted_number))
    
    return ' '.join(converted_words)

# Dictionary with the numeric words and their respective values in Portuguese (feminine and masculine forms included)
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

def main(argv):
    if len(argv) != 2:
        print("Usage: python convert_text_to_digit.py 'sentence with number words'")
        return

    input_sentence = argv[1]
    converted_sentence = extract_and_convert_numeric_phrases(input_sentence, numbers_dict)
    print(converted_sentence)

if __name__ == "__main__":
    main(sys.argv)
