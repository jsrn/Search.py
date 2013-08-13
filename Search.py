import sys, argparse
import distances

def wordsearch( searchterm ):
	results = []
	for word in dictionary:
		results.append( [ algo( searchterm, word), word ] )
	return sorted( results )

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

print "Searching for term '" + searchterm + "' in a list of " + str( len( dictionary ) ) + " words."
printresults( wordsearch( searchterm ) )