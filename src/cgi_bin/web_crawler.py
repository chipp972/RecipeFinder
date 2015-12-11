"""  Functions to browse url to determine if there is a recipe
on the web page and to retrieve the ingredients needed and
various informations """
#!/usr/bin/python
# -*- coding: utf-8 -*

import unicodedata
import urllib2
from bs4 import BeautifulSoup as parse
import re
from db.db_module import db_execute_in

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
        # i = re.sub(r'\"', '', i)
        i = re.sub(r'.*[0-9]+ ?k?g? ', '', i)
        i = re.sub(r'.*de ', '', i)
        i = re.sub(r'.*d\'', '', i)
        i = re.sub(r' $', '', i)
        i = re.sub(r'^-? ', '', i)
        if i != '':
            new_list.append(i)
    return new_list

def determine_type(title):
    """ return the type of the recipe """
    # TODO import keywords from a file
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

def insert_recipe(recipe_info):
    """ Insert a recipe into the database """
    req = """INSERT INTO recipes(name, url, photo_url, type_id)
    VALUES(\"{0}\", \"{1}\", \"{2}\", \"1\");
    """.format(recipe_info['name'], recipe_info['url'], recipe_info['img'])
    db_execute_in([str(req)])
    # TODO add ingredients
    # TODO modify the search form adding the ingredients

def web_crawler(enter_url, limit=1000):
    """ main function of the web crawler :
    manage the inputs in the database and the stack of urls
    limit is the number of recipe we get before we stop the search """
    # TODO for the type_id resolve the id of each type first
    # add ingredients
    _base = enter_url
    url_to_treat = [enter_url]
    url_treated = []
    recipe_found = 0
    while len(url_to_treat) > 0 and recipe_found < limit:
        try:
            res = get_recipe(url_to_treat.pop(), _base)
        except urllib2.HTTPError:
            pass
        except KeyboardInterrupt:
            break

        # print res['url']

        # recording the recipe in the database
        if 'name' in res.keys():
            insert_recipe(res)
            recipe_found += 1

        # Adding urls to the stack of urls to treat
        url_treated.append(res['url'])
        for i in res['add_urls']:
            if i not in url_treated and i not in url_to_treat:
                url_to_treat.append(i)
