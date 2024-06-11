import os
from time import sleep

# this class deals with prompting user for text file location, attempting to read and write to it
class TextFileOperator():
    def __init__(self) -> None:
        self.content = None
        self.fileLocation = None
    
    # abstract away all the prompting into under this method
    def promptFileLocation(self, prompt, checkFileExist: bool):
        newPath = None
        while newPath == None:
            filePath = input(prompt)
            # if the method if given to check for file existence, then it will do so, or else, move on
            if not os.path.exists(filePath) and checkFileExist:
                print('\nError: Text file does not exists')
                sleep(1.5)
            elif os.path.splitext(filePath)[-1] != '.txt':      # make sure this program only accepts txt files
                print('\nError: Not a text file')
                sleep(1.5)
            else:
                newPath = filePath
        self.fileLocation = newPath
    
    # a simple read text file method which will return the contain of the file
    def readFile(self, prompt = ''):
        if self.fileLocation == None:
            self.promptFileLocation(prompt, True)
        with open(self.fileLocation, 'r') as f:
            self.content = f.read()
        return self.content
    
    # write file function. It will only write to a text file.
    def writeFile(self, prompt = '', content = None):
        # if the file location hasn't set, then set it
        if self.fileLocation == None:
            self.promptFileLocation(prompt, False)
        # if the file already exists, also check if there is content inside. If so, warn the user whether to overwrite the content
        if os.path.exists(self.fileLocation):
            hasContent = False
            with open(self.fileLocation, 'r') as f:
                if f.read().strip() != '':
                    hasContent = True
            if hasContent:
                makeNewFile = input('\nWarning: The file already exists and has contents in it, do you want to overwrite it? (y/n) ')
                if makeNewFile.upper() != 'Y':
                    return 0
        # if no content has been provided, use the class content. 
        if content != None:
            self.content = content
        with open(self.fileLocation, 'w') as f:
            f.write(self.content)
        return 1