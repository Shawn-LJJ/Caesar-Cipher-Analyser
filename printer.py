# a simple class that takes in the list of option and be used to print when calling the .display() method
class MenuPrinter:
    def __init__(self, options) -> None:
        self.options =  options
        self.length = len(options)

    def display(self):
        print()
        print(f'Please select your choice: ({",".join([str(num) for num in range(1, self.length + 1)])})')
        print('\n'.join([f'{i + 1}. {option}' for i, option in enumerate(self.options)]))
    
    def getInputOption(self):
        # return with the user input which is trimmed from whitespaces 
        return input('Enter choice: ').strip()