import pickle

blob = pickle.load(open( "math.AG.p", "rb" ))

with open('../data/somefile.txt', 'w') as ffile:
	for i in range(0, 1000):
		ffile.write(blob[i]['summary'])
		ffile.write('\n')