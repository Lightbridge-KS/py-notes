import sys

class Notepad:
    def __init__(self, author: str, file_name: str) -> None:
        self.author = author
        self._file_name = file_name
        
    def _show_instructions(self) -> None:
        print(f'Welcome to Notepad, {self.author}!')
        print('Commands:')
        print('1 - write note')
        print('2 - display note')
        print('0 - exit Notepad')
    
    def _write_note(self) -> None:
        user_input: str = input('Enter a note: ')

        with open(self._file_name, 'w') as note:
            note.write(user_input)
            
        print("Note saved successfully!")
            
    def _display_note(self) -> None:
        try:
            with open(self._file_name, 'r') as note:
                text: str = note.read()
                print(f'Bot: {text}')
        except FileNotFoundError:
            print('Bot: You need to write a note first!')
            
    def _exit_notepad(self) -> None:
        print(f'See you next time, {self.author}!')
        sys.exit()
        
    def run(self) -> None:
        self._show_instructions()
        while True:
            user_input: str = input(f'{self.author}: ')

            if user_input not in ('0', '1', '2'):
                print('Bot: Please enter a valid choice.')
                continue
            
            if user_input == '1':
                self._write_note()
            elif user_input == '2':
                self._display_note()
            elif user_input == '0':
                self._exit_notepad()
            else:
                print(f'Bot: Unknown command {user_input}.')
                
def main():
    notepad: Notepad = Notepad('Bob', 'project/note.txt')
    notepad.run()
    
if __name__ == '__main__':
    main()