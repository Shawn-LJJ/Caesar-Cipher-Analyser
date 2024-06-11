from char_hash import CharTable
from math import ceil
CHARS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

class Analyser:
    def __init__(self, texts) -> None:

        # character table for counting each character
        self.__charCount = CharTable()
        numOfChars = 0
        
        # scan through the whole text content, then increment the character in char table if it appears on the text
        for char in texts:
            # if the char is an alphabet, then increment
            if char.upper() in CHARS:
                self.__charCount[char.upper()] += 1
                numOfChars += 1     # it makes sense for this to line to appear in here, because I don't want it to increment when the character is not an alphabet
        
        # character table for storing percentage of each char appearance
        self.__charPercent = CharTable('float')

        for i in range(26):
            self.__charPercent[CHARS[i]] = (self.__charCount[CHARS[i]] / numOfChars) * 100
        
        # this supposedly character table will be created when calling the plot_graph() method below
        self.charNumOfStars = None 
    
    # making use of the idea of encapsulation to access hidden data via methods
    def getTable(self, tableName):
        if tableName == 'count':
            return self.__charCount
        elif tableName == 'percent':
            return self.__charPercent
        raise TypeError('Invalid table name, only accepts "count" or "percent" table.')

    def plot_graph(self):
        print() # print an empty line

        # convert the __charPercent character table into a paired linked list so that it can be sorted and return the largest values
        charLinkedLists = self.__charPercent.toSortedPairLinkedLists() 

        # then get the top 5 percent characters
        top5Chars, top5Values = charLinkedLists.biggest(6)

        # dictionary for determining which position for the top 5 frequency text should appear
        top5freq = {
            'K' : 'TOP 5 FREQ',
            'L' : '----------',
            'M' : f'|{top5Chars[0]}-{("%.2f" % top5Values[0]).rjust(6, " ")}%',
            'N' : f'|{top5Chars[1]}-{("%.2f" % top5Values[1]).rjust(6, " ")}%',
            'O' : f'|{top5Chars[2]}-{("%.2f" % top5Values[2]).rjust(6, " ")}%',
            'P' : f'|{top5Chars[3]}-{("%.2f" % top5Values[3]).rjust(6, " ")}%',
            'Q' : f'|{top5Chars[4]}-{("%.2f" % top5Values[4]).rjust(6, " ")}%',
            'R' : f'|{top5Chars[5]}-{("%.2f" % top5Values[5]).rjust(6, " ")}%'
        }

        # establish the character table that counts how many stars will be printed for each character column
        self.charNumOfStars = CharTable()
        for i in range(26):
            self.charNumOfStars[CHARS[i]] = ceil((self.__charPercent[CHARS[i]] / 100) * 26)

        # for each row, which is for each character, calculate whether a star should appear for each character
        for i, charRow in enumerate(CHARS):
            rowLine = '  '.join(['*' if self.charNumOfStars[charCol] >= (26 - i) else ' ' for charCol in CHARS])
            # then check if the top 5 freq text should appear, if so, then append the rowLine
            extraText = ''
            if charRow in top5freq.keys():
                extraText = top5freq[charRow]
            print(f'  {rowLine}  |  {charRow}-{("%.2f" % self.__charPercent[charRow]).rjust(6, " ")}%     {extraText}')
        print('__' + '_' * len(rowLine) + '__|')
        print('  ' + '  '.join([char for char in CHARS]) + ' ')


