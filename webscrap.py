
class WebScraper():

	def __init__(self):
		# uncomment write method for ...write method.
		# adjust connection details.
		pass

	def fetch_page(self):

		from lxml import html
		from pymysql import connect
		import requests
		from classes.makeGarbage import GarbageMaker


		BASE_URL = 'https://en.wikinews.org/wiki/Main_Page'

		conn_path = 'lists/conn.csv'
		creds = GarbageMaker.csv2dict(self, conn_path)
		conn = connect(
						host=creds['hst'],
						user=creds['usr'],
						passwd=creds['pw'],
						db=creds['daba']
						)

		select = {
			'hl_block' : '//div[@id="MainPage_latest_news_text"]',
			'hl' : '//a[@title]'
		}

		page = requests.get(BASE_URL)
		tree = html.fromstring(page.content)
		test_xpath = select['hl_block'] + select['hl'] + "//text()"
		try:
			xpath_test = tree.xpath(test_xpath)
		except Exeption as e:
			print(repr(e))
			raise Exeption('xpath_test() failed.')
		
		# print(xpath_test)

		for headline in xpath_test:
			content = str(headline).encode('ascii', 'ignore').decode('ascii')
			print(content)
			# self.write_out(content, conn)
		conn.commit()
		conn.close()		

	def write_out(self, content, conn):

		cur = conn.cursor()
		cur.execute("INSERT INTO scrap (scrap_txt) VALUES (%s)", content)


w = WebScraper()
w.fetch_page()