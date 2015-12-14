import operator
import os
import sqlite3
from db.db_module import db_execute_out

'''
Create the statement to get last preferred ingredients
serched by the current user
@var id_user int
@var n_max int
@return string
'''
def get_select_last_preferred_ingredients(id_user, n_max):
    request = 'SELECT i.idIngr '
    request += 'FROM users u '
    request += 'LEFT JOIN search s ON u.id = s.user_id '
    request += 'LEFT JOIN search_has_ingredient si ON s.id = si.idSearch '
    request += 'WHERE u.id = id_user '
    if not n_max == 0:
        request += 'LIMIT '+str(n_max)
    return request

'''
Create the statement to searched recipes who contains
at least one ingredients researched by the current user
@var id_recipe_types int list
@var id_ingredients int list
@var n_max int
@return string
'''
def get_select_recipes(id_recipe_types, id_ingredients, n_max):
    request = 'SELECT r.id, ri.idIngr '
    request += 'FROM recipes AS r '
    request += 'LEFT JOIN recipe_has_ingredients AS ri ON r.id = ri.idRecipe '
    if id_recipe_types == [] and id_ingredients == []:
        return request
    request += 'WHERE '
    if not id_recipe_types == []:
        request += '(r.type_id='+id_recipe_types[0]+' '
        for recipe_type in id_recipe_types:
            request += 'OR r.type_id='+recipe_type+' '
        request += ') '
    if not id_recipe_types == [] and not id_ingredients == []:
        request += 'AND '
    if not id_ingredients == []:
        request += '(ri.idIngr='+id_ingredients[0]+' '
        for ingredient in id_ingredients:
            request += 'OR ri.idIngr='+ingredient+' '
        request += ') '
    if not n_max == 0:
        request += 'LIMIT '+str(n_max)
    return request

'''
Get recommander recipes to an user
@var id_user int
@var id_recipe_types int list
@var id_wanted_ingredients int list
@var id_refused_ingredients int list
@return list
'''
def get_recipes(id_user, id_recipe_types, id_wanted_ingredients, id_refused_ingredients):
    weights = {}
    weights['default'] = 0
    weights['wanted_ingredients'] = 2
    weights['past_wanted_ingredients'] = 1
    weights['refused_ingredients'] = -2

    # Get recipes from database
    selectRecipes = db_execute_out(get_select_recipes(id_recipe_types, id_wanted_ingredients, 0))

    # Create a dict to put together ingredients to the same recipe
    recipes = {}
    for recipe in selectRecipes:
        if(not recipes.has_key(recipe[0])):
            recipes[recipe[0]] = {}
            recipes[recipe[0]]['id'] = recipe[0]
            recipes[recipe[0]]['ingredients'] = []
        recipes[recipe[0]]['ingredients'].append(recipe[1])

    # Find the past ingredients preferred already searched in the past
    id_past_ingredients = []
    id_past_ingredients = get_select_last_preferred_ingredients(id_user, 10)

    # Compute the weight of each recipe
    listRecipeWeight = []
    for key in recipes:
        recipe = recipes[key]
        recipe['weights'] = [weights['default']] * len(recipe['ingredients'])
        for ingredient in id_wanted_ingredients:
            if ingredient in recipe['ingredients']:
                recipe['weights'][recipe['ingredients'].index(ingredient)] = weights['wanted_ingredients']
        for ingredient in id_past_ingredients:
            if ingredient in recipe['ingredients']:
                recipe['weights'][recipe['ingredients'].index(ingredient)] = weights['past_wanted_ingredients']
        for ingredient in id_refused_ingredients:
            if ingredient in recipe['ingredients']:
                recipe['weights'][recipe['ingredients'].index(ingredient)] = weights['refused_ingredients']
        recipe['weight'] = 0
        for i in recipe['weights']:
            recipe['weight'] += i
        listRecipeWeight.append((recipe['id'],recipe['weight']))

    # Sort recipes to get the must of recipes
    listRecipeWeight.sort(key = operator.itemgetter(1), reverse = True)

    # Get just id recipes to return
    idRecipes, w = map(list, zip(*listRecipeWeight))

    # Return recipes
    return idRecipes
