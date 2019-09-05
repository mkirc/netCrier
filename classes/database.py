from pymysql import connect

def csv2dict(file_path):

	with open(file_path) as openFile:
		out_dict = {}
		for line in openFile.readlines():
			row = line.strip().split(';')
			k, v = row
			out_dict[k] = v		
		return out_dict
creds = csv2dict('conn.csv')

def insert(in_, conn):

	# print(in_tup[0], in_tup[1])
	cur = conn.cursor()
	cur.execute("INSERT INTO scrap (scrap_txt) VALUES (%s)", (in_))
	cur.close()

def insert_scrapped(conn):


	openfileObj = open('GoogleNews.txt', 'r+')
	count = 0
	
	for line in openfileObj.readlines():
		count += 1
		insert(line.strip("\n"), conn)
		# insert(line.strip("\n"), conn)
		if count % 100 == 0:
				conn.commit()
	conn.commit()


def main():

	conn = connect(
				host=creds['hst'],
				user=creds['usr'],
				passwd=creds['pw'],
				db=creds['daba']
				) 

	insert_scrapped(conn)

	conn.close()

main()