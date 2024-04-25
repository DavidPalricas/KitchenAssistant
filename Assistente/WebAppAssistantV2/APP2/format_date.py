import re
import sys
from datetime import datetime

# Dictionary of Portuguese month names to month numbers
month_to_number = {
    "Janeiro": 1, "Fevereiro": 2, "Março": 3, "Abril": 4, "Maio": 5, "Junho": 6,
    "Julho": 7, "Agosto": 8, "Setembro": 9, "Outubro": 10, "Novembro": 11, "Dezembro": 12
}

# Regex patterns to match different date formats
date_patterns = {
    r"(\d{1,2})/(\d{1,2})\s(\d{4})": "DD/MM YYYY",  # 24/3 2045
    r"(\d{1,2})/(\d{1,2})/(\d{4})": "DD/MM/YYYY",   # 21/05/2024
    r"(\d{1,2}) de (\w+) de (\d{4})": "DD de Month de YYYY",  # 21 de Maio de 2030
    r"(\d{1,2}) de (\w+)\s(\d{4})": "DD de Month de YYYY",  # 21 de Maio 2030
    r"(\d{1,2})\s(\w+) de (\d{4})": "DD de Month de YYYY",  # 21 Maio de 2030
    r"(\d{1,2})\s(\w+)\s(\d{4})": "DD de Month de YYYY"  # 21 Maio 2030
}

def parse_date(date_string):
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
    if len(sys.argv) != 2:
        print("Usage: python format_date.py 'date string'")
        sys.exit(1)
    input_date = sys.argv[1]
    result = parse_date(input_date)
    print(result)

if __name__ == "__main__":
    main()
