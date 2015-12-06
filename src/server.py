""" The http server that will serve the recipe finder application """
#!/usr/bin/python
# -*- coding: utf-8 -*-

import BaseHTTPServer
import CGIHTTPServer
import time
import os
from cgi_bin.db.init_db import db_init
from cgi_bin.page_builder import save_page

# configurations
HOST = "localhost"
PORT = 8080
DB_NAME = "recipe_finder.db"
INDEX_CONTENT = {
    'title': 'Welcome !!',
    'middle': 'Welcome to the Recipe Finder app !!!',
    'left': '',
    'right': ''
}

if __name__ == '__main__':
    # Create the database if it doesn't exist
    if os.path.isfile(DB_NAME) is False:
        db_init(DB_NAME)

    # Generate index.html with the template
    save_page(INDEX_CONTENT, 'index.html')

    # Create and launch the http server
    Handler = CGIHTTPServer.CGIHTTPRequestHandler
    Handler.cgi_directories = ["/cgi_bin"]
    Server = BaseHTTPServer.HTTPServer
    HTTPD = Server((HOST, PORT), Handler)
    print time.asctime(), "Server Starts - %s:%s" % (HOST, PORT)
    try:
        HTTPD.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        HTTPD.server_close()
        print time.asctime(), "Server Stops - %s:%s" % (HOST, PORT)
