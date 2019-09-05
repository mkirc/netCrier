import nltk 
import random
# from pymysql import connect
from nltk import ne_chunk, pos_tag, word_tokenize
from nltk.tree import Tree
from nltk import ngrams, FreqDist
from nltk.corpus import wordnet as wn 
from nltk.corpus import stopwords
from classes.Headline import Headline, HeadlineFactory

# Tasks:	
#
#			+ dokumentation!!!
#			
class GarbageMaker():
	def __init__(self, headline):


		self.synset_tokens = self.create_synset_tokens(self.csv2dict('lists/synset_tokens.csv'))
		self.hl = headline
		self.count = 0
		self.out_0_1 = self.create_label_line()
		self.out_1 = self.hot_swap(self.static_swap(self.land_swap(self.out_0_1)))
		self.out_2 = self.create_token_line(word_tokenize(self.hl.raw[1].lower()))
		self.out_3 = self.create_token_line(self.out_1)
		self.out_4 = self.create_token_line([word.lower() for word in self.out_1])

	def create_token_line(self, line):
		
		clist = line 
		out_line = []
		for c in clist:
			try:
				word, replace = self.token_suggester(c)
			except TypeError as e:
				print(repr(e))
				out_line.append(c)
				continue
			if replace:
				# print(word, replace)
				# print(in_line)
				out_line.append(replace)
			else:
				out_line.append(c)
		return out_line

	def create_label_line(self, line=None):

		self.hl.find_labels()
		chunks = self.hl.chunks
		out_line = []
		for c in chunks:
			word, replace = self.label_suggester(c)
			if replace:
				out_line.append(replace)
			else:
				out_line.append(c)
		return out_line


	def create_synset_tokens(self, in_dict):

		out_dict = {}
		for k, v in in_dict.items():
			tlist = []
			for s in wn.synsets(str(k)):
				for h in s.hyponyms():
					for l in h.lemmas():
						tlist.append(l.name())
			out_dict[v] = tlist
		return out_dict

	def csv2dict(self, file_path):

		with open(file_path) as openFile:
			out_dict = {}
			for line in openFile.readlines():
				row = line.strip().split(';')
				k, v = row
				out_dict[k] = v		
			return out_dict
		

	def token_suggester(self, chunk):

		for k, v in self.synset_tokens.items():
			word, replace = self.word_suggest(chunk, v, wn.synsets(k))
			# print(word)
			if word:
				if "_" in replace:
					replace = replace.replace('_', ' ') # naming fail
				return word, replace
		return None, None

	def word_suggest(self, chunk, tokens, synset):
		# takes a list of words, looks for tokens, makes suggestions based on
		# wordnet synsets.
		# lookie here, OP. any() compares list of strings
		# against list of words; weird behaviour is programmed!
		chunk = [chunk] 
		if any(words in chunk for words in tokens):

			_token = wn.synsets(str(chunk))
			if not _token:
				return None, None
			def_tok = _token[0].definition().split()
			filtered = set([word for word in def_tok if word not in stopwords.words('english')])
			for s in synset[0].hyponyms():
				for t in nltk.word_tokenize(s.definition()):
					if any(words in t for words in filtered):
						return chunk, s.lemmas()[0].name()
			else:
				try:
					ran = random.choice(synset[0].hyponyms())
					ran = ran.lemmas()[0].name()
					return chunk, ran
				except IndexError as e:
					# print(repr(e))
					return None, None
		return None, None

	def label_suggester(self, chunk):
		x = None
		replace = None
		for k, v in self.hl.labels.items():
			try:
				x = any(words in chunk for words in v)
			except TypeError as e:
				# print(repr(e))
				pass
			if x:
				# print('yay!')
				if k == 'PERSON':
					replace = self.get_random_repl('race') + ' ' + self.get_random_repl('class')
				elif k == 'ORGANIZATION':
					replace = 'monsters like you and i' # gawd think of something!
				elif k == 'GPE':
					replace == self.get_random_repl('plane')
				else:
					return None, None
			return chunk, replace

	def hot_swap(self, line):
		out_line = []
		for word in line:
			if any(words in word for words in self.hl.hot):
				out_line.append(self.get_random_repl('change'))
			else:
				out_line.append(word)
		return out_line

	def static_swap(self, line):
		out_line = []
		for word in line:
			if word == '|':
				out_line.append(u'\u26e6')
			elif word == 'Brexit':
				out_line.append('Exodus')
			elif word == 'YouTube':
				out_line.append('MagicMirror')
			elif word in '$€':
				out_line.append('Gold')
			else:
				out_line.append(word)
		return out_line


	def land_swap(self, line):
		countries = []
		countries_path = 'lists/countries.txt'
		for item in open(countries_path).readlines():
			countries.append(item.strip())
		out_line = []
		for word in line:
			if any(land in word for land in countries):
				out_line.append(self.get_random_repl('plane'))
			else:
				out_line.append(word)
		return out_line


	def get_random_repl(self, wish):

		if wish == 'change':

			changes = []
			for w in wn.synsets('change'):
				for h in w.hyponyms():
					for l in h.lemmas():
						x = l.name()
						if '_' in x:
							changes.append(x.replace('_', ' '))
						else:
							changes.append(l.name())
			return random.choice(changes)

		if wish == 'race':

			rc = open('lists/races.txt', 'r+')
			races = []
			for line in rc:
				x = ''.join(line.split("\n"))
				races.append(x)
			o_rc = open('lists/other_races.txt', 'r+')
			# possible distinction for later
			# o_races = []
			for line in o_rc:
				x = ''.join(line.split("\n"))
				races.append(x)
			return random.choice(races)

		if wish == 'class':

			cl = open('lists/classes.txt', 'r+')
			classes = []
			for line in cl:
				x = ''.join(line.split("\n"))
				classes.append(x)
			return random.choice(classes)

		if wish == 'plane':

			pl = open('lists/planes.txt', 'r+')
			planes = []
			for line in pl:
				planes.append(''.join(line.split("\n")))
			return random.choice(planes)
