import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import sqlite3

def correct_word(word):
	return word

def get_select_last_preferred_ingredients(id_user, n_max):
	request = 'SELECT i.idIngr '
	request += 'FROM users u '
	request += 'LEFT JOIN search s ON u.id = s.user_id '
	request += 'LEFT JOIN search_has_ingredient si ON s.id = si.idSearch '
	request += 'WHERE u.id = id_user '
	if not n_max == 0:
		request += 'LIMIT '+n_max
def get_select_recipes(id_recipe_types, id_ingredients, n_max):
	request = 'SELECT r.id, i.name '
	request += 'FROM recipes r '
	request += 'LEFT JOIN recipe_has_ingredients ri ON r.idRecipe = ri.idRecipe '
	if recipe_types == [] and ingredients == []:
		return request
	request += 'WHERE '
	if not recipe_types == []:
		request += '(r.type_id=\''+recipe_types[0]+'\' '
		for recipe_type in recipe_types:
			request += 'OR r.type_id=\''+recipe_type+'\' '
		request += ') '
	if not recipe_types == [] and not ingredients == []:
		request += 'AND '
	if not ingredients == []:
		request += '(ri.idIngr=\''+ingredients[0]+'\' '
		for ingredient in ingredients:
			request += 'OR ri.idIngr=\''+ingredient+'\' '
		request += ') '
	if not n_max == 0:
		request += 'LIMIT '+n_max
	return request
'''
@var id_recipe_types id list
@var id_wanted_ingredients id list
@var id_refused_ingredients id list
@return list
'''
def get_recipes(id_user, id_recipe_types, id_wanted_ingredients, id_refused_ingredients):
	# Get datas from database
	conn = sqlite3.connect(os.path.dirname(__file__)+"../db/recipe_finder.db");
	#recipes = conn.execute(get_select_recipes(recipe_types, wanted_ingredients, 0))
	
	# Data examples
	selectRecipes = [
		('1',"chocolat"),
		('2',"chocolat"),
		('3',"chocolat"),
		('4',"chocolat"),
		('4',"chocolat blanc"),
		('4',"chocolat noir"),
		('4',"chocolat au lait"),
		('5',"chocolat"),
		('6',"poulet"),
		('7',"poulet"),
		('8',"poulet")
	]
	recipes = {}
	for recipe in selectRecipes:
		if(not recipes.has_key(recipe[0])):
			recipes[recipe[0]] = {}
			recipes[recipe[0]]['id'] = recipe[0]
			recipes[recipe[0]]['ingredients'] = []
		recipes[recipe[0]]['ingredients'].append(recipe[1])

	id_past_ingredients = []
	#get_select_last_preferred_ingredients(id_user, 10)
	
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

get_recipes(1,['dessert'],['chocolat'],['chocolat noir'])
