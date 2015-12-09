import sklearn.feature_extraction.text import TfidfTransformer

def correct_word(word):
	return word

'''
	@var recipe_type string
	@var ingredients string list
	@return list
'''
def get_recipes(recipe_type, ingredients, list):
	# Get datas from database
	
	##### get recipe
	
	# Compute the result
	## Compute the weight of ingredients
	transformer = TfidfTransformer()
	tfidf = transformer.fit_transform(entries)
	
	tfidf.toarray()
	
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
