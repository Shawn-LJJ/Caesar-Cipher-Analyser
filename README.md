# Caesar Cipher Analyser

This project is the submission of Data Structure & Algorithm CA1 assignment from Singapore Polytechnic AY23/24. 
The program allows users to encrypt/decrypt messages or entire text from txt files.
Not only that, it can infer the caesar cipher key from a txt file based on the number of characters occurrence and compare to the english language overall character occurrence. 
There are extra functionalities as part of the additional feature requirements. And they are the history menu and the guess-the-word minigame.

Even though I got an A from this assignment and the module as a whole as well, I have to admit that this project overall is not amazing.
The files are really messy. There is no organisation to this project at all. 
The main program is not very OOP as well. A lot of changes can be done to make this project more OOP. 
And to add more insult to my own injury, the program fails to consider a basic case: Reading an empty txt file will result in crashing the program (though it's somehow fixed post-submission but it currently reads the error message as the content)

## Prerequisite

This program is supposedly to be ran with Anaconda without installing any libraries, but it seems like it does not shipped with ```termcolor```, so install the library first. Alternatively, the program can just be ran with a regular Python environment, albeit you have to also install ```numpy``` as well.

With the required software, start the program by running the ```main.py``` file.

Note: when entering the reference frequencies file name, use englishtext.txt provided in the repo.