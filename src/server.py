""" The http server that will serve the recipe finder application """
#!/usr/bin/python
# -*- coding: utf-8 -*-

import BaseHTTPServer
import CGIHTTPServer
from ConfigParser import SafeConfigParser
import time
from cgi_bin.page_builder import save_page
from cgi_bin.db.db_module import db_init
import os

# Configurations
# Add the app path to the config file
APP_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)))
FP = 'config.txt'
CONFIG = SafeConfigParser({'app_dir': APP_DIR})
CONFIG.read(FP)
CONFIG.write(open(FP, 'wb'))

# Retrieves configs
ADDR = CONFIG.get('server', 'address')
PORT = CONFIG.getint('server', 'port')
DB_PATH = CONFIG.get('database', 'path')


AUTH_FORM = open(CONFIG.get('html', 'auth_form_path')).read()
SEARCH_FORM = open(CONFIG.get('html', 'search_form_path')).read()

# Index Content and path
CONTENT = AUTH_FORM + SEARCH_FORM

INDEX_PATH = os.path.join(APP_DIR, 'index.html')
INDEX_CONTENT = {
    'title': 'Welcome in the Recipe Finder !!!',
    'middle': CONTENT,
    'left': '',
    'right': ''
}

if __name__ == '__main__':
    # Create the database if it doesn't exist
    db_init()

    # Generate the index with the template
    save_page(INDEX_CONTENT, INDEX_PATH)

    # Create and launch the http server
    Handler = CGIHTTPServer.CGIHTTPRequestHandler
    Handler.cgi_directories = ["/cgi_bin"]
    Server = BaseHTTPServer.HTTPServer
    HTTPD = Server((ADDR, PORT), Handler)
    print time.asctime(), "Server Starts - %s:%s" % (ADDR, PORT)
    try:
        HTTPD.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        HTTPD.server_close()
        print time.asctime(), "Server Stops - %s:%s" % (ADDR, PORT)
