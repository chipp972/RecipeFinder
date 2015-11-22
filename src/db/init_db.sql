# Script to initialize the database

DROP TABLE if exists url_to_treat;
DROP TABLE if exists no_recipe_url;
DROP TABLE if exists recipe_url;
DROP TABLE if exists types;
DROP TABLE if exists recipes;
DROP TABLE if exists ingredients;#(id*, name)
DROP TABLE if exists users;#(id*, e-mail, name, birth date)
DROP TABLE if exists opinions;#(id*, mark, comment, author#, recipe#)
DROP TABLE if exists recipe_has_ingredients;#(;#(idRecipe#, idIngr#)*)
DROP TABLE if exists user_currently_has_ingredient;#(;#(idUser#, idIngr#)*)
DROP TABLE if exists user_has_favorite_ingredient;#(;#(idUser#, idIngr#)*)
DROP TABLE if exists user_has_forbidden_ingredient;#(;#(idUser#, idIngr#)*)

CREATE TABLE url_to_treat (
    id INT PRIMARY KEY AUTO_INCREMENT,
    url VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE no_recipe_url (
    id INT PRIMARY KEY AUTO_INCREMENT,
    url VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE recipe_url (
    id INT PRIMARY KEY AUTO_INCREMENT,
    url VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE recipes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    photo VARCHAR(100),
    url_id INT NOT NULL,
    type_id INT
    -- FOREIGN KEY (url_id) REFERENCES recipe_url(id),
    -- FOREIGN KEY (type_id) REFERENCES types(id)
);

# TODO finish tables

CREATE TABLE types (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL UNIQUE
);
