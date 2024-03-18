import sys

def convert_number_words_to_digits(words, numbers_dict):
    result = 0
    temp_number = 0
    for word in words:
        # Skip "e" as it's just a connector in Portuguese numbers
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

def main(argv):
    numbers_dict = {
        "zero": 0, "um": 1, "dois": 2, "três": 3, "quatro": 4,
        "cinco": 5, "seis": 6, "sete": 7, "oito": 8, "nove": 9,
        "dez": 10, "onze": 11, "doze": 12, "treze": 13, "quatorze": 14,
        "quinze": 15, "dezesseis": 16, "dezessete": 17, "dezoito": 18, "dezenove": 19,
        "vinte": 20, "trinta": 30, "quarenta": 40, "cinquenta": 50,
        "sessenta": 60, "setenta": 70, "oitenta": 80, "noventa": 90,
        "cem": 100, "cento": 100, "duzentos": 200, "trezentos": 300, 
        "quatrocentos": 400, "quinhentos": 500, "seiscentos": 600,
        "setecentos": 700, "oitocentos": 800, "novecentos": 900,
        "mil": 1000, "milhão": 1000000
    }

    if len(argv) != 2:
        print("Usage: python convert_text_to_digit.py 'number in words'")
        return

    input_text = argv[1].lower()
    words = input_text.split()

    number = convert_number_words_to_digits(words, numbers_dict)
    if number is not None:
        print(f"O número digitado foi: {number}")
    else:
        print("Não foi possível converter o texto em número.")

if __name__ == "__main__":
    main(sys.argv)
