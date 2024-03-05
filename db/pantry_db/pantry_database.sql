CREATE DATABASE IF NOT EXISTS pantry_database;

USE pantry_database;

CREATE TABLE IF NOT EXISTS ingredients (
    ingredient_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    quantity DECIMAL(10, 2),
    unit VARCHAR(50), -- (gramas, mililitros, colheres de sopa)
    calories INT, -- Calorias por o spoonacular
    source_url VARCHAR(255) -- URL da fonte original do nutri_score do ingrediente 
);

CREATE TABLE IF NOT EXISTS grocerylists (
    grocerylist_id INT AUTO_INCREMENT PRIMARY KEY,
    ingridient_id INT,
    quantity DECIMAL(10, 2),
    unit VARCHAR(50),
    FOREIGN KEY (ingridient_id) REFERENCES ingredients (ingredient_id)
);