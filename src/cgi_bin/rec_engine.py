""" Recommandation engine container """
#!/usr/bin/python
# -*- coding: utf-8 -*-

import cgi
import cgitb; cgitb.enable()
from page_builder import display

# FORM = cgi.FieldStorage()
FORM = cgi.FormContentDict()

_mid = FORM['type']
i = 0
while i < len(FORM['ingr-like']):
    _mid += ' '+FORM['ingr-like'][i]
    i += 1

# _mid = FORM['type'].value


CONTENT = {
    'title': 'Test',
    'middle': _mid,
    'left': "haha",
    'right': ''
}

# calling the recommandation engine script with the list of arguments

display(CONTENT)
