import re
import sys

def get_ingredient(sentence, lista):
    str = sentence.split(" ")

    for food_product in str:
        if food_product in lista:
            return food_product
            
