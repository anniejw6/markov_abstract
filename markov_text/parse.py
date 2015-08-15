import sys
import re

class Parser:
	SENTENCE_START_SYMBOL = '^'
	SENTENCE_END_SYMBOL = '$'


	def __init__(self, name, db):
		self.name = name
		self.db   = db
		self.depth = self.db.get_depth()


	def _split_sentence(self, doc):
		# deal with initial+last
		for y in re.findall('[A-Z]\. [A-Z]', doc):
			doc = doc.replace(y, y.replace(' ', '___babble___'))
		# Split by punctuation
		for y in ['. ', '? ', '! ', '.$$ ','.$ ']:
			doc = doc.replace(y, y + "___senend___")
		sentences = re.split('___senend___', doc)
		sentences = [x.strip() for x in sentences if x != '' ]
		return sentences


	def _split_words(self, sentence):
		for y in [' $$', '$$ ', ' $', '$ ']:
			sentence = sentence.replace(y, y.replace(' ','___math___'))
		#sentence = re.findall('$$')
		sentence = re.split('___math___', sentence)
		sentence = [re.split(' ', phrase) if phrase[0] != '$' else [phrase]
		for phrase in sentence]
		words = [item for sublist in sentence for item in sublist]
		words = [w.replace('___babble___', ' ') for w in words]
		return words


	def _process_words(self, list_of_words):
		words = [Parser.SENTENCE_START_SYMBOL] * (self.depth - 1) + list_of_words + [Parser.SENTENCE_END_SYMBOL] * (self.depth - 1)
		for n in range(0, len(words) - self.depth + 1):
				self.db.add_word(words[n:n+self.depth])
		self.db.commit()

	def parse(self, txt):
		i = 0
		for doc in txt:
			[self._process_words(w) for w in [self._split_words(sentence)
			for sentence in self._split_sentence(doc)]]
			i += 1
			if i % 50 == 0:
				print(i)
				sys.stdout.flush()