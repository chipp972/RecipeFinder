#!/usr/bin/python
# -*- coding: utf-8 -*-

""" The page builder module which create pages to display or save """

from ConfigParser import SafeConfigParser
from string import Template
from db.db_module import db_execute_out
from bs4 import BeautifulSoup as parse
from formatter import format_recipes

CONFIG_FILE = 'config.txt'

def create_recipe_list(recipe_list, user_id):
    """
    Create a web page content from the database rows of recipes
    @param recipe_list list of dictionnaries containing the recipes' informations
    and ingredients
    @return a string containing the recipe list in a html format
    """
    if recipe_list == []:
        return []
    config = SafeConfigParser()
    config.read(CONFIG_FILE)

    with open(config.get('html', 'recipe_panel')) as _fd:
        recipe_panel = _fd.read()

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
        img['id'] = '{}_{}_img'.format(str(user_id), str(recipe['id']))
        img['src'] = recipe['img']

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
        url['id'] = '{}_{}_url'.format(str(user_id), str(recipe['id']))
        url['href'] = recipe['url']

        opinion_list = panel.select('ul#$id_opinions')[0]
        opinion_list['id'] = str(recipe['id'])+'_opinions'
        for _opinion in recipe['opinions']:
            opinion_li = soup.new_tag('li')
            opinion_li['class'] = 'list-group-item'
            opinion_li.string = """
                {0} gives {1}/10 : \"{2}\"
            """.format(_opinion['author'], _opinion['mark'], _opinion['comment'])
            opinion_list.append(opinion_li)

        panel_group.append(panel)

    return soup.prettify(formatter='html')


def create_opinions(user_id):
    """
    retrieve the recipes the user visited and didn't comment,
    format them then return them in a form intended to be in the left part
    @param user_id the id of the user
    @return string containing all the opinion forms
    """
    # TODO probleme : les opinions ne s'enleve pas lorsque rempli
    op_rows = db_execute_out("""
        SELECT recipe_id
        FROM opinions
        WHERE author LIKE {};
    """.format(user_id))
    if op_rows == []:
        search_rows = db_execute_out("""
            SELECT recipe_id
            FROM search
            WHERE user_id LIKE {}
        """.format(user_id))
    elif len(op_rows[0]) == 1:
        search_rows = db_execute_out("""
            SELECT recipe_id
            FROM search
            WHERE user_id LIKE {}
            AND recipe_id NOT LIKE {};
        """.format(user_id, op_rows[0][0]))
    else:
        search_rows = db_execute_out("""
            SELECT recipe_id
            FROM search
            WHERE user_id LIKE {}
            AND recipe_id NOT IN {};
        """.format(user_id, (x[0] for x in op_rows[0])))

    if search_rows == [] or search_rows is None:
        return parse("""
            <h4>How did you find theese recipes ?</h4><p>No recipe to comment</p>
        """, 'lxml').prettify(formatter='html')
    opinion_list = format_recipes([x[0] for x in search_rows])
    # constructing the web page part
    config = SafeConfigParser()
    config.read(CONFIG_FILE)
    with open(config.get('html', 'opinion_form_path')) as _fd:
        search_panel = _fd.read()
    soup = parse('<h4>How did you find theese recipes ?</h4><div></div>', 'lxml')
    form_group = soup.div
    form_group['class'] = 'container-fluid'
    # creating a form for each recipe
    for recipe in opinion_list:
        form = parse(search_panel, 'lxml')
        # hidden info
        r_id = form.select('input#$recipe_info')[0]
        r_id['id'] = 'recipe_info_{}'.format(str(recipe['id']))
        r_id['value'] = str(recipe['id'])

        u_id = form.select('input#$user_info')[0]
        u_id['id'] = 'user_info_{}'.format(str(recipe['id']))
        u_id['value'] = str(user_id)

        # the form
        head = form.select('form#$id_form')[0]
        head['id'] = '{}_{}_form_head'.format(str(user_id), str(recipe['id']))
        # the button
        button = form.select('button#$id_button')[0]
        button['id'] = '{}_{}_form'.format(str(user_id), str(recipe['id']))
        # the img
        img = form.select('img')[0]
        img['src'] = recipe['img']
        # the fav button
        fav_button = form.select('button#$fav_id')[0]
        fav_button['id'] = 'fav_{}_{}'.format(str(user_id), str(recipe['id']))
        form_group.append(form)
    return soup.prettify(formatter='html')


def create_favs(user_id):
    """
    retrieve the favorites recipes of the user and format them then return them
    @param user_id the id of the user
    @return favorites recipes formatted in html
    """
    fav_rows = db_execute_out("""
        SELECT idRecipe
        FROM user_has_favorite_recipes
        WHERE idUser LIKE \"{}\";
    """.format(user_id))
    if fav_rows == []:
        return parse("""
            <h4>Favorite List :</h4><p>No favorite</p>
        """, 'lxml').prettify(formatter='html')
    favorite_list = format_recipes([x[0] for x in fav_rows])
    # constructing the web page part
    config = SafeConfigParser()
    config.read(CONFIG_FILE)
    _fd = open(config.get('html', 'fav_panel'))
    fav_panel = _fd.read()
    _fd.close()
    soup = parse('<h4>Favorite List :</h4><div></div>', 'lxml')
    panel_group = soup.div
    panel_group['class'] = 'container-fluid'
    # creating a panel for each recipe
    for recipe in favorite_list:
        panel = parse(fav_panel, 'lxml')
        # the well
        well = panel.select('div#$id_fav')[0]
        well['id'] = 'well_unfav_{}_{}'.format(str(user_id), str(recipe['id']))
        unfav = panel.select('button#$unfav_id')[0]
        unfav['id'] = 'unfav_{}_{}'.format(str(user_id), str(recipe['id']))
        # the img
        img = panel.select('img#$fav_img')[0]
        img['id'] = str(recipe['id'])+'_favimg'
        img['src'] = recipe['img']
        # the url
        url = panel.select('a#$fav_url')[0]
        url['id'] = str(recipe['id'])+'_favurl'
        url['href'] = recipe['url']
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
