CREATE TABLE types (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE recipes (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    url TEXT NOT NULL,
    photo TEXT,
    type_id INTEGER NOT NULL,
    FOREIGN KEY (type_id) REFERENCES types(id)
);

CREATE TABLE ingredients (
	id INTEGER PRIMARY KEY,
	name TEXT
);

CREATE TABLE users(
	id INTEGER PRIMARY KEY,
	email TEXT NOT NULL,
);

CREATE TABLE search(
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    recipe_id INTEGER NOT NULL,
    recipe_position INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (recipe_id) REFERENCES recipes(id)
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

CREATE TABLE user_has_favorite_recipes(
	idUser INTEGER,
	idRecipe INTEGER,
	PRIMARY KEY (idUser, idRecipe),
	FOREIGN KEY (idUser) REFERENCES users(id),
	FOREIGN KEY (idRecipe) REFERENCES recipes(id)
);

CREATE TABLE search_has_ingredients(
	idSearch INTEGER,
	idIngr INTEGER,
	PRIMARY KEY (idSearch, idIngr),
	FOREIGN KEY (idSearch) REFERENCES search(id),
	FOREIGN KEY (idIngr) REFERENCES ingredients(id)
);

CREATE TABLE search_has_not_ingredients(
	idSearch INTEGER,
	idIngr INTEGER,
	PRIMARY KEY (idSearch, idIngr),
	FOREIGN KEY (idSearch) REFERENCES search(id),
	FOREIGN KEY (idIngr) REFERENCES ingredients(id)
);
