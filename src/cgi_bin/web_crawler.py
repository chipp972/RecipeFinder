"""  Functions to browse url to determine if there is a recipe
on the web page and to retrieve the ingredients needed and
various informations """
#!/usr/bin/python
# -*- coding: utf-8 -*

import unicodedata
import urllib2
from bs4 import BeautifulSoup as parse
import re
from db.db_module import db_execute_in, db_execute_out, add_options_to_form


def clean_ingredients(_li):
    """ clean the ingredient list """
    new_list = []
    for i in _li:
        i = re.sub(r'  ', '', i)
        i = re.sub(r'<.*?>', '', i)
        i = re.sub(r'\n', '', i)
        i = unicode(i, 'utf-8')
        i = unicodedata.normalize('NFD', i).encode('ascii', 'ignore')
        i = re.sub(r'.*:\r', '', i)
        i = re.sub(r'[(].*[)]', '', i)
        i = re.sub(r'\"', '', i)
        i = re.sub(r'.*[0-9]+ ?k?g? ', '', i)
        i = re.sub(r'.*de ', '', i)
        i = re.sub(r'.*d\'', '', i)
        i = re.sub(r' $', '', i)
        i = re.sub(r'^-? ', '', i)
        i = i.lower()
        if i != '':
            new_list.append(i)
    return new_list

def determine_type(title):
    """ return the type of the recipe """
    std_title = title.lower()

    entree_kw = [
        'salade', 'soupe'
    ]
    main_dish_kw = [
        'gratin', 'boeuf', 'poulet', 'filet', 'saumon', 'thon', 'porc',
        'fromage', 'foie', 'gras', 'canard', 'dinde', 'fondue'
    ]
    dessert_kw = [
        'gateau', 'tiramisu', 'creme', 'caramel', 'sucre', 'chocolat',
        'vanille', 'fraise', 'poire', 'banane'
    ]
    for i in entree_kw:
        if i in std_title:
            return 'entree'
    for i in main_dish_kw:
        if i in std_title:
            return 'main_dish'
    for i in dessert_kw:
        if i in std_title:
            return 'dessert'
    return 'other'

def get_recipe(url, base):
    """ takes a url and a base url and return a dictionnary """
    web_page = urllib2.urlopen(url)
    html = web_page.read()

    soup = parse(html, "lxml")

    # urls on marmiton
    _urls = []
    for i in soup.find_all('a'):
        curr_url = i.get('href')
        if curr_url is not None:
            if base+'recettes/' in curr_url:
                _urls.append(curr_url)

    # ingredients on marmiton
    ingr_list = []
    for i in soup.find_all('div'):
        if i.get('class') is not None:
            if 'm_content_recette_ingredients' in i.get('class'):
                ingr_list = str(i).split('<br/>')
                ingr_list = clean_ingredients(ingr_list)

    if len(ingr_list) == 0:
        return {
            'url': url,
            'add_urls': _urls
        }

    # title on marmiton
    title = soup.title.string
    title = re.sub(r'[\r|\n|\t]*', '', title)
    title = re.sub(r'\"', '', title)
    title = unicodedata.normalize('NFD', title).encode('ascii', 'ignore')


    # type
    _type = determine_type(title)

    # image on marmiton
    _img = ''
    for i in soup.find_all('a'):
        if i.get('class') == ['m_content_recette_illu']:
            _img = i.findChildren()[0].get('src')

    return {
        'url': url,
        'name': title,
        'img': _img,
        'type': _type,
        'ingredients': ingr_list,
        'add_urls': _urls
    }

def get_recipe_request(recipe_info):
    """ Return the sql request to insert a recipe into the database """
    req = """INSERT INTO recipes(name, url, photo_url, type_id)
    VALUES(\"{0}\", \"{1}\", \"{2}\", \"{3}\");
    """.format(recipe_info['name'], recipe_info['url'], recipe_info['img'], recipe_info['type'])
    return str(req)

def get_ingr_request(ingredient):
    """ Return the sql request to insert an ingredient into the database """
    req = """INSERT INTO ingredients(name)
    VALUES(\"{0}\");""".format(ingredient)
    return str(req)

def web_crawler(enter_url, limit=2000):
    """ main function of the web crawler :
    manage the inputs in the database and the stack of urls
    limit is the number of recipe we get before we stop the search """
    _base = enter_url
    url_to_treat = [enter_url] # the list of url to treat
    url_treated = [] # th list of url treated
    recipes_to_insert = [] # contains the requests to insert recipes
    ingredients_to_insert = [] # contains the requests to insert ingredients
    ingr_list = [] # contains the ingredient list
    recipe_found = 0

    # Create a dictionnary with all the recipe types and their id
    type_id = {}
    for row in db_execute_out("SELECT * FROM types"):
        type_id[row[1]] = row[0]

    while len(url_to_treat) > 0 and recipe_found < limit:
        try:
            # get the recipe in a dictionnary
            res = get_recipe(url_to_treat.pop(), _base)
        except urllib2.HTTPError:
            pass

        # insert the sql request to add the recipe in the list
        if 'name' in res.keys():
            res['type'] = type_id[res['type']] # on met l'id du type
            recipes_to_insert.append(get_recipe_request(res))
            for _ingr in res['ingredients']:
                if _ingr not in ingr_list:
                    ingredients_to_insert.append(get_ingr_request(_ingr))
                    ingr_list.append(_ingr)
            recipe_found += 1

        # Adding urls to the stack of urls to treat
        url_treated.append(res['url'])
        for i in res['add_urls']:
            if i not in url_treated and i not in url_to_treat:
                url_to_treat.append(i)

    # recording all the recipes and ingredients in the database
    db_execute_in(recipes_to_insert)
    db_execute_in(ingredients_to_insert)
    add_options_to_form('ingredients', 'search_form_path', 'select#ingr-like')
    add_options_to_form('ingredients', 'search_form_path', 'select#ingr-dislike')
    # TODO remplir la table recipe_has_ingredient pour chaque recette
    # en trouvant les id des recettes dans la base et les id des ignredients
    # # avec les select
