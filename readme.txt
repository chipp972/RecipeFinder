Project : Recipe Finder
Version : 1.0
Licence : ?
Release date : 12/12/2015

Authors :
	- COTTIN Kevin
	- LI Luting
	- PIERRE-CHARLES Nicolas (pierrecharles.nicolas@gmail.com)

Description :
	Find meal recipes on the web based on user's tastes, ingredients,
	favorite meals, what other users liked etc.
	Can also generate a shopping list for selected recipes.

Dev :
	To run the project :
	1 - Download and install a version of the mysql database. create a database
	called recipe_finder_db and a user called recipe_finder_manager whom you
	grant all rights on the database created.
	2 - Download the httpd apache server and replace in the Makefile the paths
	with your own.
	3 - Run the http server on your machine
	4 - Execute "make sync" on the command line
	5 - Access the program in a web browser on the address "localhost"
