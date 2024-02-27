import mysql.connector
from mysql.connector import Error
import getpass

def connect_to_mysql(user='root', password='', host='localhost'):
    try:
        return mysql.connector.connect(host=host, user=user, password=password)
    except Error as e:
        print(f"Erro ao conectar ao MariaDB: {e}")
        return None

def create_database(cursor, db_name):
    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        print(f"Banco de dados '{db_name}' criado com sucesso.")
    except Error as e:
        print(f"Erro ao criar o banco de dados: {e}")

def create_user(cursor, user, password, db_name):
    try:
        cursor.execute(f"CREATE USER IF NOT EXISTS '{user}'@'%' IDENTIFIED BY '{password}'")
        cursor.execute(f"GRANT ALL PRIVILEGES ON {db_name}.* TO '{user}'@'%'")
        cursor.execute("FLUSH PRIVILEGES")
        print(f"Usuário '{user}' criado com sucesso e permissões concedidas.")
    except Error as e:
        print(f"Erro ao criar o usuário: {e}")

def main():
    admin_password = getpass.getpass(prompt="Digite a senha do administrador do banco de dados: ")
    db_name = 'recipe_database'
    new_user = 'admin'
    new_password = 'admin_password'  # Considere solicitar essa senha também

    # Conectar como root
    root_conn = connect_to_mysql(password=admin_password)
    if root_conn:
        root_cursor = root_conn.cursor()
        create_database(root_cursor, db_name)
        create_user(root_cursor, new_user, new_password, db_name)
        root_cursor.close()
        root_conn.close()

    # Conectar como o novo usuário
    db_conn = connect_to_mysql(user=new_user, password=new_password, host='localhost')
    if db_conn:
        db_conn.database = db_name
        # Aqui você pode criar suas tabelas usando db_conn
        print("Conectado ao banco de dados com o novo usuário.")
        db_conn.close()

if __name__ == "__main__":
    main()
