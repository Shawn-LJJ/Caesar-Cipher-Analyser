from time import sleep
from caesar_cipher import Encrypter
from analyser import Analyser
from printer import MenuPrinter
from file_operation import TextFileOperator
from cipher_breaker import CipherBreaker
from history_linked_list import HistoryList
import random
import math
import json
import os

# change the directory path so that the working directory will be in text_files which contains all the text files to do encryption and decryption
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
# dname = dname + '/text_files'     # my testing directory
os.chdir(dname)

# instantiate the history object and load the history json file into memory
# this will be the only object that will be used globally in this main program
history = HistoryList()
history.loadHistoryList()

def printWelcomeMessage():
    # title bar will be width dependable based on the length of the longest string
    messages = ['ST1507 DSAA: Welcome to:', '~ Caesar Cipher Encrypted Message Analyzer ~', "Shawn Lim Jun Jie (2239745)", 'Class DAAA/2B/01']

    maxLength = max([len(msg) for msg in messages])
    print()
    print('*' * (maxLength + 8))
    print('* ' + messages[0] + ' ' * (maxLength - len(messages[0]) + 5) + '*')
    print('*' + ' ' * (maxLength + 6) + '*')
    print('*   ' + messages[1] + '   *')
    print('*' + '-' * (maxLength + 6) + '*')
    print('*' + ' ' * (maxLength + 6) + '*')
    print('* ' + messages[2] + ' ' * (maxLength - len(messages[2]) + 5) + '*')
    print('* ' + messages[3] + ' ' * (maxLength - len(messages[3]) + 5) + '*')
    print('*' * (maxLength + 8))

    input('\n\nPress enter key to continue...')

# function to check if the key is an integer by attempting to convert it to integer and see if an error arises
def isInvalid(val):
    try:
        int(val)
    except:
        return True
    return False

# option 1 & 2: encrypt or decrypt a user input text or file based on the user choice on the menu
def encryption(textOrFile):
    
    # prompt user whether to encrypt or decrypt. Prompt again if option is invalid
    option = None
    while option != 'E' and option != 'D':

        option = input('\nEnter "E" for Encrypt or "D" for Decrypt: ').upper()  # input option should be cap insensitive, hence, uppercase the input
        
        if not (option == 'E' or option == 'D'):
            print('\nError: Invalid option')
            sleep(2)
    
    # if the user opted to encrypt or decrypt text, then the program will prompt for text, or else, it will be prompting for file name
    if textOrFile == '1':
        text = input(f'\nPlease type text you want to {"encrypt" if option == "E" else "decrypt"}: ')
    else:
        fileOperator = TextFileOperator()
        text = fileOperator.readFile(f'\nPlease enter the file you want to {"encrypt" if option == "E" else "decrypt"}: ')
        sourceFilePath = fileOperator.fileLocation
        
    # prompt user for the cipher key. Prompt again if is an invalid value
    key = None
    while isInvalid(key):
        key = input('\nEnter the cipher key: ')
        if isInvalid(key):
            print('\nError: Invalid key')
            sleep(2)
    
    # since decrypting is just the reverse of encrypting, if the user picked decrypting, the key will be multiplied by a negative, effectively reversing
    newKey = int(key) if option == 'E' else int(key) * -1
    
    encryption = Encrypter(text, newKey)
    encryption.encrypt()

    if textOrFile == '1':
        cipherText = encryption.returnResult()
        if option == 'E':
            print(f'\nPlaintext:\t{text}')
            print(f'Ciphertext:\t{cipherText}')
        else:
            print(f'\nCiphertext:\t{text}')
            print(f'Plaintext:\t{cipherText}')
        history.addHistory("Encryption" if option == "E" else "Decryption", key, text, cipherText)
    else:
        fileOperator.promptFileLocation('\nPlease enter an output file: ', False)
        result = fileOperator.writeFile(content=encryption.returnResult())
        if result:
            history.addHistory("Encryption" if option == "E" else "Decryption", key, text, encryption.returnResult(), sourceFilePath, fileOperator.fileLocation)
    input('\nPress enter key to continue...')    

# option 3: analysing the letters
def analyseLetter(_):
    
    fileOperator = TextFileOperator()
    contents = fileOperator.readFile('\nPlease enter the file you want to analyse: ')
    if contents == '':
        return print('\nWarning! You are trying to analyse an empty file!')
        
    fileAnalyser = Analyser(contents)
    fileAnalyser.plot_graph()
    input('\nPress enter key, to continue...')

# option 4 & 5: inferring key of file(s)
def inferKey(option):
    
    targetFolder = None
    # if option is 5, then get the target folder. If option is 4, there will be no target folder
    if option == '5':
        while targetFolder == None:
            userInputFolder = input('\nPlease enter the folder name: ')
            if not os.path.exists(userInputFolder):
                print('\nError: Folder does not exists')
                sleep(1.5)
            else:
                targetFolder = userInputFolder
    
    # if option is 4, prompt for the target and reference file. If option is 5, no prompting needed, just need to get all the files in the target folder
    if option == '4':
        # take advantage of the text file operator class to check if the file exists
        targetFileOperator = TextFileOperator()
        targetFileOperator.promptFileLocation('\nPlease enter file to analyse: ', True)
        targetFiles = [targetFileOperator.fileLocation]      # encapsulate the file location into a list because the cipher breaker will take in a list of file name(s)
    else:
        # iterate every file in the target folder. If the file is a txt file, then append to the target files list
        targetFiles = []
        for file in os.listdir(targetFolder):
            if os.path.splitext(file)[-1] == '.txt':
                targetFiles.append(file)
    # NOTE TO LECTURERS: I MADE USERS PROMPT FOR REFERENCE FREQUENCIES FILE FOR BOTH OPTION 4 AND 5 TO STANDARDISE HOW THE LOGIC FLOWS
    # for option 5, the reference file will be used for the entire batch files, so user just need to be prompted once for the reference file.
    referenceFileOperator = TextFileOperator()
    referenceFileOperator.promptFileLocation('\nPlease enter the reference frequencies file: ', True)
    referenceFile = referenceFileOperator.fileLocation
    
    # instantiate the cipher breaker class to start inferring all the text files
    try:
        decoder = CipherBreaker(targetFiles, referenceFile, targetFolder)
        decoder.processFiles()
    except:     # if an error occurs while trying to process, it means the reference file is not the right one
        print('\nError: Bad reference frequencies file.')
        sleep(1.5)
        return

    if option == '4':       # if the user option is 4, then print the inferred key and then prompt whether to decrypt the file
        _, key = decoder.getResult()
        key = key[0]
        print(f'\nThe inferred caesar cipher key is {key}')
        option = input('\nWould you want to decrypt this file using this key? y/n ')
        if option.lower() == 'y':       # if the user simply type anything other than y, the program will assume is a no
            targetFileOperator.readFile()
            decryption = Encrypter(targetFileOperator.content, key) 
            decryption.encrypt()
            outputFile = TextFileOperator()
            outputFile.writeFile('\nPlease enter an output file: ', decryption.returnResult())
            history.addHistory('Decryption', key, targetFileOperator.content, outputFile.content, targetFileOperator.fileLocation, outputFile.fileLocation)
    else:
        files, keys = decoder.toSortedPairLinkedLists().smallest(len(targetFiles))      # take advantage of the sorted pair linked list to get the inferred keys sorted
        logText = []
        print() # print an empty line for formatting
        # for each file, create a new file name, append to the log, read the original file content, decrypt it, and then write it to the new file
        for i, file in enumerate(files):    
            newFileName = f'file{i + 1}.txt'
            logText.append(f'Decrypting: {file} with key: {keys[i]} as: {newFileName}')
            print(logText[i])
            with open(f'{targetFolder}/{file}') as f:
                originalContent = f.read()
            decryption = Encrypter(originalContent, keys[i])
            decryption.encrypt()
            outputFile = TextFileOperator()
            outputFile.fileLocation = f'{targetFolder}/{newFileName}'
            outputFile.writeFile(content=decryption.returnResult())
        
        # write the log to the log file
        with open(f'{targetFolder}/log.txt', 'w') as f:
            f.write('\n'.join(logText))
    
    input('\nPress enter key, to continue...')

# if a user picked an invalid option, this function will be called
def default(_):
    print('\nError: Invalid option')
    sleep(1.5)

# extra option #1: history management
# this will access a submenu to manage history of encrypted message
def historyMenu(_):
    # this history manager will have a submenu
    userOption = None
    while userOption != '5':
        options = [
            'View history list',
            'Checkout a history encryption/decryption',
            'Remove a history encryption/decryption',
            'Clear entire history',
            'Return to main menu'
        ]

        subMenu = MenuPrinter(options)
        subMenu.display()
        userOption = subMenu.getInputOption()

        # since there won't be much code, I just put all the history functionality under this if else code
        if userOption == '1':
            # this option will list down the top 5 recent history in a similar manner to git log --oneline, with the option to list down further more when the user wants to
            i = 0; canDisplayMore = 1; userWantsDisplayMore = True
            while canDisplayMore and userWantsDisplayMore:      # if the list is exhausted or the user doesn't wants to see more, stop showing, or else keep displaying
                canDisplayMore = history.showList(i)
                if canDisplayMore:
                    userInputDisplayMore = input('\nDo you want to display more? y/n: ').strip().lower()
                    userWantsDisplayMore = True if userInputDisplayMore == 'y' else False
                i += 5
            input('\nPress enter to continue...')
    
        elif userOption == '2':
            # this option basically ask the user for the history node ID and then attempt to find it and print it
            userEnteredId = input('\nEnter the ID of the history: ').strip()
            history.showNode(userEnteredId)
            input('\nPress enter to continue...')

        elif userOption == '3':
            # this option will ask the user for the history node ID and attempt to find and delete it
            userEnteredId = input('\nEnter the ID of the history to be deleted: ').strip()
            history.deleteNode(userEnteredId)
            input('\nPress enter to continue...')

        elif userOption == '4':
            # this option will prompt the user whether he/she wants to clear the entire history, if user entered y, then the history will be cleared
            userPermission = input('\nAre you sure you want to clear your history? (y/n) ').strip().lower()
            if userPermission == 'y': 
                history.clearHistory()
                input('\nPress enter to continue...')

        elif userOption != '5':
            # if the user chose 5, the program will just go back to the main menu, but if is anything else, then print an error message to the user
            default(_)

# extra option #2: guess the word
def miniGame(_):
    
    # attempt to find and locate the word_definition.json. If it doesn't exists, or has tampered some way, then don't proceed
    try:
        with open('word_definition.json', 'r') as f:
            word_meaning = json.load(f)['word_dictionary']
    except:
        print('\nError: Fail to retrieve the word dictionary. Unable to proceed to the game.')
        sleep(1.5)
        return
    
    # print the welcome message
    print('\nWelcome to the Guess The Word minigame!')
    print('\nIn this minigame, we will get a random word and encrypt its definition with a random key.')
    print('Your goal of this game is to guess the word by reading its encrypted definition.')
    print('You only have 5 tries, and for each tries you fail, we will reveal a small section of the unecrypted definition.')
    input('\nPress enter to start!')
    userOption = 'y'    # user will later be asked whether they want to play again, so a while loop to make the user play again
    while userOption == 'y':
        # get random word and its definition
        word_choice = random.choice(word_meaning)
        answer, meaning = word_choice['word'].lower().strip(), word_choice['definition']
        # encrypt the word definition with a random key from 1 to 25
        defEncrypter = Encrypter(meaning, random.randint(1, 25))
        defEncrypter.encrypt()
        encryptedMeaning = defEncrypter.returnResult()

        # loop at most 5 times for each round of guessing
        for round in range(1, 6):
            # the way to reveal a small section of the unencrypted definition is to check the length of the definition times how many round has pass, then cut into 5 pieces but round down the number of words can be display
            numOfWordsToReveal = math.floor((round - 1) * len(meaning.split(' ')) / 5)
            meaningToDisplay = meaning.split(' ')[:numOfWordsToReveal] + encryptedMeaning.split(' ')[numOfWordsToReveal:]
            print(f'\nGuess number {round}')
            print(f"Here's the encrypted definition: {' '.join(meaningToDisplay)}")
            userGuess = input('Guess the word: ').lower()
            if userGuess == answer:
                print(f'\nCongrats! You guessed the correct word in {round} attempt(s)!')
                break
            elif round == 5:
                print(f'\nGame over! The correct answer is {answer}.')
            else:
                print(f'\nIncorrect! Please enter another word!')
        
        print(f"Here's the unencrypted definition: {meaning}")
        input('\nPress enter to continue...')
        userOption = input('\nDo you want to play again? (y/n) ').lower().strip()

# print the exit message when the user wants to exit
def exitMessage(_):
    return print('\nBye, thanks for using ST1507 DSAA: Caesar Cipher Encrypted Message Analyzer')

def main():

    # print the welcome message
    printWelcomeMessage()

    # loop forever the options until the user pick option 8
    option = None
    while option != '8':

        options = [
        'Encrypt/Decrypt Message',
        'Encrypt/Decrypt File',
        'Analyze letter frequency distribution',
        'Infer caesar cipher key from file',
        'Analyze, and sort encrypted files',
        'History menu',
        'Guess the word minigame',
        'Exit'
        ]

        mainMenu = MenuPrinter(options)
        mainMenu.display()
        option = mainMenu.getInputOption()

        # employing the dictionary switcher to act as the switch case like in javascript
        # I know switch match has been implemented on python 3.10 but I afraid you are using an older version of python hence I refuse to use it
        switcher = {
            '1': encryption,
            '2': encryption,
            '3': analyseLetter,
            '4': inferKey,
            '5': inferKey,
            '6': historyMenu,
            '7': miniGame,
            '8': exitMessage
        }

        # using the get method to get the appropriate function, or else, get the default function which will show error message, then call the chosen function
        switcher.get(option, default)(option)

    # once the user chose option 8 to exit the program, then the program will save the history into a json file and end the while loop and ultimately the program
    history.saveHistoryList()

if __name__ == "__main__":
    main()