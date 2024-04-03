CREATE DATABASE IF NOT EXISTS pantry_database;
USE pantry_database;


--This table will store unique types of food items without quantity. 
-- Each entry represents a type of food without regard to quantity or expiration date.
CREATE TABLE IF NOT EXISTS stock (
    stock_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);


-- This table will store individual entries of food items,including their quantities and expiration dates. 
-- Each entry is linked to an item in the Stock table but allows for tracking different expiration dates and quantities of the same food item.
CREATE TABLE IF NOT EXISTS stock_details (
    detail_id INT AUTO_INCREMENT PRIMARY KEY,
    stock_id INT,
    quantity DECIMAL(10, 2),
    unit VARCHAR(50), -- e.g., grams, milliliters, pieces
    expiration_date DATE,
    FOREIGN KEY (stock_id) REFERENCES stock(stock_id)
);

-- listing items that need to be purchased.
CREATE TABLE IF NOT EXISTS grocerylist (
    grocerylist_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    quantity DECIMAL(10, 2),
    unit VARCHAR(50)
);


-- Criar um novo usuário e conceder permissões (opcional)
-- CREATE USER IF NOT EXISTS 'admin'@'localhost' IDENTIFIED BY 'admin';
-- GRANT ALL PRIVILEGES ON pantry_database.* TO 'admin'@'localhost';
-- FLUSH PRIVILEGES;