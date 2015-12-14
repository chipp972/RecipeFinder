#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Script used to retrieve infos from the form, format the informations,
give them to the recommandation engine and display the result
"""

import cgi
import cgitb
from page_builder import display, create_recipe_list, create_favs
from db.db_module import add_user
from formatter import format_recipes, format_form_result
# from r_engine import recommander
from recommandation_engine import get_recipes
cgitb.enable()

# Retrieving informations from the form
FORM = cgi.FormContentDict()

# insert user into database and get user id
MAIL = FORM['email'][0]
USER_ID = str(add_user(MAIL)[0])

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

# TODO getting the recipe list to comment
# TODO formatting the form to display them on the left

# create the favorite list
FAVS = create_favs(USER_ID)

CONTENT = {
    'title': '{} Recipes found !'.format(str(len(RESULT))),
    'middle': create_recipe_list(RESULT),
    'left': CLEAN_FORM,
    'right':FAVS
}

display(CONTENT)
