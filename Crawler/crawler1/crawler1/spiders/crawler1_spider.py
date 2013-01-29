from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
#from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
#from scrapy.http import Request
from crawler1.items import Crawler1Item

items = []

class crawler1Spider(CrawlSpider):
    name = "crawler1"
    allowed_domains = ["cs.sfu.ca"]
    start_urls = [
        "http://www.cs.sfu.ca"
    ]
    
    rules = [
	Rule(SgmlLinkExtractor(allow = ('(html)$'), allow_domains = ('cs.sfu.ca'), deny = ('(cgi)', '(www2)')), follow=True, callback = 'parse_item')
    ]

    def parse_item(self, response):
        hxs = HtmlXPathSelector(response)
	sites = hxs.select('//@href')
	#items = []
	temp = []
	
	for site in sites:
		
		item = Crawler1Item()
		if site.re('(cgi)'):
			pass
		elif site.re('(css)|(js)$'):
			pass
		elif site.re('^(/\w+)'):
			item['webpages'] = site.extract()
			if item not in items:
				items.append(item)
				temp.append(item)
		elif site.re(r'(http://www.cs.sfu.ca)'):
			item['webpages'] = site.extract()
			if item not in items:
				items.append(item)
				temp.append(item)
		elif site.re(r'(https://intraweb.cs.sfu.ca/)|(https://portal.cs.sfu.ca/)'):
			item['webpages'] = site.extract()
			if item not in items:
				items.append(item)
				temp.append(item)
		elif site.re('^(http)'):
			item['external'] = site.extract()
			if item not in items:
				items.append(item)
				temp.append(item)
		elif site.re('^\w'):
			item['webpages'] = site.extract()
			if item not in items:
				items.append(item)
				temp.append(item)
		#items = list(set(items))
	return temp
