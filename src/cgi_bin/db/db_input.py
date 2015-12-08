""" Contains all the functions to modify the database """
#!/usr/bin/python
# -*- coding: utf-8 -*-

from base64 import b64encode
from db_module import db_execute

def create_user(info):
    """ Create a user with a dictionnary info : {email, password} """
    req = """INSERT INTO users(email, password)
    VALUES (%s, %s);""" % info['email'], b64encode(info['password'])
    db_execute([req])

def add_ingredient():
    """ add """


def get_all_recipes(info):
    """ get all recipes corresponding to some criterias """
    db_execute(""" """ % info['test'])
