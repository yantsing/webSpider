'''

@author: Yanqing
'''

from CalFreqOneFile import CalFreqOneFile
import os

class CalFreqFiles(object):
    '''
    classdocs
    '''
    def __init__(self, readDictName, writeDictName, maxWordsNum):
        self.readDictName = readDictName   
        self.writeDict = writeDictName
        self.maxWordsNum = maxWordsNum    
        if not os.path.isdir(writeDictName):
            os.mkdir(writeDictName)
    
    def calFreq(self):
        for f in os.listdir(self.readDictName):
            filepath = self.readDictName + '/' + f
            if os.path.isfile(filepath):
                calFreq = CalFreqOneFile(filepath,self.writeDict, self.maxWordsNum)
                calFreq.calFreq()
                
if __name__ == "__main__":        
    
    test  = CalFreqFiles('../test/resources','../test/targets', 4)
    test.calFreq()                
            

        