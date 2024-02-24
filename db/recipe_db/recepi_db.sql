-- Criar Tabela de Categorias
-- Exemplos de categorias: (Sobremesas, Pratos Principais, Entradas, Vegan, Saudável)
CREATE TABLE categories (
    category_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT
);

-- Criar Tabela de Ingredientes
CREATE TABLE ingredients (
    ingredient_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    nutri_score_value CHAR(1),
    source_url VARCHAR(255) -- URL da fonte original do nutri_score do ingrediente 
);

-- Criar Tabela de Receitas
CREATE TABLE recipes (
    recipe_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    number_of_servings INT,
    prep_time INT, -- Tempo em minutos
    cook_time INT, -- Tempo em minutos
    category_id INT,
    source_url TEXT, -- URL da fonte original da receita
    FOREIGN KEY (category_id) REFERENCES categories (category_id) ON DELETE SET NULL
);

-- Criar Tabela de Ingredientes das Receitas
CREATE TABLE recipe_ingredients (
    recipe_ingredient_id SERIAL PRIMARY KEY,
    recipe_id INT NOT NULL,
    ingredient_id INT NOT NULL,
    quantity DECIMAL(10, 2),
    unit VARCHAR(50), -- (gramas, mililitros, colheres de sopa)
    FOREIGN KEY (recipe_id) REFERENCES recipes (recipe_id) ON DELETE CASCADE,
    FOREIGN KEY (ingredient_id) REFERENCES ingredients (ingredient_id) ON DELETE RESTRICT
);

-- Criar Tabela de Instruções das Receitas
CREATE TABLE recipe_instructions (
    recipe_instruction_id SERIAL PRIMARY KEY,
    recipe_id INT NOT NULL,
    step_number INT NOT NULL,
    description TEXT NOT NULL,
    time INT, -- Tempo em minutos necessário para esta etapa
    FOREIGN KEY (recipe_id) REFERENCES recipes (recipe_id) ON DELETE CASCADE
);

-- Criar Tabela de Tags
-- Exemplos de tags: (Vegan, under 30 min, Glúten-free, high-Protein, Low-Cal)
CREATE TABLE tags (
    tag_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

-- Criar Tabela de Associação de Tags às Receitas
CREATE TABLE recipe_tags (
    recipe_id INT NOT NULL,
    tag_id INT NOT NULL,
    PRIMARY KEY (recipe_id, tag_id),
    FOREIGN KEY (recipe_id) REFERENCES recipes (recipe_id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES tags (tag_id) ON DELETE RESTRICT
);

-- À posteriori: Criar Tabela de Imagens das Receitas (Para depois usar na apresentação visual)
CREATE TABLE recipe_images (
    image_id SERIAL PRIMARY KEY,
    recipe_id INT NOT NULL,
    image_url TEXT NOT NULL,
    source_url TEXT, -- URL da fonte original da imagem
    FOREIGN KEY (recipe_id) REFERENCES recipes (recipe_id) ON DELETE CASCADE
);

-- Criar Tabela de utensílios
CREATE TABLE tools (
    tool_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    source_url TEXT -- URL da fonte original do utensílio
);

-- Criar Tabela de Associação de utensilios às Receitas
CREATE TABLE istructions_tools (
    recipe_instruction_id INT NOT NULL,
    tool_id INT NOT NULL,
    PRIMARY KEY (recipe_instruction_id, tool_id),
    FOREIGN KEY (recipe_instruction_id) REFERENCES recipe_instructions (recipe_instruction_id) ON DELETE CASCADE,
    FOREIGN KEY (tool_id) REFERENCES tools (tool_id) ON DELETE RESTRICT
);
```