import csv 
import re 
import lxml.html 
import urllib.parse
import os 

class ScrapeCallback:
	def __init__(self):
		self.path = 'C:\\Users\\Administrator\\Desktop\\zztj'
		self.file_name = os.path.join(self.path,'zztj.txt')

	def __call__(self,html):
		tree = lxml.html.fromstring(html)
		title = tree.xpath('//div[@class="cont"]/h1/span/b/text()')[0]
		with open(self.file_name,'a+',encoding='utf-8') as f:
			f.write('----------------------------------------------------'+'\n')
			f.write(title)
			passages_nodes = tree.xpath('//div[@class="cont"]/div[@class="contson"]/p/text()')
			for passage in passages_nodes:
				f.write(passage+'\n')
