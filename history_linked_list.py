from history_node import HistoryPoint
import os
import json

# a dual-way linked list that stores the list of history nodes
# NOTE: AS OF NOW, IT WILL NOT SUPPORT ENCRYPTION DONE BY BATCH FILES AS IT CAN FLOOD THE HISTORY. And I do not have time to figure out how to solve it.
class HistoryList():
    def __init__(self) -> None:
        self.head = None
        self.tail = None
        self.length = 0
    
    # since this linked list acts a bit like a queue, adding history will be added after the latest one
    def addHistory(self, encryption_type, key, original_text, new_text, source_file = None, dest_file = None):
        data_struct = {
            'type' : encryption_type,
            'key' : key,
            'original_text' : original_text,
            'source_file' : source_file,
            'new_text' : new_text,
            'destination_file' : dest_file
        }
        if self.head == None:   # if head is none, it means this linked list is empty
            self.head = HistoryPoint(data_struct)
            self.tail = self.head   # since this is the only node, the tail and head will be the same
        else:  
            self.tail.nextPoint = HistoryPoint(data_struct)     # create and add a new history node to the current tail's nextPoint
            self.tail.nextPoint.previousPoint = self.tail       # set the previousPoint of the new node to the current tail
            self.tail = self.tail.nextPoint                     # reassign the current tail to the new node

        self.length += 1
    
    # as we tend to look at history from the most recent to the earliest, we need to iterate through the list from tail to head
    def showList(self, start = 0, stop = None):
        if self.head == None and self.tail == None:         # first check if the history linked list is empty, if so, tell the user it is empty
            return print('\nYour history list is empty.')
        stop = start + 5 if stop == None else stop        # if the user did not specify when to stop, it will loop through the last 5 history nodes from the start value
        currentNode = self.tail
        i = 0
        print('\nID     Date       Time     Key  Original text')
        while currentNode != None and i < stop:
            if i >= start:
                currentNode.printShort()            # by taking advantage of polymorphism, I can easily print the history node data with this method
            currentNode = currentNode.previousPoint
            i += 1
            listHasNotEnded = 0 if currentNode == None else 1
        return listHasNotEnded    # this is to notify the program if there are anymore list after finishing iterating, so to determine whether to continue listing more or not
    
    # iterate over the linked list to check if the id match, if so, then display the full detail, else return error
    def showNode(self, id):
        # user must either key in the full 40 character long hash value or the ID, or the shorter 6 characer version, else error
        if len(id) != 6 and len(id) != 40:
            return print('\nError: History ID must be either short (6 characters long) or full length (40 characters long)')
        
        currentNode = self.head
        while currentNode != None:
            if currentNode.checkId(id):
                return currentNode.printFull()
            currentNode = currentNode.nextPoint
        
        return print('\nError: The ID you enter does not exists')
    
    # iterate over the linked list to find the node to delete. If not found, return a message to tell the user that the ID is not found
    def deleteNode(self, id):
        if len(id) != 6 and len(id) != 40:
            return print('\nError: History ID must be either short (6 characters long) or full length (40 characters long)')
        
        currentNode = self.head
        while currentNode != None:
            if currentNode.checkId(id):     # if the node is found, then proceed to the code below
                if currentNode.previousPoint == None and currentNode.nextPoint == None:
                    self.head = None    # if both the previous and next point are none, then this is the only node left, so deleting this node means the list is empty now
                    self.tail = None
                elif currentNode.previousPoint == None:     # if only the previous point is none, then it is removing the head
                    self.head = currentNode.nextPoint
                    currentNode.nextPoint.previousPoint = None
                elif currentNode.nextPoint == None:         # if only the next point is none, then it is removing the tail
                    self.tail = currentNode.previousPoint
                    currentNode.previousPoint.nextPoint = None
                else:                                       # or else, then do some reassignment to both the next and previous point
                    currentNode.nextPoint.previousPoint = currentNode.previousPoint
                    currentNode.previousPoint.nextPoint = currentNode.nextPoint
                return print('\nThe history has been deleted successfully!')
            currentNode = currentNode.nextPoint
        return print('\nNothing has been deleted. Either that ID did not exists or your history list is empty!')
    
    # simply clears the entire list
    def clearHistory(self):
        # the easiest way to clear the entire list is to just set the head and tail to none so there's no way to retrieve the history data anymore
        self.head = None
        self.tail = None
        print('\nHistory has been cleared!')
    
    '''
    The JSON file which stores the history will be in this format as an example:
    {
        "history_list" : [
            {
                "type" : "Encryption",
                "key" : 2,
                "original_text" : "I love coding",
                "new_text" : "K nqxg eqfkpi",
                "source_file" : "myfile.txt",
                "destination_file" : "myencryption.txt",
                "time" : "19/11/2023 12:02:20"
            },
            {
                "type" : "Decryption",
                "key" : 2,
                "original_text" : "K nqxg eqfkpi",
                "new_text" : "I love coding",
                "source_file" : null,
                "destination_file" : null,
                "time" : "19/11/2023 12:03:20"
            }
        ]
    }
    '''

    # finds and read the history_data.json file and create a new linked list with the data
    def loadHistoryList(self):
        # attempt to read the file. If it doesn't exists, just warn the user about it, but the history will be initially empty
        try:
            with open('history_data.json', 'r') as f:
                content = json.load(f)['history_list']
        except FileNotFoundError:
            return print(f'\nWarning: Unable to locate the history data file. The history will be empty.')
        
        # if the list is empty, then don't proceed, it means the history is already empty, and by default, the head and tail are none
        if not content: return
        
        # first get the first node, then go through the linked list and get each data for each node until the content list of dicts runs out
        self.head = HistoryPoint(content[0])
        self.tail = self.head
        for row in range(1, len(content)):
            self.tail.nextPoint = HistoryPoint(content[row])
            self.tail.nextPoint.previousPoint = self.tail
            self.tail = self.tail.nextPoint

    # save the history into 
    def saveHistoryList(self):
        historyDict = {'history_list' : []}     # base format for the json data

        # iterate over the linked list and then append into the dictionary which will be turned into json object
        currentNode = self.head
        while currentNode != None:
            historyDict['history_list'].append(currentNode.point)
            currentNode = currentNode.nextPoint
        
        # turn into json object and then write it to the file
        json_obj = json.dumps(historyDict)
        with open('history_data.json', 'w') as f:
            f.write(json_obj)