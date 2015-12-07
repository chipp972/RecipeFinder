'''
	@input:key words, searched options
	@output:recipes list
'''

from sklearn.feature_extraction.text import TfidfTransformer

def correct_word(word):
	return word

# Entry
entries = {}

# Get datas from database


# Compute the result
## Compute the weight of ingredients
transformer = TfidfTransformer()
tfidf = transformer.fit_transform(entries)

tfidf.toarray()

#-- TF-IDF

## Researched stats

# Return the result