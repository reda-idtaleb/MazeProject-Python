from maze import *
from tkinter.filedialog import asksaveasfile
from music_player import MusicPlayer, DEFAULT_MUSIC
from maze_reader import ParseException, read_maze_from_file

import pyfiglet
import rich

CHOICE_COLOR = "cyan"
ERROR_COLOR  = "red"
SUCCES_COLOR = "green"
FRIENDLY_COLOR = "blue"
STANDARD_COLOR = "white"

    
class Main():
    def __init__(self):
        self.__music_player = MusicPlayer(randomize=False, music_name=DEFAULT_MUSIC)
        self.__music_player.playsound()
    
    def verify_filename(self, string):
        if ".txt" in string:
            return string
        else:
            return string + ".txt" 

    def ask_to_quit(self):
        answer = input("Do you really want to quit? y/n : ")
        print("\n")
        if answer == "y" :
            self.print_ascii_text("Goodbye ! See you again  ; )", color=FRIENDLY_COLOR)
            exit()
        elif answer == "n":
            self.print_ascii_text("Ok, good !  : )", color=FRIENDLY_COLOR)
            Main().main()
        else:
            raise UnexpectedValueException("Cannot accept the entered value : %s" % (answer))

    def show_game_menu(self):
        def _create_menu_item(item_number:int, text, color=CHOICE_COLOR):
            rich.print("[%s]%d.[/%s] Enter '%d' %s\n" %(color, item_number, color, item_number, text))
        
        print('\n')
        self.print_ascii_text("Menu")
        
        _create_menu_item(1, "if you want to generate a maze as a txt file.")
        _create_menu_item(2, "if you want to join a file containing a maze and solve it.")
        _create_menu_item(3, "if you want to play/stop a music.")
        _create_menu_item(4, "if you want to quit the program.")
        
        choice = int(input("So, my choice is : "))
        print("\n")
        return choice

    def build_ascii_text(self, text, font="standard", width=80):
        return pyfiglet.figlet_format(text, font=font, width=width)
        
    
    def print_ascii_text(self, text, color="yellow", font="standard", width=80):
        title = self.build_ascii_text(text, font, width)
        rich.print(f'[%s]{title}[/%s]' %(color, color))  
        
    def game_description(self):
        self.print_ascii_text("*----------*")        
        self.print_ascii_text(" Welcome to the PyMaze game !")
        self.print_ascii_text("*----------*")
        
        self.print_ascii_text("> Please Read Carefully <", 
                        color="red", 
                        font="invita",
                        width= 120)
        
        print("** The program consists of generating mazes in text format," \
            " finding their solutions, extracting the mazes from text files and finally displaying their solutions.\n")                                              
        print("** The text file will be created automatically after entering the name of your file." \
            " Remember that the extension must necessarily be (.txt).")
        print("** Please follow the instructions for a better generation of the maze.\n")

    def show_stylish_warning(self, text, color=ERROR_COLOR):
        self.print_ascii_text(text="Warning !", color=color)
        rich.print("[%s]\t%s[/%s]\n\n" %(color, text, color))

    def show_success_message(self, text, color):
        self.print_ascii_text("Finished !", color)
        rich.print(f'[%s]%s[/%s]' %(color, text,  color)) 

    def answer_user(self, text, color, logo_mode=False, new_line_after=True):
        if logo_mode:
            self.print_ascii_text(text, color)
            print("\n")
        else:
            rich.print("%s[%s]%s[/%s]%s" %("" if new_line_after else "\n",
                                        color, 
                                        text, 
                                        color,
                                        "\n" if new_line_after else ""))
    
    def ask_user_to_start(self, text, color=CHOICE_COLOR):
        rich.print("[%s]%s[/%s]" %(color, text, color))
        btn = input()
        return True if not btn else False
        
    def main(self):
        try:
            choice = self.show_game_menu()
            if choice == 1:
                self.answer_user("Generating mazes =>", color=FRIENDLY_COLOR, logo_mode=True)
                print("** Choose a name for your file (The authorized type file is .txt).")
                try:
                    file = asksaveasfile(initialfile='generated_maze.txt',
                                        defaultextension=".txt",
                                        filetypes=[("Text Documents", "*.txt"),])
                    
                    if not file:
                        raise FileNotFoundError("No file is saved.")
                    
                    self.answer_user(">> Saved file : %s" %(file.name), color=SUCCES_COLOR)
                    
                    filename = self.verify_filename(file.name)
                    w = input("** Choose the width  of your maze : ")
                    self.answer_user(">> Ok.", color=SUCCES_COLOR)
                    h = input("** Choose the height of your maze : ")
                    self.answer_user(">> Ok.", color=SUCCES_COLOR)
                    
                    maze = Maze(int(w), int(h))
                    maze.write_maze_to_file(filename, w, h)
                
                    self.show_success_message("  You can find your file here : %s." %(filename), color=SUCCES_COLOR) 
                    
                    import subprocess
                    subprocess.call(["edit", filename])
                except FileNotFoundError as e:
                    self.show_stylish_warning(str(e))
                    self.main()
            elif choice == 2:
                self.answer_user("Solving Mazes =>", color=FRIENDLY_COLOR, logo_mode=True)
                try:
                    maze:Maze = read_maze_from_file()
                    self.answer_user("The maze:", ERROR_COLOR, new_line_after=False)
                    print(maze)

                    resolution_path = maze.find_a_way()
                    self.answer_user("The solution is:", SUCCES_COLOR, new_line_after=False)  
                    self.answer_user(maze.show_maze_after_resoluion(resolution_path), STANDARD_COLOR)
                except FileNotFoundError as e:
                    self.show_stylish_warning(str(e))
                    self.main()
                except ParseException as e:
                    self.show_stylish_warning(str(e))
                    self.main()    
                        
            elif choice == 3:
                self.answer_user("Music Player =>", color=FRIENDLY_COLOR, logo_mode=True)
                if self.__music_player.is_playing:
                    self.__music_player.pause()
                    self.answer_user("The music is stopped.", color=SUCCES_COLOR)
                else:
                    self.__music_player.playsound()
                    self.answer_user("Playing the music ...", color=SUCCES_COLOR)                    
            elif choice == 4:
                self.answer_user("Quit Game !?", color=ERROR_COLOR, logo_mode=True)
                try:
                    self.ask_to_quit()
                except UnexpectedValueException as e:
                    self.show_stylish_warning(str(e))
                    self.ask_to_quit() 
            else:
                raise UnexpectedValueException("You have to inter the number 1, 2 or 3 .")
                
        except ValueError:
            self.show_stylish_warning("Only numbers accepted !")
            self.main()
        except UnexpectedValueException as e:
            self.show_stylish_warning(str(e))
            self.main()
         

class UnexpectedValueException(Exception):
    pass
 
    
if __name__ == '__main__':
    main = Main()
    
    #doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS, verbose=True)   
    main.game_description()
    
    pressed = False
    while(not pressed):
        pressed = main.ask_user_to_start("Press <Enter> to start ...")      
    while(pressed):
        main.main()