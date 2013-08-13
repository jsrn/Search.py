# Returns the Levenshtein distance between two strings
def levenshtein( s, t ):
	len_s, len_t = len( s ), len( t )

	if len_s > len_t:
		s, t = t, s
		len_s, len_t = len_t, len_s

	if s == t: return 0;
	if len_s == 0: return len_t
	if len_t == 0: return len_s

	v0, v1 = [], []

	for i in range( len_t + 1 ):
		v0.append( i )
		v1.append( 0 )

	for i in range( len_s ):
		v1[0] = i + 1

		for j in range( len_t ):
			cost = 0 if s[i] == t[j] else 1
			v1[j+1] = min( v1[j] + 1, v0[j + 1] + 1, v0[j] + cost )

		for j in range( len( v0 ) ):
			v0[j] = v1[j]

	return v1[len_t]

# Returns the Damerau-Levenshtein distance between two strings
def dameraulevenshtein( s, t ):
	len_s, len_t = len( s ), len( t )

	if len_s > len_t:
		s, t = t, s
		len_s, len_t = len_t, len_s

	if s == t: return 0;
	if len_s == 0: return len_t
	if len_t == 0: return len_s

	d = {}
	for i in xrange( -1, len_s ):
		d[(i,-1)] = i+1
	for j in xrange( -1, len_t ):
		d[(-1,j)] = j+1
	for i in xrange( len_s ):
		for j in xrange( len_t ):

			if s[i] == t[j]: cost = 0
			else: cost = 1

			d[(i,j)] = min( d[(i-1,j)] + 1,
							d[(i,j-1)] + 1,
							d[(i-1,j-1)] + cost )
			if i > 1 and j > 1 and s[i] == t[j-1] and s[i-1] == t[j]:
				d[(i,j)] = min(  d[(i,j)],
								d[(i-2,j-2)] + cost )         
	return d[(len_s-1,len_t-1)]

# Returns a modified DL distance, with weighted costs
def custom( s, t ):
	len_s, len_t = len( s ), len( t )

	insert_cost, delete_cost, substitution_cost, transpose_cost = 0, 1, 2, 1

	if len_s > len_t:
		s, t = t, s
		len_s, len_t = len_t, len_s

	if s == t: return 0;
	if len_s == 0: return len_t
	if len_t == 0: return len_s

	d = {}
	for i in xrange( -1, len_s ):
		d[(i,-1)] = i+1
	for j in xrange( -1, len_t ):
		d[(-1,j)] = j+1
	for i in xrange( len_s ):
		for j in xrange( len_t ):

			if s[i] == t[j]: cost = 0
			else: cost = substitution_cost

			d[(i,j)] = min( d[(i-1,j)] + delete_cost, # deletion
							d[(i,j-1)] + insert_cost, # insertion
							d[(i-1,j-1)] + cost ) # substitution
			if i > 1 and j > 1 and s[i] == t[j-1] and s[i-1] == t[j]:
				d[(i,j)] = min(  d[(i,j)],
								d[(i-2,j-2)] + transpose_cost )         
	return d[(len_s-1,len_t-1)]