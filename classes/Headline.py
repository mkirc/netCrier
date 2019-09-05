import nltk 
import random
from nltk import ne_chunk, pos_tag, word_tokenize
from nltk.tree import Tree
from nltk import ngrams, FreqDist
from nltk.corpus import wordnet as wn 
from nltk.corpus import stopwords
from pymysql import connect


class Headline():
	def __init__(self, line, all_lines):

		self.raw = line
		self.tagged = pos_tag(word_tokenize(all_lines))
		self.entities = ne_chunk(self.tagged)
		self.hot = self.get_hottest_nouns()
		self.chunks = self.get_continuous_chunks(self.raw[1])
		self.labels = { 'PERSON' : None,
						'ORGANIZATION' : None,
						'GPE' :	None }
		self.find_labels()
		self.cleanup_labels()
	
	def get_hottest_nouns(self):

		hot = []
		noun = ['NN', 'NNP', 'NNS']
		for word, pos in self.tagged:
			if any(parts in pos for parts in noun):
				hot.append((word))
		word_frqs = nltk.FreqDist(hot)
		hottest = word_frqs.most_common(100)
		hot = []
		for word, count in hottest:
			hot.append(word)
		return hot

	def find_labels(self):
		for k,v in self.labels.items():
			x = []
			for tree in self.entities.subtrees(filter=lambda t: t.label() == k):
				y = ' '.join([z[0] for z in tree[:]])
				x.append(y)
				self.labels[k] = list(set(x))
		return self.labels

	def cleanup_labels(self):
		for k,v in self.labels.items():

			tagged = [pos_tag(word.split()) for word in self.labels[k]]
			filtered = []
			for lists in tagged:
				current = []
				for word,tag in lists:
					if tag == 'NN' or 'NNP' or 'NNS':
						current.append((word,tag))
				filtered.append(current)
			# print(filtered)
			self.labels[k] = filtered

		return self.labels[k]

	def get_continuous_chunks(self, line):
		'''returns continous chunked parts of speech'''
		chunked = ne_chunk(pos_tag(word_tokenize(line)))
		continuous_chunk = []
		current_chunk = []
		for e in chunked:
			if type(e) == Tree:
				for token, pos in e.leaves():
					current_chunk.append(token)
			else:
			# 	current_chunk.append(i[0])
				continuous_chunk.append(e[0])
			if current_chunk:
				continuous_chunk.append(' '.join(current_chunk))
				current_chunk = []
		return continuous_chunk

	# def get_all_lines_tagged(self, ):
	# 	'''returns ALL the entities from scrapped GN'''
	# 	all_lines = open('GoogleNews.txt', 'r+').read()
	# 	all_entities = pos_tag(word_tokenize(all_lines))
	# 	return all_entities
	


class HeadlineFactory():

	def __init__(self):

		self.lines = self.read_from_db()

	def csv2dict(self, file_path):

		with open(file_path) as openFile:
			out_dict = {}
			for line in openFile.readlines():
				row = line.strip().split(';')
				k, v = row
				out_dict[k] = v		
			return out_dict

	def read_from_db(self):


		creds = self.csv2dict('lists/conn.csv')
		conn = connect(
						host=creds['hst'],
						user=creds['usr'],
						passwd=creds['pw'],
						db=creds['daba']
						)
		cur = conn.cursor()
		try:
			cur.execute("SELECT scrap_id, scrap_txt FROM scrap")
		except Exeption as e:
			print(repr(e))
			raise Exeption('HeadlineFactory build failed!')
			conn.close()

		return [x for x in cur.fetchall()]


	def return_headline(self, lineid=None, line=None):

		if line:
			raw = line
		elif lineid:
			raw = self.get_line_by_id(lineid)			
		else:
			raw = self.get_random_gn_line()
		all_lines = self.get_all_lines()
		return Headline(raw, all_lines)

	def get_random_gn_line(self):

		return random.choice(self.lines)

	def get_line_by_id(self, number):

		return self.lines[number - 1]

	def get_all_lines(self):

		return "\n".join([x[1] for x in self.lines])


# def main():
# 	hf = HeadlineFactory()
	
# 	print(hf.get_line_by_id(len(hf.lines)))
	
# 	# print([x[1] for x in hf.lines])

# 	# print(hl.labels['ORGANIZATION'])

# main()