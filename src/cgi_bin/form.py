#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Script used to retrieve infos from the form, format the informations,
give them to the recommandation engine and display the result
"""

import cgi
import cgitb
from page_builder import display, create_recipe_list
from db.db_module import add_user
from formatter import format_recipes
from r_engine import recommander
cgitb.enable()

# Retrieving informations from the form
FORM = cgi.FormContentDict()

# insert user into database and get user id
MAIL = FORM['email'][0]
USER_ID = add_user(MAIL)

# getting the recommandation for the user
RECOMMANDATION = recommander()

# formatting the result to display it
RESULT = format_recipes(RECOMMANDATION)

# TODO getting the recipes to comment list
# TODO formatting the form to display them on the left

# TODO getting the favorite recipes of the user
# TODO formatting them to display them on the right part

FORMATTED_FORM = []

CONTENT = {
    'title': '{} Recipes found !'.format(str(len(RESULT))),
    'middle': create_recipe_list(RESULT),
    'left': '',
    'right': FORM
}

display(CONTENT)
