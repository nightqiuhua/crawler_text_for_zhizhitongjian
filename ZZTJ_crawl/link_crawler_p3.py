import re 
import urllib.parse 
import urllib.request 
import datetime 
import time 
from downloader_p3 import Downloader
from mogon_cache import MongoCache
from scrape_callback2_p3 import ScrapeCallback
import lxml.html 



def link_crawler(seed_url,root_regx=None,node_regx=None,delay=5,max_depth=-1,max_urls=-1,user_agent='wswp',proxies=None,num_retries=1,scrape_callback=None,cache=None):
	seen = {seed_url:0}
	D= Downloader(delay=delay,user_agent=user_agent,proxies=proxies,num_tries=num_retries,cache=cache)
	num_urls=0
	page = 450
	for page in range(450,744):
		url = 'https://so.gushiwen.org/guwen/bookv_{}.aspx'.format(page)
		try:
			html = D(url).decode('utf-8')
		except Exception as e:
			raise e
		else:
			if scrape_callback:
				scrape_callback.__call__(html)




#link_regx='http://www.hao123.com/manhua/detail/'
seed_url ='https://so.gushiwen.org/guwen/bookv_450.aspx'
root_regx =' '
node_regx =' '

link_crawler(seed_url=seed_url,root_regx = root_regx,node_regx=node_regx,scrape_callback=ScrapeCallback(),cache = MongoCache())