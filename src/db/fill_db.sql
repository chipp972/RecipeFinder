-- users
INSERT INTO users VALUES (1, 'user0@gmail.com');

INSERT INTO users VALUES (2, 'user1@gmail.com');

INSERT INTO users VALUES (3, 'user2@gmail.com');

-- favorites
INSERT INTO user_has_favorite_recipes VALUES (1, 3);

INSERT INTO user_has_favorite_recipes VALUES (2, 4);

INSERT INTO user_has_favorite_recipes VALUES (2, 5);

INSERT INTO user_has_favorite_recipes VALUES (2, 6);

INSERT INTO user_has_favorite_recipes VALUES (3, 5);

INSERT INTO user_has_favorite_recipes VALUES (3, 6);

INSERT INTO user_has_favorite_recipes VALUES (3, 7);

INSERT INTO user_has_favorite_recipes VALUES (3, 9);

INSERT INTO user_has_favorite_recipes VALUES (3, 11);

INSERT INTO user_has_favorite_recipes VALUES (3, 18);

INSERT INTO user_has_favorite_recipes VALUES (2, 13);

INSERT INTO user_has_favorite_recipes VALUES (3, 12);

INSERT INTO user_has_favorite_recipes VALUES (3, 17);

INSERT INTO user_has_favorite_recipes VALUES (2, 17);

INSERT INTO user_has_favorite_recipes VALUES (1, 17);

INSERT INTO user_has_favorite_recipes VALUES (1, 16);

-- searchs
INSERT INTO search(user_id, recipe_id) VALUES (1, 1);

INSERT INTO search(user_id, recipe_id) VALUES (1, 2);

-- opinions
INSERT INTO opinions(mark, comment, author, recipe_id) VALUES (5, 'bof bof', 3, 4);

INSERT INTO opinions(mark, comment, author, recipe_id) VALUES (5, 'trop bon', 2, 3);
