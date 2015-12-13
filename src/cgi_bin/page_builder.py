#!/usr/bin/python
# -*- coding: utf-8 -*-

""" The page builder module which create pages to display or save """

from ConfigParser import SafeConfigParser
from string import Template
from db.db_module import db_execute_out
from bs4 import BeautifulSoup as parse

CONFIG_FILE = 'config.txt'

def create_recipe_list(recipe_list):
    """
    Create a web page content from the database rows of recipes
    @param recipe_list list of dictionnaries containing the recipes' informations
    and ingredients
    @return a string containing the recipe list in a html format
    """
    config = SafeConfigParser()
    config.read(CONFIG_FILE)

    _fd = open(config.get('html', 'recipe_panel'))
    recipe_panel = _fd.read()
    _fd.close()

    soup = parse('<div></div>', 'lxml')
    panel_group = soup.div
    panel_group['class'] = 'panel-group'
    panel_group['id'] = 'recipe_list'
    panel_group['role'] = 'tablist'
    panel_group['aria-multiselectable'] = 'false'

    # creating a panel for each recipe
    for recipe in recipe_list:
        panel = parse(recipe_panel, 'lxml')
        for i in panel.select('div#$id'):
            i['id'] = str(recipe['id'])
        for i in panel.select('div#id_head'):
            i['id'] = str(recipe['id'])+'_head'

        img = panel.select('img#$id_img')[0]
        img['id'] = str(recipe['id'])+'_img'
        img['src'] = recipe['img']
        img['width'] = '90%'
        img['height'] = '90%'

        title = panel.select('a#$id_title')[0]
        title['id'] = str(recipe['id'])+'_title'
        title['href'] = '#'+str(recipe['id'])
        title['aria-controls'] = str(recipe['id'])
        title.string = recipe['name']

        ingr_list = panel.select('ul#$id_ingredients')[0]
        ingr_list['id'] = str(recipe['id'])+'_ingredients'
        for _ingr in recipe['ingredients']:
            ingr_li = soup.new_tag('li')
            ingr_li['class'] = 'list-group-item'
            ingr_li.string = _ingr
            ingr_list.append(ingr_li)

        url = panel.select('a#$id_url')[0]
        url['id'] = str(recipe['id'])+'_url'
        url['href'] = recipe['url']

        opinion_list = panel.select('ul#$id_opinions')[0]
        opinion_list['id'] = str(recipe['id'])+'_opinions'
        for _opinion in recipe['opinions']:
            opinion_li = soup.new_tag('li')
            opinion_li['class'] = 'list-group-item'
            opinion_li.string = """{0} gives {1}/5 : \"{2}\"
            """.format(_opinion['author'], _opinion['mark'], _opinion['comment'])
            opinion_list.append(opinion_li)

        panel_group.append(panel)

    return soup.prettify(formatter='html')


def display(_content):
    """
    display the template with the modified content
    @param _content a dictionnary {title, left, middle, right}
    """
    config = SafeConfigParser()
    config.read(CONFIG_FILE)
    _fd = open(config.get('html', 'template_path'))
    template = Template(_fd.read())
    _fd.close()
    result = template.safe_substitute(
        title=_content["title"],
        middle=_content["middle"],
        left=_content["left"],
        right=_content["right"]
    )
    print "Content-type: text/html; charset=utf-8\n\n"
    print result


def save_page(_content, _output):
    """
    generate a file and save it to the _output file specified
    @param _content a dictionnary {title, left, middle, right}
    @param _output the path to save file to save into
    """
    config = SafeConfigParser()
    config.read(CONFIG_FILE)
    _fd = open(config.get('html', 'template_path'))
    template = Template(_fd.read())
    _fd.close()
    result = template.safe_substitute(
        title=_content["title"],
        middle=_content["middle"],
        left=_content["left"],
        right=_content["right"]
    )
    open(_output, 'w').write(result)


def add_options_to_form(table_name, form, tag_id):
    """
    Add in the form having the id tag_id the content of the two first rows
    of the table_name given (id and name typically)
    @param table_name the name of the table
    @param form       an option in the config file containing the path to an html file
    @param tag_id     the tag id in the form (exemple : select#type)
    """
    config = SafeConfigParser()
    config.read(CONFIG_FILE)
    # adding types to the search form
    types = db_execute_out("SELECT * FROM "+ table_name +" ORDER BY name;")
    form_path = config.get('html', form)
    _fd = open(form_path)
    soup = parse(_fd.read(), "lxml")
    _fd.close()

    soup.select(tag_id)[0].string = ''
    for row in types:
        opt = soup.new_tag('option')
        opt.string = row[1]
        opt['value'] = row[0]
        soup.select(tag_id)[0].append(opt)

    # writing the html file
    html = soup.prettify(formatter='html')
    with open(form_path, "wb") as _fd:
        _fd.write(html)


def get_content(_file):
    """
    Return the content of the web page inside the body tags
    @param _file an option in the config file containing the path to an html file
    @return the content of the body tags in the html file
    """
    config = SafeConfigParser()
    config.read(CONFIG_FILE)
    _fd = open(config.get('html', _file), 'r')
    soup = parse(_fd.read(), "lxml")
    return soup.find('body').prettify(formatter='html')
