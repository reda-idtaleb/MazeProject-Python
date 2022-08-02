"""
AUTHOR: OUKOUKAS Ferial, ID-TALEB Réda
Projet: Labyrinthe

"""
from Cellule import *
from Stack import *
import random
import doctest

class Labyrinthe():
    """
    >>> game = Labyrinthe(10, 5)
    >>> game.get_width()
    10
    >>> game.get_height()
    5
    """
    
    def __init__(self, width, height):
        """
         build a maze grid of size width*height cells 

        :param width: horizontal size of game 
        :type width: int
        :param height: vertical size of game 
        :type height: int
        :return: a maze grid of  width*height cells 
        :rtype: Labyrinthe
        :UC: width and height must be positive integers
             
        :Example:

        >>> game = Labyrinthe(10, 5)
        >>> game.get_width()
        10
        >>> game.get_height()
        5

        """
        self.width = width
        self.height = height
        self.labyrinthe = [[Cell(x,y) for y in range(height)] for x in range(width)]
    
    
    def __repre__(self):
        """
        :return: a representation of a maze, or a representation of all
                 the cells that build a labyrinth. 
        :rtype: (list)
        :UC: none
        
        :Example:
        >>> game = Labyrinthe(3,4)
        >>> game.__repre1__()
        [[(0, 0), (1, 0), (2, 0)], [(0, 1), (1, 1), (2, 1)], [(0, 2), (1, 2), (2, 2)], [(0, 3), (1, 3), (2, 3)]]
        """
        labyrinthe = [[(x,y) for x in range(self.get_width())] for y in range(self.get_height())]
        return (labyrinthe)
     
     
    def get_width(self):
        """
        :return: height of the grid in self
        :rtype: int
        :UC: none
        
        :Example:
        >>> game = Labyrinthe(3,4)
        >>> game.get_width()
        3
        """
        return self.width
    
    def get_height(self):
        """
        :return: height of the grid in self
        :rtype: int
        :UC: none
        
        :Example:
        >>> game = Labyrinthe(3,4)
        >>> game.get_height()
        4
        """
        return self.height
    
    
    def get_cell_at_coordinate(self, x, y):
        """ 
        :param x: x-coordinate of a cell
        :type x: int
        :param y: y-coordinate of a cell
        :type y: int
        :return: the cell of coordinates (x,y) in the game's grid
        :type: cell
        :UC: 0 <= x < width of game and O <= y < height of game
        """
        return self.labyrinthe[x][y]
    
    
    def __str__(self):
        """
        :return: a string representation of a grid
        :rtype: str
        :UC: none
        :Example:
        
        """
        width = self.get_width()
        height = self.get_height()
        grid = ("+-" * width) + "+"
        for y in range(height):
            mur = "|"
            for x in range(width):
                if self.get_cell_at_coordinate(x,y).get_right_wall():
                    mur = mur + " |"
                else:
                    mur = mur + "  " 
            grid = grid + "\n" + mur
            mur = '+'
            for x in range(width):
                if self.get_cell_at_coordinate(x,y).get_bottom_wall():
                    mur = mur + "-+"
                else:
                    mur = mur + " +"
            grid = grid + "\n" + mur
        return grid   
                
                
    def neighboors_cells_possible(self, cell):
        """
          this function return the neighbors of a cell that is in an initial labyrinth (without open wall).
         :param cell: a cell in the grid of game's
         :return: a list of neighboors cells, that are possible to be visited,
                  depending on the position of the cell:
                  1- if the cell is located in the corner of the grid, so there will be two neighboring cells.
                  2- if the cell is located on the edges of the grid, then there are three neighboring cells.
                  3- for the other case where the cell is located in the middle of the grid, so there will be four neighboring cells.
         :rtype: (list)
         :CU: aucune
         
        """
        width = self.get_width()
        height = self.get_height()
        liste_direction = [['haut', (0, -1)], ['bas', (0, 1)], ['gauche', (-1, 0)], ['droite', (1, 0)]]
        list_of_neighboors = []
        for d, (i,j) in liste_direction:
            x_second = cell.x + i
            y_second = cell.y + j
            if (0 <= x_second < width) and (0 <= y_second < height):
                neighboor_cell = self.get_cell_at_coordinate(x_second, y_second)
                if neighboor_cell.is_closed_cell():
                    list_of_neighboors.append([d, neighboor_cell])
        return list_of_neighboors
    
    
    def  neighbors_cell_in_real_maze(self, cell):
        """
          this function return the neighbors of a cell that is in an real maze (with open wall).
         :param cell: a cell in the grid of game's
         :return: a list of neighboors cells, that are possible to be visited,
                  depending on the position of the cell:
         :rtype: (list)
         :CU: aucune
    
        """
        width = self.get_width()
        height = self.get_height()
        liste_direction = [['haut', (0, -1)], ['bas', (0, 1)], ['gauche', (-1, 0)], ['droite', (1, 0)]]
        list_of_neighboors = []
        cell_voisin = cell.is_not_closed_cell()
        for d, (i,j) in liste_direction:
            for c in cell_voisin:
                if d == c:
                    x_second = cell.x + i
                    y_second = cell.y + j
                    if (0 <= x_second < width) and (0 <= y_second < height):
                        neighboor_cell = self.get_cell_at_coordinate(x_second, y_second)
                        list_of_neighboors.append([c, neighboor_cell])
        return list_of_neighboors
    
    
    def cell_has_neighboor(self, cell):
        """
         this function checks if the cell has at most one neighbor, ie it is a dead end.
         except the case of the first cell and the case of the last cell.
        :param cell: a cell in the maze
        :return: check if the cell has the neighboor or not,
                 - return True if the cell really has at least one neighboor.
                 - return False if the cell has any neighboor to be visited.
                 - a special case : * True if the coordinate of cell is (0,0), 
                                    * True if the coordinate of the cell is the last cell in th maze.
        :rtype: (bool)
        :CU: none
        
        :Example:
        >>> game = Labyrinthe(4,4)
        >>> game.generate_maze()
        >>> cel = game.get_random_cell()
        >>> game.cell_has_neighboor(cel)
        True
        """
        x = self.get_width()
        y = self.get_height()
        cell_depart = self.get_cell_at_coordinate(0, 0)
        cell_arriver = self.get_cell_at_coordinate(x-1, y-1)
        liste_neigh = self.neighbors_cell_in_real_maze(cell)
        if cell == cell_depart:
            return True
        if cell == cell_arriver:
            return True
        if len(liste_neigh) > 1:
                return True
        else:
            for (d,i) in liste_neigh:
                if len(liste_neigh) == 1 and (i != cell_depart and i != cell_arriver):
                    return False
                else:
                    return True
                
                
    def get_random_cell(self):
        """ 
        :param x: x-coordinate of a cell
        :type x: int
        :param y: y-coordinate of a cell
        :type y: int
        :return: a random cell in the game's grid
        :type: cell
        :UC: 0 <= x < width of game and O <= y < height of game
        """
        w = self.get_width()
        h = self.get_height()
        x = random.randint(0, w - 1)
        y = random.randint(0, h - 1)
        return self.labyrinthe[x][y]

    
    def cell_state(self):
        """
        this function marks all the cells of a labyrinth as invisited cells,
        each cell of which corresponds to a Boolean value "False".
        :return: returns a dictionary whose keys are the coordinates of the cells of a maze,
                 and the values ​​associated with each cell are False Boolean values.
        :rtype: (dict)
        :CU: none
        """
        labyrinthe = self.labyrinthe
        w = self.get_width()
        h = self.get_height()
        length_labyrinthe = w*h
        dic = {}
        for list_cellule in labyrinthe:
            for cellule in list_cellule:
                dic[str(cellule)] = False
        return dic
    
    def generate_maze(self):

        """
        :side effect: this function modifies the initial representation of the labyrinth,
                      since it makes it possible to open the walls of a labyrinth.
                      ALgorithme : the exhaustive exploration
        :UC: none
        
        """
        w = self.get_width()
        h = self.get_height()
        length_maze = w * h
        starting_cell = self.get_cell_at_coordinate(0, 0)
        number_of_cell = 1
        l = []
        while number_of_cell < length_maze:
            list_neighboor_cell = self.neighboors_cells_possible(starting_cell)
            if not(list_neighboor_cell) :
                starting_cell = l.pop()
                continue
            direction, next_cell = random.choice(list_neighboor_cell) 
            starting_cell.wall_destroyed_between_2_cells(next_cell, direction)
            l.append(starting_cell)    
            starting_cell = next_cell
            number_of_cell += 1
     
     
    def find_a_way(self):
        """
        check if there is a path between two points and return a list of the cells that are part of the path
        
        :return: a List of coordinate of the truth way, which the first element is the first cell in the maze,
                 and the last element on  the list is the last elenment in the maze.
                 Algorithme: depth first search
        :rtype: list
        """
        x = self.get_width()
        y = self.get_height()
        s = Stack()
        s1 = Stack()
        cell_depart = self.labyrinthe[0][0]
        s.push(cell_depart)
        dic_state = self.cell_state()
        dic_state[str(cell_depart)] = True
        nv = 1
        while nv < x*y:
            top_s = s.top()
            neighboord_cell_top_s  = self.neighbors_cell_in_real_maze(top_s)
            for (dire, cell_neigh) in neighboord_cell_top_s:
                if dic_state[str(cell_neigh)] == False and self.cell_has_neighboor(s.top()) == True:
                    s.push(cell_neigh)
                    dic_state[str(cell_neigh)] = True
                elif dic_state[str(cell_neigh)] == True and self.cell_has_neighboor(s.top()) == False:
                    s1.push(s.pop())            
            if s.top() == self.get_cell_at_coordinate(x-1, y-1):
                break
            nv += 1
        L = []    
        while not(s.is_empty()):
            b = s.pop()
            L = L + [b.__repre__()]  
        L.reverse()
        return L
                    
    def read_file(self):
        """
        a function that will read a file and that returns the labyrinth of the type Labyrinth
        """
        file = input("Enter the file name(only .txt extension): ")
        op_file = open(file, "r")
        lines = op_file.readlines()
        w, h = int(lines[0][:-1]), int(lines[1][:-1])
        lab = Labyrinthe(w, h)
        x, y = 0, 0
        for l in range(4, len(lines)):
            if (l%2 == 0):
                for i in range(w*2+1):
                    if (i%2 == 0):
                        if (lines[l][i] == ' '):            
                            cell1 = lab.get_cell_at_coordinate(x, y)
                            cell2 = lab.get_cell_at_coordinate(x+1, y)
                            cell1.wall_destroyed_between_2_cells(cell2, "droite")
                            if(lines[l+1][i-1] == ' '):
                                cell3 = lab.get_cell_at_coordinate(x, y+1)
                                cell1.wall_destroyed_between_2_cells(cell3, "bas")
                            x += 1    
                        elif (lines[l][i] == '|') and i > 0:
                            cell1 = lab.get_cell_at_coordinate(x, y)
                            if(lines[l+1][i-1] == ' '):
                                cell3 = lab.get_cell_at_coordinate(x, y+1)
                                cell1.wall_destroyed_between_2_cells(cell3, "bas") 
                            x += 1    
                y += 1
                x = 0
        return lab             
                      
    def maze_on_file(self, file, w, h):
        a = open(file, "w")
        self.generate_maze()
        a.write(str(w))
        a.write("\n")
        a.write(str(h))
        a.write("\n\n")
        a.write(self.__str__())
        a.write("\n\n")
        a.write("Vous pouvez réflichir avant de regarder la solution, ne trichez pas ;)!\n\n Sinon, la résolution de ce labyrinthe est:\n "+ str(self.find_a_way()))
        a.close()

def verify_filename(s):
    if ".txt" in s:
        return s
    else:
        return s + ".txt" 
    
def main():
    try:
        choice = int(input("-> Enter '1' if you want to generate a maze and solve it\n" +
                           "-> Enter '2' if you want to join a file containing a maze\n"+
                           "-> Enter '3' if you want to quit the game\n" +
                           "My choice: "))
        print("\n")
        if choice == 1:
            fName = input("** Please choose a name for your file. ( Veuillez entrez un nom pour votre fichier.)\n** Le type du fichier adopté, est le type (.txt).\n\n - Enter the name Please: ")
            filename = verify_filename(fName)
            w = input(" - Choose the width  of your maze : ")
            h = input(" - Choose the height of your maze : ")
            
            l = Labyrinthe(int(w), int(h))
            l.maze_on_file(filename, w, h)
            
            print("Congrates! You can find your file on the main directory\n")
        elif choice == 2:
            l = Labyrinthe(0, 0)
            try:
                l = l.read_file()
                print(l)
                print("The solution is: ", l.find_a_way(), "\n")
            except FileNotFoundError:
                print("\n###### Warning! File not found. Make sure you enter an existing file! ######\n")
                main()        
        elif choice == 3:
            print("############## Goodbye! See you again ;) ##############")
            exit()
        else:
            print("\n###### Warning! You have to inter the number 1 or 2 or 3 ######\n")
            main()
    except ValueError:
        print("\n###### Warning: Only numbers accepted ######\n###### Please enter a valid number again! ######\n")
        main()
    
def description():
    print("         *-----------------------------------------------------------------*")        
    print("         |******** Bonjour, et bienvenu dans le jeu du labyrinthe *********|\n         *-----------------------------------------------------------------*\n\n")
    print("   -----> A Lire attentivement: Astuces/idées à-propos du fonctionnement du programme <-----\n\n")
    print("** Le programme consiste généralement à créer des labyrinthes au format text, trouver la solution de chaque labyrinthe crée, et à lire les fichiers text dont leurs contenus sont des labyrinthes, puis l'affichage de ses résolutions\n")                                              
    print("** Le fichier text sera créer automatiquement après la saisie du nom de votre choix, on rapelle que l'extension doit être forcément (.txt).\n   La destination du fichier crée sera initialement dans le même dossier du projet. Selon votre désire, vous pouvez le placer dans n'importe quel emplacement dans votre pc.\n")
    print("** Pour Réussir à créer le labyrinthe qui sera afficher dans votre fichier, vous devrez d'abord choisir la taille (largueur et longueur) de votre labyrinthe.\n")
    print("** Les valeurs qui seront entrées pour la taille du labyrinthe, doivent être uniquement des entiers.\n")
    print("** Veuillez respecter les consignes pour une meilleure génération du labyrinthe.\n")

if __name__ == '__main__':
    #doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS, verbose=True)   
    description()
    while(True):
        main()
