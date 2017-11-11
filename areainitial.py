import scrapy
import sqlite3 as sql

class AreaInitialSpider(scrapy.Spider):
	name =  "areainitial"

	def start_requests(self):
		urls = ['https://www.mercari.com/jp/area/']
		for url in urls:
			request = scrapy.Request(url=url, callback=self.parse)
			request.meta['proxy'] = "114.174.205.245:3128"
			yield request

	def parse(self, response):
		area_urls = response.xpath('//a[starts-with(@href, "/jp/area/")]/@href').extract()
		area_names = response.xpath('//a[starts-with(@href, "/jp/area/")]/text()').extract()
		# Create areas Table to save couple of areanames and areaurls
		# Create a connection to database file
		conn = sql.connect('area.db')
		c = conn.cursor()
		# Create Table
		c.execute('CREATE TABLE areas (area_id,area_name, area_url)')
		# Insert lots of area records
		records = [(int(area_urls[i].split('/')[3]),area_names[i],area_urls[i]) for i in range(len(area_urls))]
		c.executemany('INSERT INTO areas VALUES (?,?,?)',records)
		conn.commit()
		conn.close()
