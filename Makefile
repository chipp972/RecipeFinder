# Makefile of the project
all:

sync:
	# copy the python scripts
	cp -rf src/cgi_bin/* C:/wamp/bin/apache/apache2.4.9/cgi-bin
	# copy the web pages
	cp -rf src/www/* C:/wamp/www/RecipeFinder/
	# init the database
	mysql -u recipe_finder_manager recipe_finder_db < src/db/init_db.sql

test:
	sh tst/test.sh

clean:
	rm -rf *~
