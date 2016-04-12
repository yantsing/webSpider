# -*- coding: utf-8 -*-
"""
Created on Fri Mar 25 10:20:31 2016

@author: Yanqing
"""

import scrapy
import re
import os
import time, datetime
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class WebSpider(CrawlSpider):
    name = "example"
    dirc = "english"
    allowed_domains = ["sina.com.cn"]
    start_urls = [
        "http://tech.sina.com.cn/",
        "http://news.sina.com.cn/",
        "http://finance.sina.com.cn/",
    ]
    
    monthMap = {'1':'January', '2' : 'February', '3' : 'March', '4':'April', 
            '01':'January', '02' : 'February', '03' : 'March', '04':'April',
            'jan':'January', 'feb' : 'February', 'mar' : 'March', 'apr':'April',
            '5' : 'May',  '6' :  'June', '7' : 'July', '8':'August', 
            '05' : 'May',  '06' :  'June', '07' : 'July', '08':'August', 
            'may' : 'May',  'jun' :  'June', 'jul' : 'July', 'aug':'August', 
            '9' : 'September',  '10' : 'October', '11' : 'November', '12' : 'December',
            'sep' : 'September',  'oct' : 'October', 'nov' : 'November', 'dec' : 'December',
            '09' : 'September'}
            
    apmMap = {'a.m.':'am', 'a.m':'am','p.m.':'pm','p.m':'pm'} 
        
    def parse(self, response):
        duplicate = False
        try:
            titles = response.xpath('//title').extract()
            title= ""
            for  e in titles:
                title = title + e.encode('utf-8')
            url = response.url
        except:
            title = "no titile"
            url = "no url"
        hashresult = hash(url);
        filename = self.name + str(hashresult) +'.html'
        
        
        if os.path.exists(self.dirc + os.sep + filename):
            with open(self.dirc + os.sep + filename,'r') as f:
                line = f.readline()
                if line == url:
                    #[:-1] is used to remove '/r/n'
                    duplicate = True
                    self.logger.debug('%s duplicate!', response.url)
                else:
                    filename = filename[:-5] + str(hash(f.readline())) + '.html'
                    self.logger.debug('%s not duplicate!', response.url)
                    
                
        # Determin if there is the same file. If there is a file open it and
        # check the title.
        if duplicate == False:
            timeStamp = self.extractTimeStamp(response)
            
            try:   
                if timeStamp != None:
                    with open(self.dirc + os.sep + filename, 'wb') as f:
                        f.write(url)
                        f.write("\r\n")
                        
                        if timeStamp != None:
                            f.write(str(timeStamp))
            
                        f.write("\r\n") 
                        
                        f.write(title)
                        f.write("\r\n")  
                        
                        
                        f.write(str(datetime.datetime.fromtimestamp(timeStamp)))
                        f.write("\r\n")
                        
                        for  e in response.xpath('//p').extract():
                            f.write(e.encode('utf-8') + '\r\n')
                else:
                        self.logger.critical('%s not find time!',response.url)
                        with open(self.dirc + os.sep + "not found", 'a') as ef:
                            ef.write(response.url)
                            ef.write("\r\n")      
            except:
                ## To DO!
                # Complete the exception process
                pass
        
        try:
            for href in response.xpath('//a/@href').extract():
                url = response.urljoin(href)
#                hashresult = hash(url)
#                checkfilename = self.name + str(hashresult) +'.html'
#                if os.path.exists(self.name + os.sep + checkfilename):
#                    with open(self.name + os.sep + checkfilename,'r') as f:
#                        line = f.readline()
#                        if line == url:
#                            self.logger.debug('%s duplicate in yield request!', response.url)
#                            continue
                yield scrapy.Request(url, callback=self.parse)
        except:
            # TO DO!
            # Complete the exception process
            pass



                        
    
