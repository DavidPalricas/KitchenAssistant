import mysql.connector
from mysql.connector import Error
import getpass  # Importando a biblioteca getpass para solicitar a senha de forma segura

# Configurações iniciais
db_name = 'recipe_database'
db_user = 'admin'
db_password = 'admin'
admin_user = 'root'
# Removida a senha do admin do local de armazenamento estático
host = 'localhost'

# Comandos SQL para criar tabelas
table_creation_commands = [
    """
    CREATE TABLE IF NOT EXISTS recipes (
        recipe_id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        number_of_servings INT,
        cooking_time INT,
        source_url TEXT
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS recipe_ingredients (
        recipe_ingredient_id INT AUTO_INCREMENT PRIMARY KEY,
        recipe_id INT,
        name VARCHAR(255) NOT NULL,
        quantity DECIMAL(10, 2),
        unit VARCHAR(50),
        calories INT,
        source_url VARCHAR(255),
        FOREIGN KEY (recipe_id) REFERENCES recipes (recipe_id) ON DELETE CASCADE
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS recipe_instructions (
        recipe_instruction_id INT AUTO_INCREMENT PRIMARY KEY,
        recipe_id INT NOT NULL,
        step_number INT NOT NULL,
        description TEXT NOT NULL,
        FOREIGN KEY (recipe_id) REFERENCES recipes (recipe_id) ON DELETE CASCADE
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS tags (
        tag_id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS recipe_tags (
        recipe_id INT,
        tag_id INT,
        PRIMARY KEY (recipe_id, tag_id),
        FOREIGN KEY (recipe_id) REFERENCES recipes (recipe_id) ON DELETE CASCADE,
        FOREIGN KEY (tag_id) REFERENCES tags (tag_id) ON DELETE RESTRICT
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS recipe_images (
        image_id INT AUTO_INCREMENT PRIMARY KEY,
        recipe_id INT,
        image_url TEXT,
        source_url TEXT,
        FOREIGN KEY (recipe_id) REFERENCES recipes (recipe_id) ON DELETE CASCADE
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS tools (
        tool_id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255),
        source_url TEXT
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS instructions_tools (
        recipe_instruction_id INT,
        tool_id INT,
        PRIMARY KEY (recipe_instruction_id, tool_id),
        FOREIGN KEY (recipe_instruction_id) REFERENCES recipe_instructions (recipe_instruction_id) ON DELETE CASCADE,
        FOREIGN KEY (tool_id) REFERENCES tools (tool_id) ON DELETE RESTRICT
    );
    """
]


def connect_to_mysql(user, password):
    """Conecta ao servidor MySQL/MariaDB."""
    try:
        return mysql.connector.connect(host=host, user=user, password=password)
    except Error as e:
        print(f"Erro ao conectar ao MySQL/MariaDB: {e}")
        return None

def create_database(connection):
    """Cria o banco de dados."""
    try:
        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        print(f"Banco de dados '{db_name}' criado com sucesso.")
    except Error as e:
        print(f"Erro ao criar o banco de dados: {e}")

def create_user(connection):
    """Cria o usuário e concede permissões."""
    try:
        cursor = connection.cursor()
        cursor.execute(f"CREATE USER IF NOT EXISTS '{db_user}'@'%' IDENTIFIED BY '{db_password}'")
        cursor.execute(f"GRANT ALL PRIVILEGES ON {db_name}.* TO '{db_user}'@'%'")
        cursor.execute("FLUSH PRIVILEGES")
        print(f"Usuário '{db_user}' criado e permissões concedidas.")
    except Error as e:
        print(f"Erro ao criar usuário: {e}")

def create_tables(connection):
    """Cria as tabelas no banco de dados."""
    try:
        cursor = connection.cursor()
        for command in table_creation_commands:
            cursor.execute(command)
        print("Tabelas criadas com sucesso.")
    except Error as e:
        print(f"Erro ao criar tabelas: {e}")

def main():
    # Solicitar a senha do administrador
    admin_password = getpass.getpass(prompt="Digite a senha do administrador do banco de dados: ")

    # Conectar ao MySQL/MariaDB como administrador
    admin_connection = connect_to_mysql(admin_user, admin_password)
    if admin_connection is not None:
        create_database(admin_connection)
        create_user(admin_connection)
        admin_connection.close()

    # Conectar ao banco de dados como o usuário recém-criado
    db_connection = connect_to_mysql(db_user, db_password)
    if db_connection is not None:
        db_connection.database = db_name  # Selecionar o banco de dados
        create_tables(db_connection)
        db_connection.close()

if __name__ == "__main__":
    main()
