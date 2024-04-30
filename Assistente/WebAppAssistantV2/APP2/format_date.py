"""
@brief Módulo para análise e formatação de datas em diferentes formatos em português para o padrão ISO.

Este módulo fornece uma função para analisar strings de datas escritas em vários formatos em português e converte-las para o formato padrão ISO 8601 (YYYY-MM-DD). 
O módulo utiliza expressões regulares para identificar os formatos e o objeto datetime para a conversão.

@details A função principal do módulo é capaz de interpretar formatos com mês por extenso ou em número, 
utilizando um dicionário para a tradução dos nomes dos meses. Os formatos suportados incluem:
- DD/MM/YYYY (ex: 21/05/2024)
- DD/MM YYYY (ex: 24/3 2045)
- DD de Month de YYYY (ex: 21 de Maio de 2030)
- Outros formatos similares onde o mês pode estar por extenso e o ano pode estar com ou sem a preposição 'de'.

@note Caso a string de data não corresponda a nenhum dos formatos predefinidos, a função retornará "Invalid date format".

"""
import re
import sys
from datetime import datetime

## @var month_to_number
# @brief Dicionário que mapeia os nomes dos meses em português para seus respectivos números.
# @details Este dicionário é utilizado para converter o nome do mês em português para o número correspondente,
# permitindo a criação de objetos datetime com a data fornecida.
#
month_to_number = {
    "Janeiro": 1, "Fevereiro": 2, "Março": 3, "Abril": 4, "Maio": 5, "Junho": 6,
    "Julho": 7, "Agosto": 8, "Setembro": 9, "Outubro": 10, "Novembro": 11, "Dezembro": 12
}

## @var date_patterns
# @brief Dicionário que mapeia expressões regulares para formatos de datas em português.
# @details Este dicionário contém as expressões regulares correspondentes a diferentes formatos de datas em português,
# permitindo a identificação e extração dos componentes da data.
#
date_patterns = {
    r"(\d{1,2})/(\d{1,2})\s(\d{4})": "DD/MM YYYY",  # 24/3 2045
    r"(\d{1,2})/(\d{1,2})/(\d{4})": "DD/MM/YYYY",   # 21/05/2024
    r"(\d{1,2}) de (\w+) de (\d{4})": "DD de Month de YYYY",  # 21 de Maio de 2030
    r"(\d{1,2}) de (\w+)\s(\d{4})": "DD de Month de YYYY",  # 21 de Maio 2030
    r"(\d{1,2})\s(\w+) de (\d{4})": "DD de Month de YYYY",  # 21 Maio de 2030
    r"(\d{1,2})\s(\w+)\s(\d{4})": "DD de Month de YYYY"  # 21 Maio 2030
}

def parse_date(date_string):
    """
    @brief Analisa uma string de data em diversos formatos em português e converte para o formato ISO 8601 (YYYY-MM-DD).
    @details Esta função utiliza expressões regulares para identificar os formatos de datas suportados e extrair os componentes da data.
    Em seguida, cria um objeto datetime com a data fornecida e a converte para o formato ISO 8601.
    
    @param date_string <string> contendo a data num dos formatos suportados.
    
    @return <string> com a data no formato ISO ou uma mensagem indicando formato inválido.
    
    @note Caso a string de data não corresponda a nenhum dos formatos predefinidos, a função retornará "Invalid date format".
    """
    for pattern, date_format in date_patterns.items():
        match = re.match(pattern, date_string.strip())
        if match:
            if date_format == "DD/MM/YYYY" or date_format == "DD/MM YYYY":
                day, month, year = match.groups()
                return datetime(int(year), int(month), int(day)).strftime('%Y-%m-%d')
            elif date_format == "DD de Month de YYYY":
                day, month_name, year = match.groups()
                month = month_to_number.get(month_name.capitalize(), None)
                if month:
                    return datetime(int(year), month, int(day)).strftime('%Y-%m-%d')
    return "Invalid date format"

def main():
    """
    @brief Função principal para execução do módulo como script.
    @details Esta função é utilizada para executar o módulo como um script, recebendo a string de data como argumento da linha de comando.
    
    @param argv String de data fornecida como argumento da linha de comando.
    
    @code
    // Exemplo de uso:
    python format_date.py '21 de Maio de 2030'
    // Output:
    2030-05-21
    @endcode
    
    @note A string de data deve ser fornecida como argumento da linha de comando.
    """
    if len(sys.argv) != 2:
        print("Usage: python format_date.py 'date string'")
        sys.exit(1)
    input_date = sys.argv[1]
    result = parse_date(input_date)
    print(result)

if __name__ == "__main__":
    main()
