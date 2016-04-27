# -*- coding: utf-8 -*-
"""
Created on Mon Mar 28 14:36:58 2016

@author: Yanqing
"""

from webSpider import WebSpider
import os
import time, datetime
import re



class WalstreetSpider(WebSpider):
    """Spider for the websit the header of which has Last_Modified field"""
    def __init__(self):
        try:
            os.mkdir("english")
        except:
            self.logger.error("Creating directory fail!")
        
    name = "walstreet"
    allowed_domains = ["wsj.com",
                       "wsj-asia.com"]
    start_urls = [
        "http://www.wsj.com"
        #"http://blogs.wsj.com/washwire/2011/07/21/senators-price-out-a-detour-around-pakistan/"
    ]
    
    deltaZone = datetime.timedelta(hours = -4)
           
 
    def extractTimeStamp(self, response):
        timeStr = ""
        encodedTime = ""
        
        try:   
            s = response.xpath('//*[@class="timestamp"]').extract()
            if len(s) == 0:
                s = response.xpath('//*[@class="published"]').extract()
                
            for e in s:
                encodedTime = encodedTime + e      
            
            timeSeries  = re.search(u'([0-9a-zA-z]{1,8})\W{1,2}([0-9]{1,2})\W{1,2}([0-9]{4})\W([0-9]{1,2}:[0-9]{1,2})\W*([a|p|A|P]\.*[m|M]\.*)',encodedTime)

            monthIndex = 0
            apmIndex = 4
            self.logger.debug('timeSeries is ' + str(timeSeries))            
            
            if timeSeries == None:
                s = response.xpath('//*[@class="djs-d-day"]').extract()
                encodedTime = s[0]
                timeDay  = re.search(u'([0-9a-zA-z]{1,8})\W{1,2}([0-9]{1,2})\W{1,2}([0-9]{4})',encodedTime)                 
                
                s = response.xpath('//*[@class="djs-d-hour"]').extract()
                encodedTime = s[0]
                timeHour  = re.search(u'([0-9]{1,2}:[0-9]{1,2})\W([a|p|A|P]\.*[m|M]\.*)',encodedTime)         
                
                if timeDay != None and timeHour != None:
                    timeSeriesTup = timeDay.groups() + timeHour.groups()
                    self.logger.debug('encodeTimeTup is ' + str(timeSeriesTup))
                else:
                    return None
            else: 
                timeSeriesTup = timeSeries.groups()
                
        except:
            return None        
        
        index = 0
        
        for ele in timeSeriesTup:
            if monthIndex == index:
                ele = ele.lower()
                if ele in self.monthMap:
                    ele = self.monthMap[ele]
            
            if apmIndex == index:
                ele = ele.lower()
                if ele in self.apmMap:
                    ele = self.apmMap[ele]
                    
            timeStr = timeStr + ' '+ ele
            index = index + 1

        timeStr = timeStr.strip()
            
        self.logger.debug('timeStr is ' + timeStr)
            
        #timeStruct = time.strptime(timeStr,"%Y%m%d") 
        try:   
            localTime = datetime.datetime.strptime(timeStr,"%B %d %Y %I:%M %p")
                

            gmTime = localTime - self.deltaZone
            timeStruct = time.strptime(gmTime.strftime("%B %d %Y %I:%M %p"),"%B %d %Y %I:%M %p")
            self.logger.debug('gmtime is' +  str(gmTime))
            self.logger.debug('timeStruct is' + str(timeStruct))
        except:
            return None
             
        result = time.mktime(timeStruct)
        self.logger.debug('timeStampe is' + str(result))
        return result