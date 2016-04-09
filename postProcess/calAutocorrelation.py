'''


@author: Yanqing
'''
from pywin.scintilla.view import wordbreaks
import numpy as np


import os

class CalAutocorrelation(object):
    '''
    classdocs
    '''
    def __init__(self, readDictName):
        self.readDictName = readDictName   

    secondesPerDay = 86400
    secondesof2000 = 970329600
    maxDim = 8000
    corrcorefIndex = (maxDim + maxDim - 1)/2
    def genrateVector(self,word):
        result = np.zeros(self.maxDim)
        for f in os.listdir(self.readDictName):
            filepath = self.readDictName + '/' + f
            if os.path.isfile(filepath):
                with open(filepath, 'r+') as rf:
                    time = rf.readline()
                    timestamp = float(time)
                    timeInt = int(timestamp - self.secondesof2000)
                    for line in rf.readlines():
                        l = line.split(':')
                        try:
                            if word.strip() == l[0].strip():
                                if timeInt > 0:
                                    value = int(l[1].strip())
                                    index = timeInt/self.secondesPerDay
                                    result[timeInt/self.secondesPerDay] = result[timeInt/self.secondesPerDay]  + value
                        except:
                            pass
                        
        return result 
    
    def getAutocorrelation(self, wordA, wordB):
        vectorA = self.genrateVector(wordA)
        vectorB = self.genrateVector(wordB)
        normA = np.linalg.norm(vectorA)
        normB = np.linalg.norm(vectorB)
        autoCorrelation = np.correlate(vectorA, vectorB, "full")
        corrcoef = autoCorrelation[self.corrcorefIndex]
        return  autoCorrelation,  corrcoef/(normA * normB), normA, normB  
             
                
if __name__ == "__main__":        
    
    test  = CalAutocorrelation('../test/targets')
    result = test.genrateVector('trusted advisors') 
    autoCorrelation, corrcoef, normA, normB  = test.getAutocorrelation('trusted advisors','trusted advisors')  
    print sum(autoCorrelation)
    print corrcoef
    print normA
    print normB