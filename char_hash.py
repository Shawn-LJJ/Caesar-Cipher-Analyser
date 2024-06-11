import numpy as np
from key_value_linked_list import SortedPairLinkedLists

# character table which is basically based on a hash table but without the need to do hashing when initialising and rehashing
# since all characters are obviously unique, and there are 26 of them, there will be no collision, so no need for rehashing
# and since we can just use ord() to obtain the ASCII value, it makes things much easier
class CharTable:
    def __init__(self, defaultValueType = 'int') -> None:
        CHARS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.keys = np.array([char for char in CHARS])
        # as I am using np.array, I would also want manually specify the value type, hence this class would force the user to specify the type of value the chartable values will use
        if defaultValueType == 'int':
            self.values = np.zeros(26, np.int16)
        elif defaultValueType == 'float':
            self.values = np.zeros(26, np.float16) 
        else:
            raise TypeError('Error: CharTable values list only accepts int or float type values')

    # the hash function is simply getting the ASCII of capitalised alphabets minus 13 to start from 0 for first char and divide by length of the alphabets
    def __hashing(self, char):
        return (ord(char) - 13) % 26
    
    def __setitem__(self, char, value):
        index = self.__hashing(char)
        self.values[index] = value
    
    def __getitem__(self, char):
        index = self.__hashing(char)
        return self.values[index]
    
    # encapsulate the output into a dictionary like string
    def __str__(self) -> str:
        return '{' + ', '.join([f'"{self.keys[i]}":"{self.values[i]}"' for i in range(26)]) + '}'
    
    # converts the CharTable into a sorted pair linked list and returns it
    def toSortedPairLinkedLists(self):
        return SortedPairLinkedLists(self.keys, self.values)        
