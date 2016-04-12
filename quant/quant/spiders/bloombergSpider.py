# -*- coding: utf-8 -*-
"""
Created on Mon Mar 28 14:36:58 2016

@author: Yanqing
"""

from webSpider import WebSpider
import os
import time, datetime
import re



class BloombergSpider(WebSpider):
    """Spider for the websit the header of which has Last_Modified field"""
    def __init__(self):
        try:
            os.mkdir("english")
        except:
            self.logger.error("Creating directory fail!")
        
    name = "bloomberg"
    allowed_domains = ["bloomberg.com",
                       "bloombergview.com",
                       "bloombergmedia.com",
                       "bloomberg.net"]
    start_urls = [
        "http://www.bloomberg.com/"
#        "http://www.bloomberg.com/news/articles/2016-04-12/china-tells-g-7-to-stop-hyping-sea-disputes-focus-on-economy"
    ]
    
    deltaZone = datetime.timedelta(hours = 0)
           
 
    def extractTimeStamp(self, response):
        timeStr = ""
        encodedTime = ""
        
        try:   
            s = response.xpath('//*[@datetime]').extract()

            for e in s:
                encodedTime = encodedTime + e      
            
            timeSeries  = re.search(u'([0-9]{4})-([0-9]{2})-([0-9]{2})T([0-9]{2}:[0-9]{2})',encodedTime)
                
        except:
            return None        
        
        if timeSeries == None:
            return None
            
        timeSeriesTup = timeSeries.groups()
        
        for ele in timeSeriesTup:       
            timeStr = timeStr + ' '+ ele
  

        timeStr = timeStr.strip()
            
        self.logger.debug('timeStr is ' + timeStr)
            
        #timeStruct = time.strptime(timeStr,"%Y%m%d") 
        try:   
            localTime = datetime.datetime.strptime(timeStr,"%Y %m %d %H:%M")
                

            gmTime = localTime - self.deltaZone
            timeStruct = time.strptime(gmTime.strftime("%B %d %Y %I:%M %p"),"%B %d %Y %I:%M %p")
            self.logger.debug('gmtime is' +  str(gmTime))
            self.logger.debug('timeStruct is' + str(timeStruct))
        except:
            return None
             
        result = time.mktime(timeStruct)
        self.logger.debug('timeStampe is' + str(result))
        return result