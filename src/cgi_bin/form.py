#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Script used to retrieve infos from the form, format the informations,
give them to the recommandation engine and display the result
"""

import cgi
import cgitb
from page_builder import display, create_recipe_list, create_favs, create_opinions
from db.db_module import add_user, db_execute_in
from formatter import format_recipes, format_form_result
# from r_engine import recommander
from recommandation_engine import get_recipes
cgitb.enable()

# Retrieving informations from the form
FORM = cgi.FormContentDict()

# insert user into database and get user id
MAIL = FORM['email'][0]
USER_ID = str(add_user(MAIL)[0])

# adding a search for the user
REQ = "INSERT INTO search(user_id, recipe_id) VALUES ({}, NULL);".format(USER_ID)
db_execute_in([REQ])

# format the informations for the recommandation engine
CLEAN_FORM = format_form_result(FORM, USER_ID)

# getting the recommandation for the user
# RECOMMANDATION = recommander(CLEAN_FORM)
RECOMMANDATION = get_recipes(
    CLEAN_FORM['user_id'],
    CLEAN_FORM['recipe_type'],
    CLEAN_FORM['ingr_like'],
    CLEAN_FORM['ingr_dislike']
)

# formatting the result to display it
RESULT = format_recipes(RECOMMANDATION)

# create the list of opinions
OPINIONS = create_opinions(USER_ID)

# create the favorite list
FAVS = create_favs(USER_ID)

CONTENT = {
    'title': '{} Recipes found !'.format(str(len(RESULT))),
    'middle': create_recipe_list(RESULT, USER_ID),
    'left': OPINIONS,
    'right': FAVS
}

display(CONTENT)
