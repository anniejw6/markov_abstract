import urllib.request
from bs4 import BeautifulSoup
import pickle

def pull_data(url):
	""" Pull data """
	with urllib.request.urlopen(url) as url:
		s = url.read()
	return s


def _grab_entry(entry):
	"""Parse each entry"""
	return {'id' : entry.id.string,
	'date_updated' : entry.updated.string,
	'date_published' : entry.published.string,
	'title' : entry.title.string.replace('\n','').strip(),
	'summary' : entry.summary.string.replace('\n','').strip(),
	'author' : [x.contents[1].string for x in entry.find_all('author')],
	'category' : entry.category['term']}
	

def parse(html):
	"""Parse HTML"""
	soup = BeautifulSoup(html, 'html.parser')
	result = []
	for link in soup.find_all('entry'):
		result.append(_grab_entry(link))
	return result



def run(category, start, num_res):
	"""Main Function"""
	base_url = 'http://export.arxiv.org/api/query?'\
	'search_query=cat:{cat}&start={start}&max_results={num_results}'
	url1 = base_url.format(cat = category, 
		start = start, num_results = num_res)
	return parse(pull_data(url1))


if __name__ == '__main__':

	math_cat = ['math.AG', 'math.AT', 'math.AP', 'math.CT', 'math.CA',
'math.CO', 'math.AC', 'math.CV', 'math.DG', 'math.DS', 'math.FA',
'math.GM', 'math.GN', 'math.GT', 'math.GR', 'math.HO', 'math.IT',
'math.IT', 'math.KT', 'math.LO', 'math.MP', 'math.MG', 'math.NT',
'math.NA', 'math.OA', 'math.OC', 'math.PR', 'math.QA', 'math.RT',
'math.RA', 'math.SP', 'math.ST', 'math.ST', 'math.SG']

	records = 10000
	interval = 1000

	if(interval > records):
		interval = records

	for cat in math_cat:

		print(cat)
		res = []

		for i in range(0, records, interval):
			print(cat + str(i))
			res = res + run(cat, i, interval)

		# Save
		pickle.dump(res, open( cat + ".p", "wb" ) )

		print('done')