# -*- coding: utf-8 -*-
"""
Created on Mon Mar 28 14:36:58 2016

@author: Yanqing
"""

from webSpider import WebSpider
import os
import time, datetime
import re


class sinaSpider(WebSpider):
    """Spider for the websit the header of which has Last_Modified field"""
    def __init__(self):
        try:
            os.mkdir("sina1")
        except:
            self.logger.error("Creating directory fail!")
        
    name = "sina1"
    allowed_domains = ["sina.com.cn"]
    start_urls = [
        "http://www.sina.com.cn/",
    ]
    
    deltaZone = datetime.timedelta(hours = 8)
    
    def extractTimeStamp(self, response):
        timeStr = ""
        encodedTime = ""
        
        try:   
            s = response.xpath('//*[@class="navtimeSource"]').extract()
            for e in s:
                encodedTime = encodedTime + e  
            
            s = response.xpath('//*[@id="navtimeSource"]').extract()
            for e in s:
                encodedTime = encodedTime + e

            s = response.xpath('//*[@id="pub_date"]').extract() 
            for e in s:
                encodedTime = encodedTime + e
                
            s = response.xpath('//span').extract()
            for e in s:
                encodedTime = encodedTime + e    
            
            s = response.xpath('//div').extract()
            for e in s:
                encodedTime = encodedTime + e
            

                
                
  
            timeSeries  = re.search(u'([0-9]{4})[^0-9]([0-9]{2})[^0-9]([0-9]{2})',encodedTime)
           
            if timeSeries == None:
                s = str(response.body)
                timeSeries = re.search('([0-9]{4})\\xe5\\xb9\xb4([0-9]{2})\\xe6\\x9c\\x88([0-9]{2})',s)
            if timeSeries == None:
                timeSeries = re.search('([0-9]{4})[^0-9]([0-9]{2})[^0-9]([0-9]{2})',s)
                
        except:
            return None
        
        if timeSeries == None:
            return None
        
        for ele in timeSeries.groups():
            timeStr = timeStr + ele
            
        #timeStruct = time.strptime(timeStr,"%Y%m%d") 
        try:    
            localTime = datetime.datetime.strptime(timeStr,"%Y%m%d")
            gmTime = localTime
            timeStruct = time.strptime(gmTime.strftime("%Y%m%d"),"%Y%m%d")
            self.logger.debug('gmtime is' +  str(gmTime))
            self.logger.debug('timeStruct is' + str(timeStruct))
        except:
            return None
             
        result = time.mktime(timeStruct)
        self.logger.debug('timeStampe is' + str(result))
        return result
        

        
 