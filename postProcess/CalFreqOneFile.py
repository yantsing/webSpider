'''

@author: Yanqing
'''

import os, re

class CalFreqOneFile:
    def __init__(self, readFileName, writeDictName,maxWordsNum):
        self.readFileName = readFileName   
        self.writeDict = writeDictName    
        self.maxWordsNum = maxWordsNum
        print self.readFileName
        print self.writeDict
    
    matchDict = dict()   
     
    def calFreq(self):  
        with open(self.readFileName,'r+') as rf:
            rf.readline()
            timeline  = rf.readline()
            for line in rf:
                wordList = re.findall(ur'([0-9a-zA-Z]{2,}\b)',line.decode('utf-8'))
                
                wordLen = len(wordList)
                for num in range(self.maxWordsNum):
                    for i in range(wordLen - num):
                        words = ""
                        for j in range(num + 1):
                            words = words + wordList[i + j] + " "
                        words = words.strip()   
                        if words in self.matchDict:
                            self.matchDict[words] = self.matchDict[words] + 1
                        else:
                            self.matchDict[words] = 1;
                        
        
        writeFileName = self.writeDict + os.sep + os.path.basename(self.readFileName)[:-5]    
        with open(writeFileName,'w') as fileWritten:
            fileWritten.write(timeline.strip())
            fileWritten.write('\r\n')
            for element in self.matchDict:
                fileWritten.write(element + ':')
                fileWritten.write(str(self.matchDict[element]) + '\r\n')
    
    
if __name__ == "__main__":        
    
    test  = CalFreqOneFile('../test/resources/fortune630202526.html','../test/targets', 4)
    test.calFreq()
