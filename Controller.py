from pymysql import connect
from classes.makeGarbage import GarbageMaker
from classes.Headline import HeadlineFactory




class Controller():

	def __init__(self):

		# a_string = 'Video appears to show helicopter which crashed into New York skyscraper swirling and diving minutes before it came down'
		# a_string = 'Ridgecrest earthquake packed the power of 45 nuclear bombs, but its impact was muted'

		self.test_string = None
		self.hf = HeadlineFactory()
		self.creds = self.csv2dict('lists/conn.csv')
		self.conn = connect(
							host=self.creds['hst'], 
							user=self.creds['usr'], 
							passwd=self.creds['pw'], 
							db=self.creds['daba']
							)
	def csv2dict(self, file_path):

		with open(file_path) as openFile:
			out_dict = {}
			for line in openFile.readlines():
				row = line.strip().split(';')
				k, v = row
				out_dict[k] = v		
			return out_dict

	def write_to_db(self, scrap_id, content, conn):

		cur = self.conn.cursor()
		cur.execute("INSERT INTO gen (scrap_id, gen_txt) VALUES (%s, %s)", (scrap_id, content))

	def make_garbage_headline(self):

		for i in range(1401, 1403):
			for j in range(1,10):
				gb = GarbageMaker(self.hf.return_headline(lineid=i))
				# print('Attempt' + " " + str(i) +'_'+ str(j))
				if ''.join(gb.out_2) != ''.join(gb.out_4) and ''.join(gb.out_3) != ''.join(gb.out_1):

					# print(gb.hl.raw)
					# print(' '.join(gb.out_3))
					if type(gb.hl.raw[0]) is int:
						print('on attempt: ' + str(j))
						yield (gb.hl.raw[0], ' '.join(gb.out_3))
						break
			else:
				print('dud.')
		return


def main():

	c = Controller()
	new_hl = c.make_garbage_headline()
	for tpl in new_hl:
		count, line = tpl
		print(str(count), line)
		# c.write_to_db(count, line, c.conn)
		c.conn.commit()
	c.conn.close()

main()

		# x = True
		# count = 0
		# while x:
		# 	gb = GarbageMaker(self.hf.return_headline(lineid=i))
		# 	count += 1
		# 	# print('Attempt' + " " + str(count))
		# 	if ''.join(gb.out_2) != ''.join(gb.out_4) and ''.join(gb.out_3) != ''.join(gb.out_1):
		# 		x = False

		# 		print(gb.hl.raw)
		# 		# print(gb.out_1)
		# 		# print(gb.out_2)
		# 		print(' '.join(gb.out_3))
		# 		# print(gb.out_4)
		# 		if type(gb.hl.raw[0]) is int:

		# 			#self.write_to_db(gb.hl.raw[0], ' '.join(gb.out_3), self.conn)
		# 			pass

	# self.conn.commit()
	# self.conn.close()