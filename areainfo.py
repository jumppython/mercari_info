import scrapy
import sqlite3 as sql
import random

class AreaInfoSpider(scrapy.Spider):
	name = "areainfo"
	#global conn
	#global c
	#conn = sql.connect('area.db')
	#c = conn.cursor()

	def __init__(self, *args, **kwargs):
		super(AreaInfoSpider, self).__init__(*args, **kwargs)
		self.conn = sql.connect('area.db')
		self.c = self.conn.cursor()
		self.proxy_pool = ['202.9.104.10:80', \
		                   '110.77.232.210:8080']

	def start_requests(self):
		self.c.execute('DROP TABLE IF EXISTS areainfos')
		self.c.execute('CREATE TABLE IF NOT EXISTS areainfos (item_id, item_url, area_id)')
		areas = [row for row in self.c.execute('SELECT * FROM areas ORDER BY area_id')]
		self.conn.commit()
		#self.conn.close()
		for area in areas:
			for page in range(1,51):
				url = 'https://www.mercari.com'+area[2]+'?page=%d' % page
				request = scrapy.Request(url=url,callback=self.parse)
				if self.proxy_pool:
					request.meta['proxy'] = random.choice(self.proxy_pool)
				#request.meta['proxy'] = '202.9.104.10:80'
				request.meta['area_id'] = area[0]
				yield request
		self.conn.commit()

	def parse(self, response):
		#global conn
		#global c
		item_urls = response.xpath('//a[starts-with(@href,"https://item.mercari.com/jp/")]/@href').extract()
		item_ids = [_.split('/')[4].encode() for _ in item_urls]
		area_id = response.meta['area_id']
		records = [(item_ids[i], item_urls[i], area_id) for i in range(len(item_urls))]
		self.c.executemany('INSERT INTO areainfos VALUES (?,?,?)', records)
		
		
