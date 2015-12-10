import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import sqlite3

def correct_word(word):
	return word

'''
@var recipe_type string
@var ingredients string list
@return list
'''
def get_recipes(recipe_type, ingredients):
	# Get datas from database
	conn = sqlite3.connect(os.path.dirname(__file__)+"../db/recipe_finder.db");
	'''recipes = conn.execute(
		"SELECT r.id, r.name, r.url, r.photo, i.name "
		+"FROM recipes r "
		+"LEFT JOIN recipe_has_ingredients ri ON r.idRecipe = ri.idRecipe "
		+"LEFT JOIN ingredients i ON ri.idIngr = i.idIngr "
	    +"WHERE ")
	'''
	# Data examples
	selectRecipes = [
		('1',"Recette chocolat","","","chocolat"),
		('2',"Recette moelleux chocolat","","","chocolat"),
		('3',"Recette fondant chocolat","","","chocolat"),
		('4',"Recette 3 chocolats","","","chocolat blanc"),
		('4',"Recette 3 chocolats","","","chocolat noir"),
		('4',"Recette 3 chocolats","","","chocolat au lait"),
		('5',"Recette parfait au chocolat","","","chocolat"),
		('6',"Poulet au curry","","","chocolat"),
		('7',"Poulet au crabe","","","chocolat"),
		('8',"Cuisses de poulets","","","chocolat")
	]
	recipes = {}
	for recipe in selectRecipes:
		if(not recipes.has_key(recipe[0])):
			recipes[recipe[0]] = {}
			recipes[recipe[0]]['name'] = recipe[1]
			recipes[recipe[0]]['url'] = recipe[2]
			recipes[recipe[0]]['photo'] = recipe[3]
			recipes[recipe[0]]['ingredients'] = []
		recipes[recipe[0]]['ingredients'].append(recipe[4])
	
	print recipes
	'''
	# Compute the weight of ingredients
	vectorizer = CountVectorizer(min_df=1)

	tfidfs = []
	for recipe in recipes:
		tfidfs.append(vectorizer.fit_transform(list(recipe)))
		#analyse = vectorizer.build_analyser()
	
	transformer = TfidfTransformer()	
	#-- TF-IDF
	
	## Researched stats
	
	# Return the result
	'''
'''
Idea :
DB :
	- new relation : "Stats" that regroups
	 -> its position (rank)
	 -> if it was clicked
	 -> id recipe
	 -> id user

	- add index on user id and recipe id

 R_engine :
(dico) -> {"78%": "id_recipe1", "53%" : "id2"...}

Algo :
	Init :
		Determine the weight of each :
		-> disliked ingredients of the user
		-> liked ingredients of the user
		-> recipes that were chosen before by the user
			in function of its tastes
		-> his opinions
		-> (his favorites)
        -> recipes that were chosen before by eveybody except user in function of their tastes

	Compute :
		TFIDF

	Return :
		Dictionnary with the recipe ids and the result of the tfidf
'''

get_recipes("",[""])
