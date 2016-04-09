# -*- coding: utf-8 -*-
"""
Created on Mon Mar 28 14:36:58 2016

@author: Yanqing
"""

from webSpider import WebSpider
import os
import time, datetime
import re



class ThestreetSpider(WebSpider):
    """Spider for the websit the header of which has Last_Modified field"""
    def __init__(self):
        try:
            os.mkdir("thestreet")
        except:
            self.logger.error("Creating directory fail!")
        
    name = "thestreet"
    allowed_domains = ["thestreet.com"]
    start_urls = [
        "http://www.thestreet.com/",
    ]
 
    def extractTimeStamp(self, response):
        timeStr = ""
        encodedTime = ""
        
        try:   
            s = response.xpath('//*[@class="pubDate"]').extract()
            for e in s:
                encodedTime = encodedTime + e              
            
            timeSeries  = re.search(u'([0-9]{2})\W{1,2}([0-9]{2})\W{1,2}([0-9]{2})',encodedTime)
                           
        except:
            return None
        
        if timeSeries == None:
            return None
        
        for ele in timeSeries.groups():
            timeStr = timeStr + ele
            
        #timeStruct = time.strptime(timeStr,"%Y%m%d") 
        try:    
            localTime = datetime.datetime.strptime(timeStr,"%m%d%y")
            gmTime = localTime
            timeStruct = time.strptime(gmTime.strftime("%Y%m%d"),"%Y%m%d")
            self.logger.debug('gmtime is' +  str(gmTime))
            self.logger.debug('timeStruct is' + str(timeStruct))
        except:
            return None
             
        result = time.mktime(timeStruct)
        self.logger.debug('timeStampe is' + str(result))
        return result