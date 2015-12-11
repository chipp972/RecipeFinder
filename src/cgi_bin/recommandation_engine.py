import sklearn.feature_extraction.text import TfidfTransformer

def correct_word(word):
	return word

'''
	@var recipe_type string
	@var ingredients string list
	@return list
'''
def get_recipes(recipe_type, ingredients):
	# Get datas from database
	
	
	# Compute the result
	## Compute the weight of ingredients
	transformer = TfidfTransformer()
	tfidf = transformer.fit_transform(entries)
	
	tfidf.toarray()
	
	#-- TF-IDF
	
	## Researched stats
	
	# Return the result