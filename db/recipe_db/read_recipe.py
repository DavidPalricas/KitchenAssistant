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

# Exemplo de uso
file_path = 'recipe_format.txt'
recipe_data = read_recipe_from_txt(file_path)

print(recipe_data)
