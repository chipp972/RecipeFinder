""" General functions to access the database """
#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3
from ConfigParser import SafeConfigParser

def db_execute_in(requests):
    """ Execute requests given in a list of string """
    config = SafeConfigParser()
    config.read('config.txt')
    try:
        _conn = sqlite3.connect(config.get('database', 'path'))
        try:
            _cursor = _conn.cursor()
            for req in requests:
                _cursor.execute(req)
            _conn.commit()
        except sqlite3.OperationalError:
            print 'Error : Operation Error with request ', req
            _conn.rollback()
        finally:
            _conn.close()
    except sqlite3.Error:
        print 'Error : connect error'

def db_execute_out(request):
    """ Execute a select request and send back the result """
    config = SafeConfigParser()
    config.read('config.txt')
    data = None
    try:
        _conn = sqlite3.connect(config.get('database', 'path'))
        try:
            _cursor = _conn.cursor()
            _cursor.execute(request)
            data = _cursor.fetchall()
            _conn.commit()
        except sqlite3.OperationalError:
            print 'Error : Operation Error with request ', request
            _conn.rollback()
        finally:
            _conn.close()
    except sqlite3.Error:
        print 'Error : connect error'
    return data


def db_init():
    """ Create the tables of the database and add the types """
    config = SafeConfigParser()
    config.read('config.txt')
    _fd = open(config.get('database', 'init_file_path'), 'r')
    sql_requests = _fd.read().split('\n\n')
    _fd.close()
    db_execute_in(sql_requests)
    sql_insert_types = [
        "INSERT INTO types(name) VALUES ('entree')",
        "INSERT INTO types(name) VALUES ('main_dish')",
        "INSERT INTO types(name) VALUES ('dessert')",
        "INSERT INTO types(name) VALUES ('other')"
    ]
    db_execute_in(sql_insert_types)
