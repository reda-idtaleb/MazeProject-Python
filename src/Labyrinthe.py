"""
AUTHOR: ID-TALEB Réda
Project-name: PyMaze

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
    
    
    def __repr__(self):
        """
        :return: a representation of a maze, or a representation of all
                 the cells that build a labyrinth. 
        :rtype: (list)
        :UC: none
        
        :Example:
        >>> game = Labyrinthe(3,4)
        >>> game.__repr__()
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
                
                
    def get_possible_neighboring_cells(self, cell):
        """
          This function returns the neighbors of a cell that is in an initial labyrinth (without open wall).
         :param cell: a cell in the grid of game's
         :return: a list of neighboors cells, that are possible to be visited,
                  depending on the position of the cell:
                  1- if the cell is located in the corner of the grid, so there will be two neighboring cells.
                  2- if the cell is located on the edges of the grid, then there are three neighboring cells.
                  3- for the other case where the cell is located in the middle of the grid, so there will be four neighboring cells.
         :rtype: (list)
         :CU: none
         
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
                if neighboor_cell.is_closed():
                    list_of_neighboors.append([d, neighboor_cell])
        return list_of_neighboors
    
    
    def get_cell_neighbors(self, cell):
        """
        This function returns the neighbors of a cell that is in an real maze (with open wall).
        :param cell: a cell in the grid of game's
        :return: a list of neighboors cells, that are possible to be visited,
                  depending on the position of the cell:
        :rtype: (list)
        :CU: none
        """
        width = self.get_width()
        height = self.get_height()
        liste_direction = [['haut', (0, -1)], ['bas', (0, 1)], ['gauche', (-1, 0)], ['droite', (1, 0)]]
        list_of_neighboors = []
        cell_voisin = cell.get_destroyed_walls()
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
        liste_neigh = self.get_cell_neighbors(cell)
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
                
                
    def get_a_random_cell(self):
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

    
    def make_all_cells_unvisited(self):
        """
        this function marks all the cells of a labyrinth as invisited cells,
        each cell of which corresponds to a Boolean value "False".
        :return: returns a dictionary whose keys are the coordinates of the cells of a maze,
                 and the values ​​associated with each cell are False Boolean values.
        :rtype: (dict)
        :CU: none
        """
        dic = {}
        for list_cellule in self.labyrinthe:
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
            list_neighboor_cell = self.get_possible_neighboring_cells(starting_cell)
            if not(list_neighboor_cell) :
                starting_cell = l.pop()
                continue
            direction, next_cell = random.choice(list_neighboor_cell) 
            starting_cell.destroy_a_wall(next_cell, direction)
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
        x, y = self.get_width(), self.get_height()
        solution, trash_stack = Stack(), Stack()
        
        starting_cell = self.labyrinthe[0][0]
        solution.push(starting_cell)
        
        dic_state = self.make_all_cells_unvisited()
        dic_state[str(starting_cell)] = True
        
        visited_cell = 1
        while visited_cell < x*y:
            top_s = solution.top()
            neighboord_cell_top_s  = self.get_cell_neighbors(top_s)
            for (_, cell_neigh) in neighboord_cell_top_s:
                if dic_state[str(cell_neigh)] == False and self.cell_has_neighboor(solution.top()) == True:
                    solution.push(cell_neigh)
                    dic_state[str(cell_neigh)] = True
                elif dic_state[str(cell_neigh)] == True and self.cell_has_neighboor(solution.top()) == False:
                    trash_stack.push(solution.pop())            
            if solution.top() == self.get_cell_at_coordinate(x-1, y-1):
                break
            visited_cell += 1
        path = []    
        while not(solution.is_empty()):
            cell = solution.pop()
            path = path + [cell.__repr__()]  
        path.reverse()
        return path
    
    def show_maze_after_resoluion(self, resolution_path):
        width, height = self.get_width(), self.get_height()
        grid = ("+-" * width) + "+"
        for y in range(height):
            mur = "|"
            for x in range(width):
                if (x, y) in resolution_path:
                    mur = mur + ".|" if self.get_cell_at_coordinate(x, y).get_right_wall() else mur + ".." 
                else:
                    mur = mur + " |" if self.get_cell_at_coordinate(x, y).get_right_wall() else mur + "  " 
            grid = grid + "\n" + mur
            mur = '+'
            for x in range(width):
                if (x, y) in resolution_path:
                    mur = mur + "-+" if self.get_cell_at_coordinate(x, y).get_bottom_wall() else mur + ".+"
                else:
                    mur = mur + "-+" if self.get_cell_at_coordinate(x, y).get_bottom_wall() else mur + " +"
            grid = grid + "\n" + mur
        return grid  
                    
    def read_maze_from_file(self):
        """
        A function that will read a file and that returns the labyrinth of the type Labyrinth.
        """
        from tkinter import filedialog as fd
        file = fd.askopenfilename(title="Open a file",
                                  filetypes=(('text files', '*.txt'),)
                                  )
        if not file:
            raise FileNotFoundError("No file is selected.")

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
                            cell1.destroy_a_wall(cell2, "droite")
                            if(lines[l+1][i-1] == ' '):
                                cell3 = lab.get_cell_at_coordinate(x, y+1)
                                cell1.destroy_a_wall(cell3, "bas")
                            x += 1    
                        elif (lines[l][i] == '|') and i > 0:
                            cell1 = lab.get_cell_at_coordinate(x, y)
                            if(lines[l+1][i-1] == ' '):
                                cell3 = lab.get_cell_at_coordinate(x, y+1)
                                cell1.destroy_a_wall(cell3, "bas") 
                            x += 1    
                y += 1
                x = 0
        return lab                     
                          
    def write_maze_to_file(self, file, w, h):
        a = open(file, "w")
        self.generate_maze()
        a.write(str(w))
        a.write("\n")
        a.write(str(h))
        a.write("\n\n")
        a.write(self.__str__())
        a.write("\n\n")
        resolution_path = self.find_a_way()
        a.write("You can think before looking at the solution, don't cheat ;)!\n\n" 
                + "Otherwise, the resolution is:\n"  
                + self.show_maze_after_resoluion(resolution_path))
        a.close()