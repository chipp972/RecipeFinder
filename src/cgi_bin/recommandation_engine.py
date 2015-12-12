import os
import sqlite3

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
	weights = {}
	weights['default'] = 0
	weights['wanted_ingredients'] = 10
	weights['past_wanted_ingredients'] = 5
	weights['refused_ingredients'] = -10
	
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

	for key in recipes:
		recipe = recipes[key]
		recipe['weights'] = [weights['default']] * len(recipe['ingredients'])
		for ingredient in id_wanted_ingredients:
			if ingredient in recipe['ingredients']:
				recipe['weights'][recipe['ingredients'].index(ingredient)] = weights['wanted_ingredients']
		for ingredient in id_past_ingredients:
			if ingredient in recipe['ingredients']:
				recipe['weights'][recipe['ingredients'].index(ingredient)] = weights['past_wanted_ingredients']
		for ingredient in id_refused_ingredients:
			if ingredient in recipe['ingredients']:
				recipe['weights'][recipe['ingredients'].index(ingredient)] = weights['refused_ingredients']
		recipe['weight'] = 0
		for i in recipe['weights']:
			recipe['weight'] += i

get_recipes(1,['dessert'],['chocolat'],['chocolat noir'])
