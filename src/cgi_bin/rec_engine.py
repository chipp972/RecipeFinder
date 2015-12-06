""" Recommandation engine script """
#!/usr/bin/python
# -*- coding: utf-8 -*-

import cgi
# from db.db_module import DatabaseModule
from page_builder import display

FORM = cgi.FieldStorage()


_mid = ''
for i in FORM.keys():
    _mid += FORM.getValue(i)

CONTENT = {
    'title': 'Test',
    'middle': _mid,
    'left': "haha",
    'right': ''
}

display(CONTENT)
