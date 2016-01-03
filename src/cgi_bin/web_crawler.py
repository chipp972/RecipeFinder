#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Functions to browse url to determine if there is a recipe
on the web page and to retrieve the ingredients needed and
various informations
"""

import unicodedata

import urllib2
from bs4 import BeautifulSoup as parse
import re
from db.db_module import db_execute_in, db_execute_out
from page_builder import add_options_to_form

with open('db/mots_francais.txt') as _fd:
    FRENCH_DICTIONNARY = _fd.read().split('\n')

def clean_ingredients(_li):
    """
    clean the ingredients list
    @param _li a list of string containing ingredient names
    @return the list of ingredient cleaned up
    """
    new_list = []
    for i in _li:
        i = i.lower()
        i = re.sub(r'  ', '', i)
        i = re.sub(r'<.*?>', '', i)
        i = re.sub(r'\n', '', i)
        i = re.sub(r'.*:\r', '', i)
        i = re.sub(r'[(].*[)]', '', i)
        i = re.sub(r'\"', '', i)
        i = re.sub(r'.*[0-9]+ ?k?g? ', '', i)
        i = re.sub(r'.*de ', '', i)
        i = re.sub(r'.*d\'', '', i)
        i = re.sub(r' $', '', i)
        i = re.sub(r'^-? ', '', i)
        if i != '':
            new_list.append(i)
    return new_list

def determine_type(title):
    """
    determine the type of the recipe according to keywords found in it
    @param title the title of a recipe
    @return the type of recipe
    """
    std_title = title.lower()

    entree_kw = [
        'salade', 'soupe'
    ]
    main_dish_kw = [
        'gratin', 'boeuf', 'poulet', 'filet', 'saumon', 'thon', 'porc',
        'fromage', 'foie', 'gras', 'canard', 'dinde', 'fondue', 'volaille'
    ]
    dessert_kw = [
        'gateau', 'tiramisu', 'creme', 'caramel', 'sucre', 'chocolat',
        'vanille', 'fraise', 'poire', 'banane', 'tarte'
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
    """
    Retrieve a web page and get informations from it
    @param url the url of the web page to analyze
    @param base the base url of the web site
    @return a dictionnary containing all the informations of a recipe or just
            the urls found on the page and the url of the page :
            {url, name, img, type, ingredients, add_urls} or
            {url, add_urls}
    """
    web_page = urllib2.urlopen(url)
    html = web_page.read()

    soup = parse(html.decode('utf8', 'replace'), "lxml")

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

    # image on marmiton
    _img = ''
    for i in soup.find_all('a'):
        if i.get('class') == ['m_content_recette_illu']:
            _img = i.findChildren()[0].get('src')

    if len(ingr_list) == 0 or _img == '':
        return {
            'url': url,
            'add_urls': _urls
        }

    # title on marmiton
    title = soup.title.string
    title = re.sub(r'[\r|\n|\t]*', '', title)
    title = re.sub(r'\"', '', title)
    title = unicodedata.normalize('NFD', title).encode('utf8', 'ignore')


    # type
    _type = determine_type(title)

    return {
        'url': url,
        'name': title,
        'img': _img,
        'type': _type,
        'ingredients': ingr_list,
        'add_urls': _urls
    }

def get_recipe_request(recipe_info):
    """
    Create a sql request to insert a recipe into the database
    @param recipe_info a dictionnary containing the recipe informations
    @return the sql request to insert a recipe into the database
    """
    req = """INSERT INTO recipes(name, url, photo_url, type_id)
    VALUES(\"{0}\", \"{1}\", \"{2}\", \"{3}\");
    """.format(recipe_info['name'], recipe_info['url'], recipe_info['img'], recipe_info['type'])
    return str(req)

def get_ingr_request(ingredient):
    """
    Create a sql request to insert an ingredient into the database
    @param ingredient a string which is the ingredient name
    @return the sql request to insert an ingredient into the database
    """
    req = """INSERT INTO ingredients(name)
    VALUES(\"{0}\");""".format(ingredient)
    return str(req)

def get_recipe_ingr_request(recipe_info_list):
    """
    Create a sql request to link recipes with ingredients in the database
    @param recipe_info_list list of dictionnary containing recipe informations :
    [{url, img, ingredients, ...}, {...}, ...]
    @return the sql requests to insert in the table recipe_has_ingredients
    """
    req = []
    for recipe in recipe_info_list:
        recipe_id = db_execute_out("SELECT id FROM recipes WHERE url=\"{}\";".format(recipe['url']))
        recipe_id = recipe_id[0][0]
        for _ingr in recipe['ingredients']:
            ingr_id = db_execute_out("SELECT id FROM ingredients WHERE name=\"{}\";".format(_ingr))
            ingr_id = ingr_id[0][0]
            req.append("""
                INSERT INTO recipe_has_ingredients
                VALUES (\"{0}\", \"{1}\");""".format(recipe_id, ingr_id))
    return req


def web_crawler(enter_url, limit=20):
    """
    Get recipes and insert them in the database with ingredients
    @param enter_url base url of a web site (http://marmiton.org)
    @param limit limit number of recipes before ending the search
    """
    _base = enter_url
    url_to_treat = [enter_url] # the list of url to treat
    url_treated = [] # th list of url treated
    requests = [] # contains the requests to insert recipes and ingredients
    ingr_list = [] # contains the ingredient list
    recipe_info_list = []
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
            # put the type id instead of the name of the id
            res['type'] = type_id[res['type']]
            # add the sql request to insert the recipe in the list of requests
            requests.append(get_recipe_request(res))
            # add the sql request for the ingredients
            for _ingr in res['ingredients']:
                if _ingr not in ingr_list:
                    requests.append(get_ingr_request(_ingr))
                    ingr_list.append(_ingr)
            # showing the number of recipes found
            recipe_found += 1
            print '{0}/{1} recipes found'.format(str(recipe_found), str(limit))
            # keep recipes info to add to recipe_has_ingredients table
            recipe_info_list.append(res)

        # Adding urls to the stack of urls to treat
        url_treated.append(res['url'])
        for i in res['add_urls']:
            if i not in url_treated and i not in url_to_treat:
                url_to_treat.append(i)

    # recording all the recipes and ingredients in the database
    db_execute_in(requests)
    add_options_to_form('ingredients', 'search_form_path', 'select#ingr-like')
    add_options_to_form('ingredients', 'search_form_path', 'select#ingr-dislike')
    requests = get_recipe_ingr_request(recipe_info_list)
    db_execute_in(requests)
