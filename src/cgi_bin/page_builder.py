""" The page builder module which create pages to display or save """
#!/usr/bin/python
# -*- coding: utf-8 -*-

from string import Template
# from bs4 import BeautifulSoup as parse

TEMPLATE_FILE = 'www/html/template.html'

def get_template():
    """ Return the content of the template file """
    template_handle = open(TEMPLATE_FILE, 'r')
    template_input = template_handle.read()
    template_handle.close()
    return Template(template_input)

# TODO create recipe page
# def create_recipe_page(id_list):
#     """ create a recipe list and return a dictionnary containing
#      the content of the page {left, right, middle} """

def display(_content):
    """
    display the template with the modified content
    @param _content a dictionnary {title, left, middle, right}
    """
    _template = get_template()
    _result = _template.safe_substitute(
        title=_content["title"],
        middle=_content["middle"],
        left=_content["left"],
        right=_content["right"]
    )
    print "Content-type: text/html; charset=utf-8\n\n"
    print _result

def save_page(_content, _output):
    """
    generate a file and save it to the _output file specified
    @param _content a dictionnary {title, left, middle, right}
    @param _output the path to save file to save into
    """
    _template = get_template()
    _result = _template.safe_substitute(
        title=_content["title"],
        middle=_content["middle"],
        left=_content["left"],
        right=_content["right"]
    )
    _fd = open(_output, 'w')
    _fd.write(_result)
