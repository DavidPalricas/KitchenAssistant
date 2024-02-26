-- -------------------------------------------------------------------------------
-- 1. Visualização das Informações da Receita
-- -------------------------------------------------------------------------------
-- Esta visualização mostra: 
--  o nome da receita, 
--  o número de porções, 
--  o tempo de cozimento, 
--  as calorias por porção.
--
CREATE VIEW recipe_information AS
SELECT 
    r.recipe_id,
    r.name AS RECEITA,
    r.number_of_servings AS Serviços,
    r.cooking_time AS Tempo,
    (SUM(ri.calories) / r.number_of_servings) AS CaloriasPorPorção
FROM 
    recipes r
JOIN 
    recipe_ingredients ri ON r.recipe_id = ri.recipe_id
GROUP BY
    r.recipe_id;


-- -------------------------------------------------------------------------------
-- 2. Visualização dos Ingredientes de uma Receita Selecionada
-- -------------------------------------------------------------------------------
-- Esta visualização mostra:
--  os ingredientes para uma receita, 
--
CREATE VIEW recipe_ingredients_view AS
SELECT 
    r.recipe_id,
    r.name AS Receita,
    ri.name AS Ingrediente,
    ri.quantity,
    ri.unit,
    ri.calories,
    ri.source_url
FROM 
    recipes r
JOIN 
    recipe_ingredients ri ON r.recipe_id = ri.recipe_id;


-- -------------------------------------------------------------------------------
-- 3. Visualização das Ferramentas para uma Receita Selecionada
-- -------------------------------------------------------------------------------
-- Esta visualização mostra: 
--  as ferraments necessárias para uma receita, 
--  com base nas isntruções
--
CREATE VIEW recipe_tools_view AS
SELECT 
    r.recipe_id,
    r.name AS Receita,
    t.name AS Ferramenta
FROM 
    recipes r
JOIN 
    recipe_instructions ri ON r.recipe_id = ri.recipe_id
JOIN 
    instructions_tools it ON ri.recipe_instruction_id = it.recipe_instruction_id
JOIN 
    tools t ON it.tool_id = t.tool_id;


-- -------------------------------------------------------------------------------
-- 4. Visualização das Instruções de uma Receita Selecionada e Ferramentas Usadas
-- -------------------------------------------------------------------------------
-- Esta visualização mostra: 
--  as instruções de preparação de uma receita, 
--  e as ferramentas necessárias para cada instrução
--
CREATE VIEW recipe_instructions_tools_view AS
SELECT 
    r.recipe_id,
    r.name AS Receita,
    ri.step_number AS Passo,
    ri.description AS Instrução,
    t.name AS Ferramenta
FROM 
    recipes r
JOIN 
    recipe_instructions ri ON r.recipe_id = ri.recipe_id
LEFT JOIN 
    instructions_tools it ON ri.recipe_instruction_id = it.recipe_instruction_id
LEFT JOIN 
    tools t ON it.tool_id = t.tool_id;


-- -------------------------------------------------------------------------------
-- 5. Visualização da URL da Imagem da Receita para uma Receita Selecionada
-- -------------------------------------------------------------------------------
-- Esta visualização mostra: 
--  o url da imagem da receita,
--
CREATE VIEW recipe_image_view AS
SELECT 
    recipe_id,
    image_url AS recipe_img_url
FROM 
    recipe_images;


-- -------------------------------------------------------------------------------
-- 6. Visualização das Tags de uma Receita Selecionada
-- -------------------------------------------------------------------------------
-- Esta visualização mostra: 
--  as tags da receita,
--
CREATE VIEW recipe_tags_view AS
SELECT 
    r.recipe_id,
    r.name AS Receita,
    t.name AS Tag
FROM 
    recipes r
JOIN 
    recipe_tags rt ON r.recipe_id = rt.recipe_id
JOIN 
    tags t ON rt.tag_id = t.tag_id;



-- SELECTS PARA USAR AS VIEWS CRIADAS -------------------------------------------

-- 1. Visualização das Informações da Receita
SELECT * FROM recipe_information WHERE RECEITA = 'Pica-Pau de Entremeada';

-- 2. Visualização dos Ingredientes de uma Receita Selecionada
SELECT * FROM recipe_ingredients_view WHERE recipe_id = 57;

-- 3. Visualização das Ferramentas para uma Receita Selecionada
SELECT * FROM recipe_tools_view WHERE recipe_id = 57;

-- 4. Visualização das Instruções de uma Receita Selecionada e Ferramentas Usadas
SELECT * FROM recipe_instructions_tools_view WHERE recipe_id = 57;

-- 5. Visualização da URL da Imagem da Receita para uma Receita Selecionada
SELECT * FROM recipe_image_view WHERE recipe_id = 57;

-- 6. Visualização das Tags de uma Receita Selecionada
SELECT * FROM recipe_tags_view WHERE recipe_id = 57;

-- -------------------------------------------------------------------------------