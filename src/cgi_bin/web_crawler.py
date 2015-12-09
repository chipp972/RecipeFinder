"""  Functions to browse url to determine if there is a recipe
on the web page and to retrieve the ingredients needed and
various informations """
#!/usr/bin/python
# -*- coding: utf-8 -*

import urllib2
from bs4 import BeautifulSoup as parse
import re
from db.db_module import db_execute
# from db.db_output import get_all_recipes

URL = 'http://www.marmiton.org/'
URL = 'http://www.marmiton.org/recettes/recette_gateau-au-yaourt_12719.aspx'
URL = 'http://www.marmiton.org/recettes/recette_tiramisu-aux-fraises_14039.aspx'
# URL = 'http://www.foodnetwork.com/recipes/food-network-kitchens/classic-sugar-cookies.html'
URL = 'http://www.marmiton.org/recettes/recettes-index.aspx'

def clean_ingredients(_li):
    """ clean the ingredient list """
    new_list = []
    for i in _li:
        i = re.sub(r'  ', '', i)
        i = re.sub(r'<.*?>', '', i)
        i = re.sub(r'.*-', '', i)
        new_list.append(i)
    return new_list

def determine_type(title):
    """ return the type of the recipe """
    std_title = title.lower()

    entree_kw = [
        'salade', 'soupe'
    ]
    main_dish_kw = [
        'gratin', 'boeuf', 'poulet', 'filet', 'saumon', 'thon'
    ]
    dessert_kw = [
        'gateau', 'tiramisu', 'creme', 'caramel', 'sucre', 'chocolat', 'vanille', 'fraise'
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

def get_recipe(url):
    """ take a url and return a dictionnary containing a recipe or None """
    web_page = urllib2.urlopen(url)
    html = web_page.read()

    soup = parse(html, "lxml")

    # urls
    _urls = []
    for i in soup.find_all('a'):
        _urls.append(i.get('href'))

    # ingredients on marmiton
    ingr_list = []
    for i in soup.find_all('div'):
        if i.get('class') is not None:
            if 'm_content_recette_ingredients' in i.get('class'):
                ingr_list = str(i).split('<br/>')
                ingr_list = clean_ingredients(ingr_list)
                print ingr_list

    if len(ingr_list) == 0:
        return {
            'url': url,
            'add_urls': _urls
        }

    # title on marmiton
    title = soup.title.string
    print title

    # type
    _type = determine_type(title)
    print _type

    # image on marmiton
    for i in soup.find_all('a'):
        if i.get('class') == ['m_content_recette_illu']:
            print i.findChildren()[0].get('src')

    return {
        'url': url,
        'title': title,
        'type': _type,
        'ingredients': ingr_list,
        'add_urls': _urls
    }

def web_crawler(url):
    """ start the web crawling """
    # verify if the url contains the header


print get_recipe(URL)

# affichage des tables de la base
