""" The class that will serve as an ORM """
#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3
import base64

class DatabaseModule(object):
    """ Module used to retrieve and put info in the database """
    def __init__(self, db_path):
        """ Connection to the database """
        self._db = db_path

    def create_user(self, info):
        """ Create a user with a dictionnary info : {email, password} """
        try:
            _conn = sqlite3.connect(self._db)
            _cursor = _conn.cursor()
            _cursor.execute("""INSERT INTO users(email, password)
            VALUES (%s, %s);""" % info['email'], base64.b64encode(info['password']))
            _conn.commit()
        except sqlite3.OperationalError:
            print 'Error adding user'
            _conn.rollback()
        finally:
            _conn.close()

    def add_ingredient(self):
        """ add """
