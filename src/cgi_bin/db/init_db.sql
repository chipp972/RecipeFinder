CREATE TABLE url_to_treat (
    id INTEGER PRIMARY KEY,
    url TEXT NOT NULL UNIQUE
);

CREATE TABLE no_recipe_url (
    id INTEGER PRIMARY KEY,
    url TEXT NOT NULL UNIQUE
);

CREATE TABLE recipe_url (
    id INTEGER PRIMARY KEY,
    url TEXT NOT NULL UNIQUE
);

CREATE TABLE types (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE recipes (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    photo TEXT,
    url_id INTEGER NOT NULL,
    type_id INTEGER,
    FOREIGN KEY (url_id) REFERENCES recipe_url(id),
    FOREIGN KEY (type_id) REFERENCES types(id)
);

CREATE TABLE ingredients (
	id INTEGER PRIMARY KEY,
	name TEXT
);

CREATE TABLE users(
	id INTEGER PRIMARY KEY,
	email TEXT,
	password TEXT
);

CREATE TABLE opinions(
	id INTEGER PRIMARY KEY,
	mark INTEGER,
	comment TEXT,
	author INTEGER,
    recipe INTEGER,
	FOREIGN KEY (author) REFERENCES users(id),
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
