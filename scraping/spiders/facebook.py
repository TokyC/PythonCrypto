import scrapy
import scraping.items

class FacebookSpiderA(scrapy.Spider):
    name = 'facebookaz'
    allowed_domains = ['facebook.com']
    start_urls = ['http://facebook.com/']

    def parse(self, response):
        pass
