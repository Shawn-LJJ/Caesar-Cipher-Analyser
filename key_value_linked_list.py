from node_class import Node

# a specialised dictionary-like pair linked lists that is derived from the concept of sorted linked list
# it will be sorted based on the value of this "key-value" linked lists in ascending order
# it will be sorted when first instantiated
class SortedPairLinkedLists():
    def __init__(self, keys, values) -> None:
        self.valueHead = Node(values[0])
        self.keyHead = Node(keys[0])
        self.length = len(values)

        # inserting the remaining values and keys 
        for i, newValue in enumerate(values[1:]):
            
            # if the new value is smaller than or equal to the head, set it as the new head
            if newValue <= self.valueHead.point:
                # temporarily assign the current head to a variable
                oldValueHead = self.valueHead
                oldKeyHead = self.keyHead
                # assign the new head
                self.valueHead = Node(newValue)
                self.keyHead = Node(keys[i + 1])
                # set the new head's pointer to the old head
                self.valueHead.nextPoint = oldValueHead
                self.keyHead.nextPoint = oldKeyHead
            # or else, will have to loop through the link until the new value reaches either the end or a larger value
            else:
                # if the linked list only has one item, the head, then just add it after the item, then skip the rest of the code
                if self.valueHead.nextPoint == None:
                    self.valueHead.nextPoint = Node(newValue)
                    self.keyHead.nextPoint = Node(keys[i + 1])
                    continue

                hasNotAssign = True

                currentValueNode = self.valueHead
                currentKeyNode = self.keyHead

                while hasNotAssign:
                    # first check if the next node after the head is nothing, if so, it means is already the end
                    if currentValueNode.nextPoint == None:
                        currentValueNode.nextPoint = Node(newValue)
                        currentKeyNode.nextPoint = Node(keys[i + 1])
                        hasNotAssign = False
                    # if the new value is smaller than the next node's value, then insert a new node between the current and the next node
                    elif newValue <= currentValueNode.nextPoint.point:
                        # create a temporary node which will be our new node
                        tempValueNode = Node(newValue)
                        tempKeyNode = Node(keys[i + 1])
                        # set the temp node next node pointer to point to the next node
                        tempValueNode.nextPoint = currentValueNode.nextPoint
                        tempKeyNode.nextPoint = currentKeyNode.nextPoint
                        # set the current node pointer to this temp node
                        currentValueNode.nextPoint = tempValueNode
                        currentKeyNode.nextPoint = tempKeyNode
                        hasNotAssign = False
                    else:
                        # if the new value is larger than the next, then keep on moving, assign the current node to the next
                        currentValueNode = currentValueNode.nextPoint
                        currentKeyNode = currentKeyNode.nextPoint
    
    def __str__(self) -> str:

        # set up the output string variable with the first value
        output = '{ ' + f"'{self.keyHead.point}' : '{self.valueHead.point}'"
        currentValueNode = self.valueHead.nextPoint
        currentKeyNode = self.keyHead.nextPoint

        # iterate through the linked lists and append the output for each iteration
        while currentValueNode != None:
            output += f", '{currentKeyNode.point}' : '{currentValueNode.point}'"
            currentValueNode = currentValueNode.nextPoint
            currentKeyNode = currentKeyNode.nextPoint
        
        return output + ' }'
    
    # basically simiar to numpy .head(n) function but also retrieves the keys of the top n smallest values
    def smallest(self, n):
        topValues = []
        topKeys = []

        currentValueNode = self.valueHead
        currentKeyNode = self.keyHead
        # loop through the linked list until it reaches the end or the number of smallest values reaches n
        while currentValueNode != None and n > 0:
            topValues.append(currentValueNode.point)
            topKeys.append(currentKeyNode.point)
            currentValueNode = currentValueNode.nextPoint
            currentKeyNode = currentKeyNode.nextPoint
            n -= 1
        
        return (topKeys, topValues)
    
    # now is just like numpy .tail(n) function and works the same as the smallest() method above, but implementation will be completely different
    def biggest(self, n):
        # since we can only traverse from small to big, this is linked list has its own flaw when doing retrieving the largest value
        # I need to traverse the entire linked list, and only start appending keys and values on the last n values, and then reverse the list
        bottomValues = []
        bottomKeys = []
        i = self.length - n     # i will be number of iteration until the program will start appending the keys and values

        currentValueNode = self.valueHead
        currentKeyNode = self.keyHead
        # loop through the linked list until it reaches the end
        while currentValueNode != None:
            if i <= 0:
                bottomValues.append(currentValueNode.point)
                bottomKeys.append(currentKeyNode.point)
            currentValueNode = currentValueNode.nextPoint
            currentKeyNode = currentKeyNode.nextPoint
            i -= 1

        bottomKeys.reverse();bottomValues.reverse()

        return (bottomKeys, bottomValues)