import urllib.request 
import urllib.parse 
import socket 
from datetime import datetime 
import time 
import random 

DEFAULT_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
DEFAULT_DELAY = 2
DEFAULT_TIMEOUT = 60
DEFAULT_RETRIES = 1

class Throttle:
	def __init__(self,delay):
		self.delay = delay
		self.domains = {}

	def wait(self,url):
		domain = urllib.parse.urlparse(url).netloc
		last_accessed = self.domains.get(domain)

		if self.delay > 0 and last_accessed is not None:
			sleep_sec = self.delay-(datetime.now() - last_accessed).seconds
			if sleep_sec>0:
				time.sleep(sleep_sec)
		self.domains[domain] = datetime.now()

class Downloader:
	def __init__(self,delay=DEFAULT_DELAY,user_agent=DEFAULT_AGENT,proxies=None,num_tries=DEFAULT_RETRIES,timeout=DEFAULT_TIMEOUT,opener=None,cache=None):
		socket.setdefaulttimeout(timeout)
		self.throttle = Throttle(delay)
		self.user_agent=user_agent 
		self.proxies = proxies 
		self.num_tries=num_tries
		self.cache = cache
		self.opener = opener

	def __call__(self,url):
		result = None
		if self.cache:
			try:
				result = self.cache[url]
			except KeyError:
				pass
			else:
				if self.num_tries > 0 and 500<= result['code'] <600:
					result = None
		if result is None:
			self.throttle.wait(url)
			proxy = random.choice(self.proxies) if self.proxies else None
			headers = {'User_agent':self.user_agent}
			result = self.download(url,headers,proxy=proxy,num_tries=self.num_tries)
			if self.cache:
				self.cache[url] = result
		#print(result['html'])
		return result['html']

	def download(self,url,headers,proxy,num_tries,data=None):
		print('Downloading:',url)
				#将含中文的url转化为unicode格式的url
		b = b'/:&?='
		url = urllib.parse.quote(url,b)
		url = url.encode('utf-8').decode()
		request = urllib.request.Request(url) or {}
		opener = urllib.request.build_opener() or self.opener 
		if proxy:
			proxy_para = {urllib.parse.urlparse(url).scheme:proxy}
			opener.add_handler(urllib.request.ProxyHandler(proxy_para))

		try:
			#发送请求
			response = opener.open(request)
			html = response.read()
			#print('html=',html)
			code = response.code
		except urllib.error.URLError as e:
			print('Download error',e.reason)
			html = ''
			if hasattr(e,code):
				code = e.code
				if num_tries>0 and 500<=code<600:
					html = self.download(url,headers,proxy,num_tries-1)
			else:
				code = response.code
		return {'html':html,'code':code}
