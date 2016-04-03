# -*- coding: utf-8 -*-
"""
Created on Thu Mar 31 13:13:25 2016

@author: Yanqing
"""

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
class exampleSpider(CrawlSpider):
    name = 'example.com'
    allowed_domains = ['sina.com.cn']
    start_urls = ['http://www.sina.com.cn',]
    rules = (
        # Extract links matching 'category.php' (but not matching 'subsection.php')
        # and follow links from them (since no callback means follow=True by default).
        #Rule(LinkExtractor(allow=('category\.php', ), deny=('subsection\.php', ))),
        #Rule(LinkExtractor(allow=('category\.php', ), deny=('subsection\.php', ))),
        # Extract links matching 'item.php' and parse them with the spider's method parse_item
        #Rule(LinkExtractor(allow=('item\.php', )), callback='parse_item', follow = True,),
        Rule(LinkExtractor(restrict_xpaths=('//a', )), callback='parse_item', follow = True,),
    )
    
    def parse(self, response):
        self.logger.info('Hi, this is an item page! %s', response.url)
    
    def parse_item(self, response):
        self.logger.info('Hi, this is an item page! %s', response.url)