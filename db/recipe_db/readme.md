
# Comandos MariaDB para macOS e Windows

Este documento fornece uma visão geral dos comandos necessários para gerir uma base de dados MariaDB em sistemas operacionais macOS e Windows.

## macOS

### Instalação
- Instale o MariaDB usando o Homebrew:
```bash
brew install mariadb
```

### Iniciar o Servidor MariaDB
- Para iniciar o MariaDB:
```bash
brew services start mariadb
```

### Acesso ao MariaDB
- Acessar o MariaDB:
```bash
mysql -u
```

### Criar a Base de Dados
- Criar uma base de dados:
```sql
CREATE DATABASE recipe_database;
```

### Importar um Ficheiro SQL
- Importar um ficheiro SQL para a base de dados:
```bash
mysql -u recipe_database < db/recipe_db/setup_database.sql 
```

## Windows

### Instalação
- Baixe o instalador do MariaDB do [site oficial](https://mariadb.org/download/) e siga as instruções de instalação.

### Iniciar o Servidor MariaDB
- Geralmente, o MariaDB é configurado para iniciar automaticamente. Caso contrário, pode iniciar o MariaDB através do Serviços do Windows ou usando o `mysqld`.

### Acesso ao MariaDB
- Abra o Prompt de Comando e acesse o MariaDB:
```bash
mysql -u
```

### Criar a Base de Dados
- Criar uma base de dados:
```sql
CREATE DATABASE recipe_database;
```

### Importar um Ficheiro SQL
- Importar um ficheiro SQL para a base de dados:
```bash
mysql -u  recipe_database < db/recipe_db/setup_database.sql 
```

