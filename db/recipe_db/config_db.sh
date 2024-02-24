#!/bin/bash

# Caminho para o arquivo SQL
SQL_FILE="KitchenAssistant/db/recipe_db/setup_database.sql"

# Usuário e senha do banco de dados
DB_USER="admin"
DB_PASSWORD="admin" # Atenção: armazenar senhas em scripts é inseguro

# Executar o script SQL
mysql -u "$DB_USER" -p"$DB_PASSWORD" < "$SQL_FILE"

echo "Base de dados configurada."
