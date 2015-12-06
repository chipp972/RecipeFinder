""" Script that will initialise the SQLlite database """
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3

def db_init(db_name):
    """ Create the tables of the database """
    _fd = open('db/init_db.sql', 'r')
    _content = _fd.read().split('\n\n')
    _fd.close()

    try:
        _conn = sqlite3.connect(db_name)
        _cursor = _conn.cursor()
        for req in _content:
            # print req
            _cursor.execute(req)
        _conn.commit()
    except sqlite3.OperationalError:
        print 'Error : Operation Error'
        _conn.rollback()
    finally:
        _conn.close()
