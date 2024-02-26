-- Criar a base de dados se ela não existir
CREATE DATABASE IF NOT EXISTS recipe_database;

-- Selecionar a base de dados
USE recipe_database;

-- Criar Tabela de Receitas
CREATE TABLE IF NOT EXISTS recipes (
    recipe_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    number_of_servings INT,
    cooking_time INT, -- Tempo em minutos necessário para preparar a receita
    source_url TEXT -- URL da fonte original da receita
);

-- Criar Tabela de Ingredientes das Receitas
CREATE TABLE IF NOT EXISTS recipe_ingredients (
    recipe_ingredient_id INT AUTO_INCREMENT PRIMARY KEY,
    recipe_id INT ,
    name VARCHAR(255) NOT NULL,
    quantity DECIMAL(10, 2),
    unit VARCHAR(50), -- (gramas, mililitros, colheres de sopa)
    calories INT, -- Calorias por o spoonacular
    source_url VARCHAR(255), -- URL da fonte original do nutri_score do ingrediente 
    FOREIGN KEY (recipe_id) REFERENCES recipes (recipe_id) ON DELETE CASCADE
);

-- Criar Tabela de Instruções das Receitas
CREATE TABLE IF NOT EXISTS recipe_instructions (
    recipe_instruction_id INT AUTO_INCREMENT PRIMARY KEY,
    recipe_id INT NOT NULL,
    step_number INT NOT NULL,
    description TEXT NOT NULL,
    FOREIGN KEY (recipe_id) REFERENCES recipes (recipe_id) ON DELETE CASCADE
);

-- Criar Tabela de Tags
-- Exemplos de tags: (Vegan, under 30 min, Glúten-free, high-Protein, Low-Cal)
CREATE TABLE IF NOT EXISTS tags (
    tag_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

-- Criar Tabela de Associação de Tags às Receitas
CREATE TABLE IF NOT EXISTS recipe_tags (
    recipe_id INT ,
    tag_id INT ,
    PRIMARY KEY (recipe_id, tag_id),
    FOREIGN KEY (recipe_id) REFERENCES recipes (recipe_id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES tags (tag_id) ON DELETE RESTRICT
);

-- À posteriori: Criar Tabela de Imagens das Receitas (Para depois usar na apresentação visual)
CREATE TABLE IF NOT EXISTS recipe_images (
    image_id INT AUTO_INCREMENT PRIMARY KEY,
    recipe_id INT ,
    image_url TEXT ,
    source_url TEXT, -- URL da fonte original da imagem
    FOREIGN KEY (recipe_id) REFERENCES recipes (recipe_id) ON DELETE CASCADE
);

-- Criar Tabela de utensílios
CREATE TABLE IF NOT EXISTS tools (
    tool_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) ,
    source_url TEXT -- URL da fonte original do utensílio
);

-- Criar Tabela de Associação de utensilios às Receitas
CREATE TABLE IF NOT EXISTS instructions_tools (
    recipe_instruction_id INT ,
    tool_id INT ,
    PRIMARY KEY (recipe_instruction_id, tool_id),
    FOREIGN KEY (recipe_instruction_id) REFERENCES recipe_instructions (recipe_instruction_id) ON DELETE CASCADE,
    FOREIGN KEY (tool_id) REFERENCES tools (tool_id) ON DELETE RESTRICT
);

-- Criar um novo usuário e conceder permissões (opcional)
-- CREATE USER IF NOT EXISTS 'admin'@'localhost' IDENTIFIED BY 'admin';
-- GRANT ALL PRIVILEGES ON recipe_database.* TO 'admin'@'localhost';
-- FLUSH PRIVILEGES;
