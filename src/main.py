from curses import ERR
from Labyrinthe import *
from tkinter.filedialog import asksaveasfile

import pyfiglet
import rich

class UnexpectedValueException(Exception):
    pass

CHOICE_COLOR = "cyan"
ERROR_COLOR  = "red"
SUCCES_COLOR = "green"
FRIENDLY_COLOR = "blue"

def verify_filename(s):
    if ".txt" in s:
        return s
    else:
        return s + ".txt" 

def ask_to_quit():
    answer = input("Do you really want to quit? y/n : ")
    print("\n")
    if answer == "y" :
        print_ascii_text("Goodbye ! See you again  ; )", color=FRIENDLY_COLOR)
        exit()
    elif answer == "n":
        print_ascii_text("Ok, good !  : )", color=FRIENDLY_COLOR)
        main()
    else:
        raise UnexpectedValueException("Cannot accept the entered value : %s" % (answer))

def show_game_menu():
    print('\n')
    print_ascii_text("Menu")
    rich.print(f"[%s]{'1.'}[/%s] Enter '1' if you want to generate a maze and solve it.\n"\
                f"[%s]{'2.'}[/%s] Enter '2' if you want to join a file containing a maze.\n"\
                f"[%s]{'3.'}[/%s] Enter '3' if you want to quit the game.\n\n" \
                %(CHOICE_COLOR, CHOICE_COLOR,
                CHOICE_COLOR, CHOICE_COLOR,
                CHOICE_COLOR, CHOICE_COLOR))
    
    choice = int(input("So, my choice is : "))
    print("\n")
    return choice

def build_ascii_text(text, font="standard", width=80):
    return pyfiglet.figlet_format(text, font=font, width=width)
    
 
def print_ascii_text(text, color="yellow", font="standard", width=80):
    title = build_ascii_text(text, font, width)
    rich.print(f'[%s]{title}[/%s]' %(color, color))  
    
def game_description():
    print_ascii_text("*----------*")        
    print_ascii_text(" Welcome to the PyMaze game !")
    print_ascii_text("*----------*")
    
    print_ascii_text("> Please Read Carefully <", 
                     color="red", 
                     font="invita",
                     width= 120)
    
    print("** The program consists of generating mazes in text format," \
          " finding their solutions, extracting the mazes from text files and finally displaying their solutions.\n")                                              
    print("** The text file will be created automatically after entering the name of your file." \
          " Remember that the extension must necessarily be (.txt).")
    print("** Please follow the instructions for a better generation of the maze.\n")

def show_stylish_warning(text, color=ERROR_COLOR):
    print_ascii_text(text="Warning !", color=color)
    rich.print("[%s]\t%s[/%s]\n\n" %(color, text, color))

def show_success_message(text, color):
    print_ascii_text("Finished !", color)
    rich.print(f'[%s]%s[/%s]' %(color, text,  color)) 

def answer_user(text, color, logo_mode=False):
    if logo_mode:
        print_ascii_text(text, color)
    else:
        rich.print("[%s]%s[/%s]" %(color, text, color))
    print("\n")
        
def main():
    try:
        choice = show_game_menu()
        if choice == 1:
            answer_user("Generating mazes =>", color=FRIENDLY_COLOR, logo_mode=True)
            print("** Choose a name for your file (The authorized type file is .txt).")
            try:
                file = asksaveasfile(initialfile='generated_maze.txt',
                                    defaultextension=".txt",
                                    filetypes=[("Text Documents", "*.txt"),])
                
                if not file:
                    raise FileNotFoundError("No file is saved.")
                
                answer_user(">> Saved file : %s" %(file.name), color=SUCCES_COLOR)
                
                filename = verify_filename(file.name)
                w = input("** Choose the width  of your maze : ")
                answer_user(">> Ok.", color=SUCCES_COLOR)
                h = input("** Choose the height of your maze : ")
                answer_user(">> Ok.", color=SUCCES_COLOR)
                
                l = Labyrinthe(int(w), int(h))
                l.write_maze_to_file(filename, w, h)
            
                show_success_message("  You can find your file here : %s." %(filename), color=SUCCES_COLOR) 
                
                import subprocess
                subprocess.call(["edit", filename])
            except FileNotFoundError as e:
                show_stylish_warning(str(e))
                main()
        elif choice == 2:
            answer_user("Solving Mazes =>", color=FRIENDLY_COLOR, logo_mode=True)
            l = Labyrinthe(0, 0)
            try:
                l = l.read_maze_from_file()
                print(l)
                resolution_path = l.find_a_way()
                rich.print("[%s]\nThe solution is:[/%s]" %(SUCCES_COLOR, SUCCES_COLOR))  
                rich.print(l.show_maze_after_resoluion(resolution_path))
            except FileNotFoundError as e:
                show_stylish_warning(str(e))
                main()        
        elif choice == 3:
            answer_user("Quit Game !?", color=ERROR_COLOR, logo_mode=True)
            try:
                ask_to_quit()
            except UnexpectedValueException as e:
                show_stylish_warning(str(e))
                ask_to_quit()
        else:
            raise UnexpectedValueException("You have to inter the number 1, 2 or 3 .")
            
    except ValueError:
        show_stylish_warning("Only numbers accepted !")
        main()
    except UnexpectedValueException as e:
        show_stylish_warning(str(e))
        main()

def ask_user_to_start(text, color=CHOICE_COLOR):
    rich.print("[%s]%s[/%s]" %(color, text, color))
    btn = input()
    return True if not btn else False

if __name__ == '__main__':
    #doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS, verbose=True)   
    game_description()
    pressed = False
    while(not pressed):
        pressed = ask_user_to_start("Press <Enter> to start ...")      
    while(pressed):
        main()