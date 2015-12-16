#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Script used to retrieve infos from the form, format the informations,
give them to the recommandation engine and display the result
"""

import cgi
import cgitb
from db.db_module import db_execute_in
# from formatter import format_recipes, format_form_result
# from r_engine import recommander
import re
cgitb.enable()

# Retrieving informations from the form
FORM = cgi.FormContentDict()

# search : add recipe_id
if 'search' in FORM.keys():
    RECI_ID = re.sub(r'_url', '', FORM['search'][0])
    REQ = """
        UPDATE search
        SET recipe_id={0}
        WHERE user_id={1} AND recipe_id IS NULL;
    """.format(RECI_ID.split('_')[1], RECI_ID.split('_')[0])
    db_execute_in([REQ])

# fav
if 'fav' in FORM.keys():
    FAV_ID = re.sub(r'fav_', '', FORM['fav'][0])
    REQ = """
        INSERT INTO user_has_favorite_recipes
        VALUES ({}, {});
    """.format(FAV_ID.split('_')[0], FAV_ID.split('_')[1])
    db_execute_in([REQ])

# unfav
if 'unfav' in FORM.keys():
    UNFAV_ID = re.sub(r'unfav_', '', FORM['unfav'][0])
    REQ = """
        DELETE FROM user_has_favorite_recipes
        WHERE idUser={} AND idRecipe={};
    """.format(UNFAV_ID.split('_')[0], UNFAV_ID.split('_')[1])
    db_execute_in([REQ])


# post opinion
if 'mark' in FORM.keys():
    REQ = """
        INSERT INTO opinions(mark, comment, author, recipe_id)
        VALUES ({}, \"{}\", {}, {});
    """.format(
        FORM['mark'][0],
        FORM['comment'][0],
        FORM['user_id'][0],
        FORM['recipe_id'][0]
    )
    db_execute_in([REQ])
