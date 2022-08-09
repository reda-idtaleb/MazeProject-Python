from Labyrinthe import *

class UnexpectedValueException(Exception):
    pass

def verify_filename(s):
    if ".txt" in s:
        return s
    else:
        return s + ".txt" 

def ask_to_quit():
    answer = input("Do you really want to quit? y/n : ")
    print("\n")
    if answer is "y" :
        print("############## Goodbye! See you again ;) ##############")
        exit()
    elif answer is "n":
        print("Ok, good! :)\n")
        main()
    else:
        raise UnexpectedValueException("* Cannot accept the entered value : %s" % (answer))
    
def main():
    try:
        choice = int(input("-> Enter '1' if you want to generate a maze and solve it\n" +
                           "-> Enter '2' if you want to join a file containing a maze\n"+
                           "-> Enter '3' if you want to quit the game\n" +
                           "My choice: "))
        print("\n")
        if choice == 1:
            fName = input("** Choose a name for your file (The authorized type file is .txt).\n\n - Please, enter a name of your file : ")
            filename = verify_filename(fName)
            w = input(" - Choose the width  of your maze : ")
            h = input(" - Choose the height of your maze : ")
            
            l = Labyrinthe(int(w), int(h))
            l.write_maze_to_file(filename, w, h)
            
            print("Congrates! You can find your file on the main directory\n")
        elif choice == 2:
            l = Labyrinthe(0, 0)
            try:
                l = l.read_maze_from_file()
                resolution_path = l.find_a_way()
                print(l)
                print("\nThe solution is:\n%s\n" % (l.show_maze_after_resoluion(resolution_path)))
            except FileNotFoundError as e:
                print("\n###### Warning! %s ######\n" % (str(e)))
                main()        
        elif choice == 3:
            try:
                ask_to_quit()
            except UnexpectedValueException as e:
                print(str(e) + "\n")
                ask_to_quit()
        else:
            raise UnexpectedValueException("###### Warning! You have to inter the number 1, 2 or 3 ######")
            
    except ValueError:
        print("\n###### Warning: Only numbers accepted ######\n\n")
        main()
    except UnexpectedValueException as e:
        print("%s\n" % (str(e)))
        main()
    
def description():
    print("         *-----------------------------------------------------------------*")        
    print("         |       ******** Hello, and welcome to the maze game *********    |\n")
    print("         *-----------------------------------------------------------------*\n\n")
    print("   -----> Please Read Carefully: Tips/Ideas About How the Program Works <-----\n\n")
    print("** The program generally consists of creating mazes in text format, finding the solution of the mazes created and reading the text files whose contents are mazes, \
              finally displaying their resolutions.\n")                                              
    print("** The txt file will be created automatically after entering the name of your choice, remember that the extension must necessarily be (.txt).")
    print("The destination of the created file will initially be in the same project folder. According to your desire, you can place it in any location in your pc.")
    print("** To successfully create the maze that will be displayed in your file, you must first choose the size (width and length) of your maze.\n")
    print("** The values that will be entered for the maze size must be integers only.\n")
    print("** Please follow the instructions for a better generation of the maze.\n")

if __name__ == '__main__':
    #doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS, verbose=True)   
    description()
    while(True):
        main()