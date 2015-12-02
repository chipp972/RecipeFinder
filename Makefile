# Makefile of the project
all: sync test

sync:
	# copy the python scripts
	cp -rf src/cgi_bin/* Path/to/apache/cgi-bin
	# copy the web pages
	cp -rf src/www/* path/to/apache/www/

	# init the database
	mysql -u recipe_finder_manager recipe_finder_db < src/db/init_db.sql
	# fill the database
	mysql -u recipe_finder_manager recipe_finder_db < src/db/fill_db.sql

test:
	sh tst/test.sh

clean:
	rm -rf *~
