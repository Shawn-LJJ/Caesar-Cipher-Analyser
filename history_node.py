from datetime import datetime
from termcolor import colored
from hashlib import sha1
from node_class import Node

# a recursive function that will return a string that cut the original text until it has slightly above 50 characters long
def textSlicer(fullText : str, numOfWords = 1):
    shortText = ' '.join(fullText.split(' ')[:numOfWords])
    if len(shortText) > 50 or shortText == fullText:
        return shortText
    return textSlicer(fullText, numOfWords + 1)

# inherit the history node from the original node class, as this history node is like the subset of a node
# this history node will basically contain more data than a regular node class
# NOTE: As of now, it will not support storing encryption done on batch files
class HistoryPoint(Node):
    def __init__(self, point) -> None:
        super().__init__(point)
        # for this type of node, it will also be able to traverse backwards
        self.previousPoint = None

        # just like how git use sha1 to identify each commit's ID, I would do the same but for each history node
        # although I have no idea how git differentiate between each hash, 
        # I would do it by adding the POSIX time, which is guranteed to be different everytime, plus the original text, so as to prevent a rainbow attack to dechiper the time
        self.__id = sha1(f'{datetime.now().timestamp()}{self.point["original_text"]}'.encode()).hexdigest()

        # also adds a the time the encryption took place
        try:
            self.point['time'] = point["time"]  # if the point dictionary already has the time key, then insert into the node data
        except KeyError:                        # or else, then get the current time
            nowTime = datetime.now()
            self.point['time'] = f'{nowTime.day:02d}/' + f'{nowTime.month:02d}' + f'/{nowTime.year} ' + f'{nowTime.hour:02d}:' + f'{nowTime.minute:02d}:' + f'{nowTime.second:02d}'  
            
        '''
        The self.point data structure will look like this:
        self.point = {
            'type' : 'Encryption'                       # determines whether this is an encryption or decryption
            'key'  : 2                                  # the key for this encryption/decryption
            'original_text' : 'I love coding'           # original text before encryption/decryption
            'new_text' : 'K nqxg eqfkpi'                # the encrypted/decrypted text
            'source_file' : 'myfile.txt'                # file path of the original text file, will be None if is done from option 1
            'destination_file' : 'myecryption.txt'      # file path of the encrypted/decrypted text file, will be None if the result is not saved
            'time' : datetime string                    # stores the time the encryption took place in string
        }
        '''
    
    # just like git, it's able to check if the id matches with shorter hash value
    def checkId(self, id):
        if len(id) == 6:
            return id == self.__id[:6]
        return id == self.__id
    
    # retrieves the history node ID, or the hash value, either full length or shorter length with 6 characters
    def getId(self, length = 'full'):
        if length == 'full':
            return self.__id
        elif length == 'short':
            return self.__id[:6]
        else:
            raise TypeError('Error: Invalid ID length, only accept "full" or "short" length.')
    
    # git's equivalent of "git log" command but will be only showing this one node
    def printFull(self):
        print(f'\nFull detail on your {self.point["type"].lower()}:')
        print(colored('ID:', 'cyan') + f' {self.__id}')
        print(colored('Time:', 'cyan') + f' {self.point["time"]}')
        print(colored(f'{self.point["type"]} key:', 'cyan') + f' {self.point["key"]}')
        print(colored('Original text:', 'cyan') + f' {self.point["original_text"]}')
        print(colored(f'Result text:', 'cyan') + f' {self.point["new_text"]}')
        if self.point["source_file"] != None:
            print(colored('Original text file location:', 'cyan') + f' {self.point["source_file"]}')
        if self.point["destination_file"] != None:
            print(colored('Result text file location:', 'cyan') + f' {self.point["destination_file"]}')
    
    # git's equivalent of "git log --oneline" command
    def printShort(self):
        # if the original_text is over 50 characters long, cut the text after 50 characters 
        # taking advantage of recursive function to cut short of text until the entire text is at least 50 characters long without slicing any word
        original_text = " ".join(self.point['original_text'].split("\n"))
        slicedText = textSlicer(original_text)

        # if the text is sliced, add the three fullstops "..." at the back. Also check for the sentence stoppers symbols, replace them if they exists on the last word
        if slicedText != original_text:
            SYMBOLS = ',.!?'
            if slicedText.split(' ')[-1][-1] in SYMBOLS:
                slicedText = f'{slicedText[:-1]}...'
            else:
                slicedText = f'{slicedText}...'

        print(f'{self.__id[:6]} {self.point["time"]} ' + f'{self.point["key"]}'.rjust(2, ' ') + f'   {slicedText}')
    
    # returns the data in dictionary form
    def getData(self):
        return self.point
