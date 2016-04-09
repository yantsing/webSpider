''' 

@author: Yanqing
'''

class ReadSettings(object):
    '''
    classdocs
    '''
 

    def __init__(self):
        '''
        Constructor
        '''
        with open('settings/settings.txt', 'r+') as f:
            self.readWebDir = f.readline().split()[0].strip()
            self.writeWebDir = f.readline().split()[0].strip()    
            self.wordsFilePath = f.readline().split()[0].strip()
            self.resultsDir = f.readline().split()[0].strip()
            
    def getReadWebDir(self):
        return self.readWebDir
    
    def getWriteWebDir(self):
        return self.writeWebDir
    
    def getWordsFilePath(self):
        return self.wordsFilePath
    
    def getResultsDir(self):
        return self.resultsDir

if __name__ == "__main__":      
    test = ReadSettings()
    print test.getReadWebDir()
    print test.getWriteWebDir()
    print test.getWordsFilePath()
    print test.getResultsDir()    