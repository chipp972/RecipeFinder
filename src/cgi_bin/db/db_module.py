""" General functions to access the database """
#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3
from ConfigParser import SafeConfigParser

CONFIG_FILE = 'config.txt'

def db_execute_in(requests):
    """
    Execute requests given in a list of string
    @param requests LIST of strings containing a sql request each
    """
    config = SafeConfigParser()
    config.read(CONFIG_FILE)
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
    """
    Execute a sql request that send back results (select)
    @param request a string containing ONE request
    @return the result of the request
    """
    config = SafeConfigParser()
    config.read(CONFIG_FILE)
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
    """
    Create the tables of the database and add the types
    """
    config = SafeConfigParser()
    config.read(CONFIG_FILE)
    # create tables
    _fd = open(config.get('database', 'init_file_path'), 'r')
    sql_requests = _fd.read().split('\n\n')
    _fd.close()
    db_execute_in(sql_requests)
    # inserting types in the database
    sql_insert_types = [
        "INSERT INTO types(name) VALUES ('entree')",
        "INSERT INTO types(name) VALUES ('main_dish')",
        "INSERT INTO types(name) VALUES ('dessert')",
        "INSERT INTO types(name) VALUES ('other')"
    ]
    db_execute_in(sql_insert_types)

def add_user(mail):
    """
    insert a user into the database if he doesn't exist
    @param mail the mail of the user
    @return the id of the user
    """
    req = """
        SELECT id FROM users WHERE users.email LIKE \"{}\";
    """.format(mail)
    users_rows = db_execute_out(req)
    if len(users_rows) == 0:
        req2 = "INSERT INTO users(email) VALUES (\"{}\");".format(mail)
        db_execute_in([req2])
        users_rows = db_execute_out(req)
    return users_rows[0]
