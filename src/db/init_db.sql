# Script to initialize the database

DROP TABLE if exists url_to_treat;
DROP TABLE if exists no_recipe_url;
DROP TABLE if exists recipe_url;
DROP TABLE if exists types;
DROP TABLE if exists recipes;
DROP TABLE if exists ingredients;
DROP TABLE if exists users;
DROP TABLE if exists opinions;
DROP TABLE if exists recipe_has_ingredients;
DROP TABLE if exists user_currently_has_ingredient;
DROP TABLE if exists user_has_favorite_ingredient;
DROP TABLE if exists user_has_forbidden_ingredient;

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

CREATE TABLE ingredients (
	id INT PRIMARY KEY AUTO_INCREMENT,
	name VARCHAR(100)
);

CREATE TABLE users(
	id INT PRIMARY KEY AUTO_INCREMENT,
	email VARCHAR(100),
	name VARCHAR(100),
	birth DATE
);

CREATE TABLE opinions(
	id INT PRIMARY KEY AUTO_INCREMENT,
	mark INT,
	comment VARCHAR(100),
	author INTEGER,
		FOREIGN KEY (author) REFERENCES users(id),
	recipe INTEGER,
		FOREIGN KEY (recipe) REFERENCES recipes(id)
);

CREATE TABLE recipe_has_ingredients(
	idRecipe INTEGER,
	idIngr INTEGER,
	PRIMARY KEY (idRecipe, idIngr),
	FOREIGN KEY (idRecipe) REFERENCES recipes(id),
	FOREIGN KEY (idIngr) REFERENCES ingredients(id)
);

CREATE TABLE user_currently_has_ingredient(
	idUser INTEGER,
	idIngr INTEGER,
	PRIMARY KEY (idUser, idIngr),
	FOREIGN KEY (idUser) REFERENCES users(id),
	FOREIGN KEY (idIngr) REFERENCES ingredients(id)
);

CREATE TABLE user_has_favorite_ingredient(
	idUser INTEGER,
	idIngr INTEGER,
	PRIMARY KEY (idUser, idIngr),
	FOREIGN KEY (idUser) REFERENCES users(id),
	FOREIGN KEY (idIngr) REFERENCES ingredients(id)
);

CREATE TABLE user_has_forbidden_ingredient(
	idUser INTEGER,
	idIngr INTEGER,
	PRIMARY KEY (idUser, idIngr),
	FOREIGN KEY (idUser) REFERENCES users(id),
	FOREIGN KEY (idIngr) REFERENCES ingredients(id)
);
