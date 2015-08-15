import pickle

blob = pickle.load(open( "math.AG.p", "rb" ))

with open('../data/somefile.txt', 'w') as ffile:
	for i in range(0, 1000):
		text = blob[i]['summary']
		text = text.replace('\quad', '')
		text = ' '.join(text.split())
		ffile.write(text)
		ffile.write('\n')