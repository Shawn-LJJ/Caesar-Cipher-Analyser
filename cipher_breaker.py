from key_value_linked_list import SortedPairLinkedLists
from analyser import Analyser
from caesar_cipher import Encrypter

CHARS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

class CipherBreaker:
    def __init__(self, fileNames: list, referenceFile: str, folderName = None) -> None:
        # this assumes all the file(s) already exist(s)
        self.folder = folderName
        self.fileNames = fileNames
        self.keys = [None] * len(fileNames)

        with open(referenceFile, 'r') as f:
            content = f.read()

        self.referenceFreq = {row.split(',')[0] : float(row.split(',')[1]) for row in content.split('\n')}
    
    # method for breaking the caesar cipher and obtain the key
    def breaker(self, fileName):
        if self.folder == None:
            filePath = fileName
        else:
            filePath = f'{self.folder}/{fileName}'

        with open(filePath, 'r') as f:
            content = f.read()
        
        # build a lambda function that takes in both reference frequency dictionary and the actual frequency CharTable to calculate the sum squared error
        SSE = lambda ref, act: sum([(act[char] - ref[char]) ** 2 for char in CHARS])    # this will obtain the SSE for a key

        sse_list = []   # stores all the SSE values for all the keys, the index of the list acts as the keys as it ranges from 0 to 25
        # iterate all 26 possible keys, from 0 to 25 
        for key in range(26):
            encryption = Encrypter(content, key)    # use the encrypter class to do the encryption and then get the result
            encryption.encrypt()
            # taking advantage of the analyser class to obtain a dictionary-like CharTable for storing percentage value for each encrypted character
            analyser = Analyser(encryption.returnResult())
            # get the charPercent CharTable and then calculate the SSE and then append into the list
            sse_list.append(SSE(self.referenceFreq, analyser.getTable('percent')))
        
        # finally, the smallest SSE is most likely the correct key, hence get the index of the smallest SSE and return it
        return sse_list.index(min(sse_list))            

    # method to process all the files that are provided when instantiating the class
    def processFiles(self):
        for i, file in enumerate(self.fileNames):
            self.keys[i] = self.breaker(file)
    
    # return the file names and their corresponding keys, but they are not sorted
    def getResult(self):
        return (self.fileNames, self.keys)

    # convert the new file name list and the keys list into a sorted pair linked lists
    def toSortedPairLinkedLists(self):
        return SortedPairLinkedLists(self.fileNames, self.keys)