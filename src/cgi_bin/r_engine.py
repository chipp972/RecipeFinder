#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
recommandation engine script
use user opinion, user favorites or user's searchs to recommand recipes
"""

from db.db_module import db_execute_out
from formatter import format_recipes

# TODO finish recommandation engine
def recommander(form):
    """
    main class of the recommandation engine
    @param form the informations retrieved from the html form
    @return a list of string containing recipe's ids ordered
    by the recommandation
    """
    rec = {
        'weight-mark': mark_recommandation,
        'weight-fav': fav_recommandation,
        'weight-click': click_recommandation
    }
    # return rec[form['weighing']](form)
    return ['1', '2', '3', '4', '5']

def mark_recommandation(form):
    """
    - Retrieve the marks of the user and the mark of other users on the same recipes
    - compare them to determine the distance between the user and other users
    - find the recipes that the user is interested in (according to the ingredients)
      and order them in function of the opinions of "close distance" users
    @param form form informations
    @return a list of ids sorted thanks to the "opinions"
    """
    # retrieve the opinions of the users
    request = """
        SELECT DISTINCT recipes.id
        FROM recipes
        INNER JOIN recipe_has_ingredients as ingr
        ON recipes.id LIKE ingr.idRecipe
        WHERE recipes.type_id LIKE \"{0}\"
    """.format(form['recipe_type'])
    for _ingr in form['ingr_dislike']:
        request += "AND ingr.idIngr NOT LIKE \"{}\"".format(_ingr)
    request += "AND (ingr.idIngr LIKE \"{}\"".format(form['ingr_like'].pop())
    for _ingr in form['ingr_like']:
        request += "OR ingr.idIngr LIKE \"{}\"".format(_ingr)
    request += ");"

    recipe_id = db_execute_out(request)
    recipe_list = format_recipes(recipe_id)


def fav_recommandation():
    """ TODO """
    # TODO

def click_recommandation():
    """ TODO """
    #TODO
