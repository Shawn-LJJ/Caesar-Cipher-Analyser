# encrypter class acts as a template to build specialised encrypter objects
class Encrypter:
    def __init__(self, msg, key) -> None:
        self.msg = msg
        self.key = key
        self.newMsg = None

    # method to do the encryption/decryption
    def encrypt(self):
        self.newMsg = ''

        # by simply taking advantage of ASCII code, I can map the original char to the encrypted char without needing any data structure
        alphabets = 'abcdefghijklmnopqrstuvwxyz'
        converter = lambda c: alphabets[(ord(c) - 19 + self.key) % 26] 

        for char in self.msg:
            # if the char is capped, then lower it, convert, then capitalise. Or else just convert
            if char.lower() in alphabets:
                self.newMsg += converter(char.lower()).upper() if char.isupper() else converter(char)
            else:
                self.newMsg += char     # if the char is just some other symbols like numbers or punctuations, then just append it
    
    # return the result of the encrypted message. If the message has not been encrypted, raise an error
    def returnResult(self):
        if self.newMsg is not None:
            return self.newMsg
        raise 'Error: Message has not been encrypted yet'

    # save the encrypted message in a new file.
    def saveResult(self, filePath):
        with open(filePath, 'x') as f:
            f.write(self.newMsg)