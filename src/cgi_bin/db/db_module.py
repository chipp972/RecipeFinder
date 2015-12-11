""" General functions to access the database """
#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3
from ConfigParser import SafeConfigParser
from bs4 import BeautifulSoup as parse

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

    # adding types to the search form
    types = db_execute_out("SELECT * FROM types")
    search_form_path = config.get('html', 'search_form_path')
    _fd = open(search_form_path)
    soup = parse(_fd.read(), "lxml")
    _fd.close()

    soup.select('select#type_select')[0].string = ''
    for row in types:
        opt = soup.new_tag('option')
        opt.string = row[1]
        opt['name'] = row[0]
        soup.select('select#type_select')[0].append(opt)

    # writing the html file
    html = soup.prettify(formatter='html')
    with open(search_form_path, "wb") as _fd:
        _fd.write(html)

def get_content(file_path):
    """ Return the content of the web page inside the body tags """
    _fd = open(file_path, 'r')
    soup = parse(_fd.read(), "lxml")
    return soup.find('body').prettify(formatter='html')
