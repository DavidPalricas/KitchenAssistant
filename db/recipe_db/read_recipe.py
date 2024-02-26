import argparse
import ast


def read_recipe_from_txt(file_path):
    recipe_data = {}
    buffer = ""
    multi_line = False

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            stripped_line = line.strip()
            if stripped_line.endswith('{'):
                # Início de uma estrutura multilinha
                buffer += stripped_line
                multi_line = True
            elif multi_line:
                # Continuação/fim de uma estrutura multilinha
                buffer += stripped_line
                if stripped_line.endswith('}'):
                    # Tentativa de avaliar a estrutura multilinha completa
                    try:
                        key, value = buffer.split('=', 1)
                        recipe_data[key.strip()] = ast.literal_eval(value.strip())
                        buffer = ""
                        multi_line = False
                    except SyntaxError as e:
                        print(f"Erro ao interpretar a estrutura multilinha: {e}")
            else:
                # Linhas que não fazem parte de uma estrutura multilinha
                if '=' in line:
                    try:
                        key, value = line.split('=', 1)
                        recipe_data[key.strip()] = ast.literal_eval(value.strip())
                    except SyntaxError as e:
                        print(f"Erro ao interpretar a linha: {line.strip()}: {e}")

    return recipe_data

def main(file_path):
    recipe_data = read_recipe_from_txt(file_path)
    print("RECIPE NAME:", recipe_data.get("NAME"))
    print("\n")
    print("RECIPE INGREDIENTS:", recipe_data.get("INGREDIENTS"))
    print("\n")
    print("RECIPE TOOLS:", recipe_data.get("TOOLS"))
    print("\n")
    print("RECIPE INSTRUCTIONS:", recipe_data.get("INSTRUCTIONS"))
    print("\n")
    print("RECIPE TIME:", recipe_data.get("COOKING_TIME"))
    print("\n")
    print("RECIPE SERVINGS:", recipe_data.get("NUMBER_OF_SERVINGS"))
    print("\n")
    print("RECIPE IMAGE:", recipe_data.get("IMAGE_URL"))
    print("\n")
    print("RECIPE TAGS:", recipe_data.get("TAGS"))
    print("\n")

if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Read and display recipe data from a text file.")
    parser.add_argument('file_path', type=str, help='Path to the recipe text file.')

    # Parse arguments
    args = parser.parse_args()

    # Call the main function with the provided file path
    main(args.file_path)






