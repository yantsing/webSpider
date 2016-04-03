# -*- coding: utf-8 -*-
"""
Created on Fri Mar 25 10:20:31 2016

@author: Yanqing
"""

import scrapy
import os
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class FortuneSpiderTest(CrawlSpider):
    name = "fortunetest"
    allowed_domains = ["fortune.com"]
    start_urls = [
        "http://fortune.com/",
    ]
 

    def parse(self, response):
        duplicate = False
        title = str(response.xpath('//title').extract());
        hashresult = hash(title);
        filename = self.name + str(hashresult)
        
        
        if os.path.exists(filename):
            with open(filename,'r') as f:
                line = f.readline()
                if line[:-1] == title:
                    #[:-1] is used to remove '/r/n'
                    duplicate = True
                    self.logger.debug('%s duplicate!', response.url)
                else:
                    filename = filename[:-5] + str(hash(f.readline())) + '.html'
                    self.logger.debug('%s not duplicate!', response.url)
                    
                
        
        #       To do     #
        # Determin if there is the same file. If there is a file open it and
        # check the title.
        if duplicate == False:
            if 'Last-Modified' in response.headers:
                with open(self.name + os.sep + filename, 'wb') as f:
                    f.write(title)
                    f.write("\r\n")            
                    f.write(str(response.headers['Last-Modified']))
                    f.write("\r\n")            
                    f.write(str(response.xpath('//p').extract())) 
        
        for href in response.xpath('//a/@href'):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse)
