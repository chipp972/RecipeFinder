#!/usr/bin/python
# -*- coding: utf-8 -*-

""" The http server that will serve the recipe finder application """

import BaseHTTPServer
import CGIHTTPServer
from ConfigParser import SafeConfigParser
import time
from cgi_bin.page_builder import save_page, get_content, add_options_to_form
from cgi_bin.db.db_module import db_execute_file, db_execute_out
from cgi_bin.web_crawler import web_crawler
import os
import sys

# Configurations
# Add the app path to the config file
CONFIG_FILE = 'config.txt'
APP_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)))
CONFIG = SafeConfigParser()
CONFIG.read(CONFIG_FILE)
CONFIG.set('DEFAULT', 'app_dir', APP_DIR)
CONFIG.write(open(CONFIG_FILE, 'wb'))

# Retrieves configs
ADDR = CONFIG.get('server', 'address')
PORT = CONFIG.getint('server', 'port')
DB_PATH = CONFIG.get('database', 'path')

# url of the recipe site
BASE_URL = 'http://www.marmiton.org/'

# Create the database if it doesn't exist and modify the search form
if os.path.isfile(DB_PATH) is False:
    print 'Initializing database'
    db_execute_file('init_db_path')
    # adding types to the search form
    add_options_to_form('types', 'search_form_path', 'select#type_select')
    print 'Fetching recipes'
    TIME1 = time.clock()
    if len(sys.argv) > 1:
        web_crawler(BASE_URL, int(sys.argv[1]))
    else:
        web_crawler(BASE_URL)
    TIME2 = time.clock()
    NB = db_execute_out("SELECT COUNT(id) FROM recipes")
    print '{} recipes added in {} seconds'.format(str(NB[0][0]), str(TIME2 - TIME1))
    print 'filling database with exemples'
    db_execute_file('fill_db_path')
else:
    NB = db_execute_out("SELECT COUNT(id) FROM recipes")
    print 'There are {} recipes in the database'.format(str(NB[0][0]))

# Generating the index.html file with the template
SEARCH_FORM = get_content('search_form_path')

# Index Content and path
CONTENT = SEARCH_FORM

INDEX_PATH = os.path.join(APP_DIR, 'index.html')
INDEX_CONTENT = {
    'title': 'Welcome in the Recipe Finder !!!',
    'middle': CONTENT,
    'left': '',
    'right': ''
}
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
