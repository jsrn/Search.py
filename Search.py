import sys, argparse, re
import distances

def prep_line( line ):
	line = line.lower()
	line = re.sub( '[^a-z ]', '', line )
	line = re.sub( '  ', ' ', line )
	line = line.strip( ' ' )
	return set( line.split( ' ' ) )

def sentencesearch( searchterm ):
	s_terms = prep_line( searchterm )
	results = []
	for sentence in dictionary:
		display_sentence = sentence
		words = prep_line( sentence )
		total = 0
		wtemp = ""
		print words
		for s in s_terms:
			lowest_for_s = 999
			for w in words:
				d = distances.custom( s, w )
				if d < lowest_for_s:
					lowest_for_s = d
					wtemp = w
			total += lowest_for_s
			words.remove(wtemp)
		total += len( words )
		results.append( [total, display_sentence] )
	return sorted( results )

def wordsearch( searchterm ):
	results = []
	for word in dictionary:
		# Somewhere here we need to check if the dictionary word is actually a sentence
		results.append( [ algo( searchterm, word), word ] )
	return sorted( results )

def search( searchterm ):
	if " " not in searchterm:
		return wordsearch( searchterm )
	else:
		return sentencesearch( searchterm )

# Iterate through the results list and print
def printresults( results, quantity=10 ):
	for result in results[0:quantity+1]:
		print "{0} [{1}]".format( result[1], str( result[0] ) )

algos = {}
algos['l'] = distances.levenshtein
algos['dl'] = distances.dameraulevenshtein
algos['c'] = distances.custom

# begin defaults
wordlist = "dicts/100words.txt"
searchterm = "kitten"
algo = distances.custom
# end defaults

# process args
parser = argparse.ArgumentParser()
parser.add_argument('--search', help="Term to search for.")
parser.add_argument('--dict', help="Filename of the wordlist to search.")
parser.add_argument('--algo', help="l: Levenshtein, d: Damarau-Levenshtein, c: Custom")
args = parser.parse_args()

if args.search is not None:
	searchterm = args.search

if args.dict is not None:
	wordlist = "dicts/" + args.dict

if args.algo is not None:
	algo = algos[args.algo]
# end processing args

# Load lines from dict into dictionary
dictionary = []
with open( wordlist ) as f:
    for line in f:
        dictionary.append( line.rstrip('\n') )

# Search!
print "Searching for term '{0}' in a list of {1} words.".format( searchterm, str( len( dictionary ) ) )
printresults( search( searchterm ) )