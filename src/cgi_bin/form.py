""" Script used to retrieve infos from the form and check identity """
#!/usr/bin/python
# -*- coding: utf-8 -*-

import cgi
import cgitb
from page_builder import display

cgitb.enable()

# FORM = cgi.FieldStorage()
FORM = cgi.FormContentDict()

MID = FORM['type']
i = 0
while i < len(FORM['ingr-like']):
    MID += ' '+FORM['ingr-like'][i]
    i += 1

# MID = FORM['type'].value


CONTENT = {
    'title': 'Test',
    'middle': MID,
    'left': "haha",
    'right': ''
}

# calling the recommandation engine script with the list of arguments

display(CONTENT)
