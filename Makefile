# Makefile of the project
all:

sync:
	# copy the python scripts
	cp -rf src/cgi_bin/* C:/Apache24/cgi-bin
	# copy the web pages
	cp -rf src/www/* C:/Apache24/htdocs/
	# init the database
	mysql -u recipe_finder_manager recipe_finder_db < src/db/init_db.sql
	# fill the database
	mysql -u recipe_finder_manager recipe_finder_db < src/db/fill_db.sql

test:
	sh tst/test.sh

clean:
	rm -rf *~
