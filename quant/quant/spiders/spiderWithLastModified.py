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

class webSpider(CrawlSpider):
    name = "sina"
    allowed_domains = ["sina.com.cn"]
    start_urls = [
        "http://tech.sina.com.cn/",
        "http://news.sina.com.cn/",
        "http://finance.sina.com.cn/",
    ]

    deltaZone = datetime.timedelta(hours = 8)
    
    def extractTimeStamp(self, response):
        timeStr = ""
        encodedTime = ""
        
        try:   
            s = response.xpath('//*[@class="navtimeSource"]').extract()
            for e in s:
                encodedTime = encodedTime + e.encode('utf-8')    
            
            s = response.xpath('//*[@class="time-source"]').extract()
            for e in s:
                encodedTime = encodedTime + e.encode('utf-8')

            s = response.xpath('//*[@id="pub_date"]').extract() 
            for e in s:
                encodedTime = encodedTime + e.encode('utf-8')
            
            s = response.xpath('//div').extract()
            for e in s:
                encodedTime = encodedTime + e.encode('utf-8')
            
            s = response.xpath('//span').extract()
            for e in s:
                encodedTime = encodedTime + e.encode('utf-8')
                
                
  
            timeSeries = re.search('([0-9]{4})\\xe5\\xb9\xb4([0-9]{2})\\xe6\\x9c\\x88([0-9]{2})',encodedTime)
            if timeSeries == None:
                timeSeries = re.search('([0-9]{4}).([0-9]{2}).([0-9]{2})',encodedTime)
            
            if timeSeries == None:
                s = str(response.body)
                timeSeries = re.search('([0-9]{4})\\xe5\\xb9\xb4([0-9]{2})\\xe6\\x9c\\x88([0-9]{2})',s)
            if timeSeries == None:
                timeSeries = re.search('([0-9]{4}).([0-9]{2}).([0-9]{2})',encodedTime)
                
        except:
            return None
        
        if timeSeries == None:
            return None
        
        for ele in timeSeries.groups():
            timeStr = timeStr + ele
            
        #timeStruct = time.strptime(timeStr,"%Y%m%d") 
        try:    
            localTime = datetime.datetime.strptime(timeStr,"%Y%m%d")
            gmTime = localTime - self.deltaZone
            timeStruct = time.strptime(gmTime.strftime("%Y%m%d"),"%Y%m%d")
        except:
            return None
        
        
        return time.mktime(timeStruct)
        
    def parse(self, response):
        duplicate = False
        title = str(response.xpath('//title').extract());
        hashresult = hash(title);
        filename = "sina" + str(hashresult) +'.html'
        
        
        if os.path.exists(self.name + os.sep + filename):
            with open(self.name + os.sep + filename,'r') as f:
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
            timeStamp = self.extractTimeStamp(response)
            if timeStamp != None:
                with open(self.name + os.sep + filename, 'wb') as f:
                    f.write(title)
                    f.write("\r\n")  
                    f.write(str(timeStamp))  
                    f.write("\r\n")  
                    f.write(str(time.gmtime(timeStamp)))
                    f.write("\r\n")
                    f.write(str(response.xpath('//p').extract())) 
            else:
                self.logger.critical('%s not find time!',response.url)
                with open(self.name + os.sep + "not finde", 'a') as ef:
                    ef.write(response.url)
                    ef.write("\r\n")
        
        for url in response.xpath('//a/@href').extract():
            yield scrapy.Request(url, callback=self.parse)



                        
    
