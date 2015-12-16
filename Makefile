# Makefile of the project
all: 

test:
	sh tst/test.sh
pkg:
	tar -cvf recipe_finder.tar src/

clean:
	rm -rf *~ src/db/recipe_finder.db src/index.html
