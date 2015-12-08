""" Class that will be used to access the database """
#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3
from ConfigParser import SafeConfigParser
import os

def db_execute(requests):
    """ Execute requests given in a list of string """
    config = SafeConfigParser()
    config.read('config.txt')
    try:
        _conn = sqlite3.connect(config.get('database', 'path'))
        _cursor = _conn.cursor()
        for req in requests:
            _cursor.execute(req)
        _conn.commit()
    except sqlite3.OperationalError:
        print 'Error : Operation Error with request ', req
        _conn.rollback()
    finally:
        _conn.close()

def db_init():
    """ Create the tables of the database """
    config = SafeConfigParser()
    config.read('config.txt')
    if os.path.isfile(config.get('database', 'path')) is False:
        _fd = open(config.get('database', 'init_file_path'), 'r')
        sql_requests = _fd.read().split('\n\n')
        _fd.close()
        db_execute(sql_requests)
        db_execute(["INSERT INTO types VALUES (?, %s)" % 'entree'])
        db_execute(["INSERT INTO types VALUES (?, %s)" % 'main_dish'])
        db_execute(["INSERT INTO types VALUES (?, %s)" % 'dessert'])
        db_execute(["INSERT INTO types VALUES (?, %s)" % 'other'])
