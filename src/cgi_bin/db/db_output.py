""" Contains all the functions to retrieve informations from the database """
#!/usr/bin/python
# -*- coding: utf-8 -*-

from base64 import b64encode
from db_module import db_execute

# TODO class pour récu^pérer les select
def check_user(info):
    """ Create a user with a dictionnary info : {email, password} """
    req = """INSERT INTO users(email, password)
    VALUES (%s, %s);""" % info['email'], b64encode(info['password'])
    db_execute([req])
    return True

def get_all_recipes(info):
    """ get all recipes corresponding to some criterias """
    # r = db_execute(["""
    #     SELECT *
    #     FROM recipes
    # """])
    # print r
    # db_execute("" % info['test'])
