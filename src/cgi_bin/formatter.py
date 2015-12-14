#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
script containing functions to format the informations
given by the database into well formed lists and dictionnaries
"""

from db.db_module import db_execute_out
import unicodedata

def format_recipes(recipe_list):
    """
    retrieve recipes in the database and format them in dictionnaries
    @param recipe_list a list string containing recipe's ids
    @return a lit of dictionnaries containing recipes :
    [{id, name, url, img, ingredients, opinions}, {...}, ...]
    """
    if recipe_list == []:
        return []
    _req = """
        SELECT recipes.id, recipes.name, recipes.url, recipes.photo_url
        FROM recipes
        WHERE recipes.id LIKE \"{}\"
    """.format(recipe_list.pop())
    for i in recipe_list:
        _req += 'OR recipes.id LIKE \"{}\"'.format(i)
    _req += ';'

    rows = db_execute_out(_req)

    result = []
    for _row in rows:
        # general informations
        recipe = {
            'id': _row[0],
            'name': unicodedata.normalize('NFD', _row[1]).encode('ascii', 'ignore'),
            'url': unicodedata.normalize('NFD', _row[2]).encode('ascii', 'ignore'),
            'img': unicodedata.normalize('NFD', _row[3]).encode('ascii', 'ignore'),
            'ingredients': [],
            'opinions': []
        }

        if recipe['img'] == '':
            recipe['img'] = 'https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg'

        # adding ingredients
        ingredient_rows = db_execute_out("""
            SELECT ingredients.name
            FROM ingredients
            INNER JOIN recipe_has_ingredients
            ON ingredients.id LIKE recipe_has_ingredients.idIngr
            WHERE recipe_has_ingredients.idRecipe LIKE \"{}\";
        """.format(_row[0]))
        for _ingr in ingredient_rows:
            recipe['ingredients'].append(
                unicodedata.normalize('NFD', _ingr[0]).encode('ascii', 'ignore'))

        # adding opinions
        opinion_rows = db_execute_out("""
            SELECT opinions.mark, opinions.comment, users.email
            FROM opinions
            INNER JOIN users ON opinions.author LIKE users.id
            WHERE opinions.author LIKE \"{}\";
        """.format(_row[0]))
        for _op in opinion_rows:
            recipe['opinions'].append({
                'mark': _op[0],
                'comment': unicodedata.normalize('NFD', _op[1]).encode('ascii', 'ignore'),
                'author': unicodedata.normalize('NFD', _op[2]).encode('ascii', 'ignore')
            })
        # adding the recipe to the list
        result.append(recipe)
    return result


def format_form_result(form, user_id):
    """
    format the form result and return a clean dictionnary
    @param form the form from cgi.FormContentDict()
    @param user_id the user_id in a tuple retrieved from the database
    @return a clean dictionnary
    """
    formated_form = {
        'user_id': user_id,
        'weighing': form['weighing'][0],
        'recipe_type': form['type'][0],
        'ingr_like': form['ingr-like'],
    }
    if 'ingr-dislike' in form.keys():
        formated_form['ingr_dislike'] = form['ingr-dislike']
    else:
        formated_form['ingr_dislike'] = []
    return formated_form
