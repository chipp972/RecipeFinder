"""  Functions to browse url to determine if there is a recipe
on the web page and to retrieve the ingredients needed and
various informations """
#!/usr/bin/python
# -*- coding: utf-8 -*

import unicodedata
import urllib2
from bs4 import BeautifulSoup as parse
import re
from db.db_module import db_execute
# from db.db_output import get_all_recipes

BASE = 'http://www.marmiton.org/'
URL = 'http://www.marmiton.org/recettes/recette_gateau-au-yaourt_12719.aspx'
URL = 'http://www.marmiton.org/recettes/recette_tiramisu-aux-fraises_14039.aspx'
# URL = 'http://www.foodnetwork.com/recipes/food-network-kitchens/classic-sugar-cookies.html'
URL = 'http://www.marmiton.org/recettes/recettes-index.aspx'
URL = 'http://www.marmiton.org/recettes/recette_joue-de-porc-a-la-biere_36896.aspx'

def clean_ingredients(_li):
    """ clean the ingredient list """
    new_list = []
    for i in _li:
        i = re.sub(r'  ', '', i)
        i = re.sub(r'<.*?>', '', i)
        i = re.sub(r'\n', '',i)
        i = unicode(i, 'utf-8')
        i = unicodedata.normalize('NFD',i).encode('ascii','ignore')
        i = re.sub(r'.*:\r', '',i)
        i = re.sub(r'[(].*[)]', '', i)
        #i = re.sub(r'-', r'', i)
        i = re.sub(r'.*[0-9]+ ?k?g? ', '', i)
        i = re.sub(r'.*de ', '', i)
        i = re.sub(r'.*d\'', '', i)
        i = re.sub(r' $','',i)
        i = re.sub(r'^-? ','', i)
        
        #i = re.sub(r'.* (de)? ', r'', i)
        if(i!=''):
            new_list.append(i)
    return new_list

def determine_type(title):
    """ return the type of the recipe """
    std_title = title.lower()

    entree_kw = [
        'salade', 'soupe'
    ]
    main_dish_kw = [
        'gratin', 'boeuf', 'poulet', 'filet', 'saumon', 'thon', 'porc'
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

def get_recipe(url, base):
    """ take a url and return a dictionnary containing a recipe or None """
    web_page = urllib2.urlopen(url)
    html = web_page.read()

    soup = parse(html, "lxml")

    # urls
    _urls = []
    for i in soup.find_all('a'):
        _u = i.get('href')
        if _u is not None:
            if base+'recettes/' in _u:
                _urls.append(_u)

    # ingredients on marmiton
    ingr_list = []
    for i in soup.find_all('div'):
        if i.get('class') is not None:
            if 'm_content_recette_ingredients' in i.get('class'):
                ingr_list = str(i).split('<br/>')
                ingr_list = clean_ingredients(ingr_list)
                # print ingr_list

    if len(ingr_list) == 0:
        return {
            'url': url,
            'add_urls': _urls
        }

    # title on marmiton
    title = soup.title.string
    title = re.sub(r'[\r|\n|\t]*', '', title)
    # print title

    # type
    _type = determine_type(title)
    # print _type

    # image on marmiton
    _img = ''
    for i in soup.find_all('a'):
        if i.get('class') == ['m_content_recette_illu']:
            _img = i.findChildren()[0].get('src')

    return {
        'url': url,
        'title': title,
        'img': _img,
        'type': _type,
        'ingredients': ingr_list,
        'add_urls': _urls
    }

def web_crawler(enter_url):
    """ start the web crawling """
    _base = enter_url
    url_to_treat = [enter_url]
    url_treated = []
    while len(url_to_treat) > 0 :
        try:
            res = get_recipe(url_to_treat.pop(), _base)
        except urllib2.HTTPError:
            pass
        # enregistrement dans la bdd
        print res['url']
        url_treated.append(res['url'])
        for i in res['add_urls']:
            if i not in url_treated and i not in url_to_treat:
                url_to_treat.append(i)



web_crawler(BASE)
# print get_recipe(URL, BASE)

# affichage des tables de la base
