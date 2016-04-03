# -*- coding: utf-8 -*-
"""
Created on Mon Mar 28 14:36:58 2016

@author: Yanqing
"""

from webSpider import WebSpider
import os
import time, datetime
import re



class FortuneSpider(WebSpider):
    """Spider for the websit the header of which has Last_Modified field"""
    def __init__(self):
        try:
            os.mkdir("fortune")
        except:
            self.logger.error("Creating directory fail!")
        
    name = "fortune"
    allowed_domains = ["fortune.com"]
    start_urls = [
        "http://fortune.com/2016/03/29/trump-strategist-open-letter/",
    ]
 
    def extractTimeStamp(self, response):
        timeStr = ""
        encodedTime = ""
        
        try:   
            s = response.xpath('//*[@datetime]').extract()
            for e in s:
                encodedTime = encodedTime + e              
            
            timeSeries  = re.search(u'([a-zA-z]{3,6})\W{1,2}([0-9]{2})\W{1,2}([0-9]{4})',encodedTime)
                           
        except:
            return None
        
        if timeSeries == None:
            return None
        
        for ele in timeSeries.groups():
            timeStr = timeStr + ele
            
        #timeStruct = time.strptime(timeStr,"%Y%m%d") 
        try:    
            localTime = datetime.datetime.strptime(timeStr,"%B%d%Y")
            gmTime = localTime
            timeStruct = time.strptime(gmTime.strftime("%Y%m%d"),"%Y%m%d")
            self.logger.debug('gmtime is' +  str(gmTime))
            self.logger.debug('timeStruct is' + str(timeStruct))
        except:
            return None
             
        result = time.mktime(timeStruct)
        self.logger.debug('timeStampe is' + str(result))
        return result