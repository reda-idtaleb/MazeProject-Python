"""
AUTHOR: ID-TALEB Réda
Project-name: PyMaze

"""
from collections import deque
import queue
from cell import *
from Stack import *

from random import choice

import random
import doctest

PATH_SYMBOL = "⬧"
STARTING_SYMBOL = "S"
FINISHED_SYMBOL = "T"

PATH_COLOR = "green"
FINISHED_COLOR = "red"

class Maze():
    """
    >>> game = Maze(10, 5)
    >>> game.get_width()
    10
    >>> game.get_height()
    5
    """
    
    def __init__(self, width, height):
        """
         build a maze grid of size width*height cells 

        :param width: (int) horizontal size of game 
        :param height: (int) vertical size of game 
        :return: (Maze) a maze grid of  width*height cells 
        
        :UC: width and height must be positive integers
             
        :Example:

        >>> maze = Maze(3, 3)
        >>> maze.get_width()
        3
        >>> maze.get_height()
        3
        >>> maze.get_grid()
        [[(0, 0), (1, 0), (2, 0)],
         [(0, 1), (1, 1), (2, 1)],
         [(0, 2), (1, 2), (2, 2)]]
        """
        self.__width = width
        self.__height = height
        self.__grid = [[Cell(x, y) for y in range(height)] for x in range(width)]
        
        self.__starting_cell:Cell = self.get_a_random_cell()
        self.__starting_cell.set_as_starting_cell()
        
        # The goal cell should be different from the starting cell
        self.__goal_cell:Cell = self.get_a_random_cell(without_starting_cell=True)
        self.__goal_cell.set_as_goal_cell()
    
    
    def get_neighboring_cells(self, cell:Cell, with_destroyed_walls:bool):
        """
        This function returns the neighbors of a cell that is in an real maze (with open wall).
        :param cell: a cell in the grid of game's
        :param with_destroyed_walls: set as True to get the neighboring cells from the original grid.
                                     without open walls.
        :return: a list of neighboors cells, that are possible to be visited,
                  depending on the position of the cell:
        :rtype: (list)
        :CU: none
        """
        directions = [['top', (0, -1)], ['bottom', (0, 1)], ['left', (-1, 0)], ['right', (1, 0)]]
        neighbor_cells = []
        neighb_cell = cell.get_destroyed_walls()
        for d, (i, j) in directions:
            x_neighb = cell.get_X_coordinate() + i
            y_neighb = cell.get_Y_coordinate() + j
            if (0 <= x_neighb < self.get_width()) and (0 <= y_neighb < self.get_height()):
                neighbor_cell = self.get_cell_at_coordinates(x_neighb, y_neighb)
                if with_destroyed_walls:
                    for c in neighb_cell:          
                        if d == c:
                            neighbor_cells.append([c, neighbor_cell])
                else:
                    if neighbor_cell.is_closed():
                        neighbor_cells.append([d, neighbor_cell])
        return neighbor_cells
    
    
    def cell_has_neighbors(self, cell):
        """
        :param cell: a cell in the maze
        :return: check if the cell has at least one neighboor or not,
        :rtype: (bool)
        :CU: none
        """
        s, g = self.get_starting_cell(), self.get_goal_cell()
        neighbors_list = self.get_neighboring_cells(cell, True)
        if cell == s or cell == g:
            return True
        return True if len(neighbors_list) >= 1 else False

                
    def get_a_random_cell(self, without_starting_cell=False, without_goal_cell=False):
        """ 
        :param without_starting_cell: (bool) Set as True to exclude the starting cell. 
                                             By default set as False.
        :param without_goal_cell: (bool) Set as True to exclude the goal cell.
                                         By default set as False.
        :return: (Cell) a random cell in the game's grid
        """
        w = self.get_width()
        h = self.get_height()
        x = random.randint(0, w - 1)
        y = random.randint(0, h - 1)
        if without_starting_cell:
            assert(self.__starting_cell != None)
            x = choice([i for i in range(0, w - 1) if i != self.__starting_cell.get_X_coordinate()])
            y = choice([i for i in range(0, h - 1) if i != self.__starting_cell.get_Y_coordinate()])
        elif without_goal_cell:
            assert(self.__goal_cell != None)
            x = choice([i for i in range(0, w - 1) if i != self.__goal_cell.get_X_coordinate()])
            y = choice([i for i in range(0, h - 1) if i != self.__goal_cell.get_Y_coordinate()])
        elif without_starting_cell and without_goal_cell:
            assert(self.__starting_cell != None)
            assert(self.__goal_cell != None)
            x = choice([i for i in range(0, w - 1) if i not in [self.__starting_cell.get_X_coordinate(), self.__goal_cell.get_X_coordinate()]])
            y = choice([i for i in range(0, h - 1) if i not in [self.__starting_cell.get_Y_coordinate(), self.__goal_cell.get_Y_coordinate()]])
        return self.get_cell_at_coordinates(x, y)

    def make_all_cells_unvisited(self):
        """
        This function marks all the cells of a labyrinth as invisited cells.
        Each cell corresponds to a boolean value "False".
        :return: returns a dictionary whose keys are the coordinates of the cells of a maze,
                 and the values ​​associated with each cell are False boolean values.
        :rtype: (dict)
        :CU: none
        """
        dic = {}
        for list_cellule in self.__grid:
            for cellule in list_cellule:
                dic[str(cellule)] = False
        return dic
    
    def generate_maze(self):

        """
        :side effect: this function modifies the initial representation of the labyrinth,
                      since it makes it possible to open the walls of a labyrinth.
                      Algorithm : Depth-first 
        :UC: none
        
        """
        w, h = self.get_width(), self.get_height()
        maze_size = w * h
        starting_cell:Cell = self.get_a_random_cell()
        visited_cell = 1
        l = []
        while visited_cell < maze_size:
            list_neighboor_cell = self.get_neighboring_cells(starting_cell, False)
            if not(list_neighboor_cell) :
                starting_cell = l.pop()
                continue
            direction, next_cell = random.choice(list_neighboor_cell) 
            starting_cell.destroy_a_wall(next_cell, direction)
            l.append(starting_cell)    
            starting_cell = next_cell
            visited_cell += 1
     
    def find_a_way(self):
        """
        check if there is a path between two points and return a list of the cells that are part of the path
        
        :return: (list) a List of coordinate of the truth way, which the first element is the first cell in the maze,
                 and the last element on  the list is the last elenment in the maze.
                 Algorithm: Breadth-first search
        """
        nums = queue.Queue()
        start = self.get_starting_cell()
        nums.put([start])
        path = [start]

        while not path[-1] == self.get_goal_cell(): 
            path = nums.get()
            for d, cell in self.get_neighboring_cells(path[-1], True):
                put = path + [cell]
                nums.put(put)
        return path
    
    def show_maze_after_resoluion(self, resolution_path, with_colors=True):
        width, height = self.get_width(), self.get_height()
        grid = ("+-" * width) + "+"
        for y in range(height):
            mur = "|"
            for x in range(width):
                symbol = self.__get_cell_symbol(x, y, when_solving=True, with_colors=with_colors)   
                cell = self.get_cell_at_coordinates(x, y)
                if cell in resolution_path:
                    mur = mur + "%s|" %(symbol) if cell.has_right_wall() \
                                                else mur + "%s%s" %(symbol, (symbol if symbol == PATH_SYMBOL else " "))
                else:
                    mur = mur + " |" if cell.has_right_wall() else mur + "  " 
            grid = grid + "\n" + mur
            mur = '+'
            for x in range(width):
                mur = mur + "-+" if self.get_cell_at_coordinates(x, y).has_bottom_wall() else mur + " +"
            grid = grid + "\n" + mur
        return grid                      
                          
    def write_maze_to_file(self, file, w, h):
        a = open(file, "w")
        self.generate_maze()
        a.write(str(w))
        a.write("\n")
        a.write(str(h))
        a.write("\n\n")
        a.write(str(self))
        a.close()
        
    def __repr__(self):
        """
        :return: a representation of a maze, or a representation of all
                 the cells that build a labyrinth. 
        :rtype: (list)
        :UC: none
        
        :Example:
        >>> game = Maze(3, 4)
        >>> game.__repr__()
        [[(0, 0), (1, 0), (2, 0)], 
         [(0, 1), (1, 1), (2, 1)], 
         [(0, 2), (1, 2), (2, 2)], 
         [(0, 3), (1, 3), (2, 3)]]
        """
        return str([[(x,y) for x in range(self.get_width())] for y in range(self.get_height())])
             
    def get_width(self):
        """
        :return: height of the grid
        :rtype: int
        :UC: none
        
        :Example:
        >>> game = Maze(3,4)
        >>> game.get_width()
        3
        """
        return self.__width
    
    def get_height(self):
        """
        :return: height of the grid
        :rtype: int
        :UC: none
        
        :Example:
        >>> game = Maze(3,4)
        >>> game.get_height()
        4
        """
        return self.__height
    
    def get_grid(self):
        """
        :return: The grid of the game
        :rtype: List
        :UC: none
        
        :Example:
        >>> game = Maze(3, 4)
        >>> game.get_grid()
        [[(0, 0), (1, 0), (2, 0)], 
         [(0, 1), (1, 1), (2, 1)], 
         [(0, 2), (1, 2), (2, 2)], 
         [(0, 3), (1, 3), (2, 3)]]
        """
        return self.__grid
        
    def get_cell_at_coordinates(self, x, y):
        """ 
        :param x: x-coordinate of a cell
        :type x: int
        :param y: y-coordinate of a cell
        :type y: int
        :return: the cell of coordinates (x,y) in the game's grid
        :type: cell
        :UC: 0 <= x < width of game and O <= y < height of game
        """
        return self.__grid[x][y]
    
    def get_goal_cell(self):
        return self.__goal_cell
    
    def set_goal_cell(self, new_goal_cell:Cell):
        self.__goal_cell.unset_goal_cell()
        new_goal_cell.set_as_goal_cell()
        self.__goal_cell = new_goal_cell
    
    def get_starting_cell(self):
        return self.__starting_cell
    
    def set_starting_cell(self, new_starting_cell:Cell):
        self.__starting_cell.unset_starting_cell()
        new_starting_cell.set_as_starting_cell()
        self.__starting_cell = new_starting_cell
        
    def __get_cell_symbol(self, x, y, when_solving=False, with_colors=False):
        if self.get_cell_at_coordinates(x, y).is_goal_cell():
            symbol = "[%s]%s[/%s]" %(FINISHED_COLOR, FINISHED_SYMBOL, FINISHED_COLOR) if with_colors else FINISHED_SYMBOL
        elif self.get_cell_at_coordinates(x, y).is_starting_cell():
            symbol = STARTING_SYMBOL  
        else:
            if when_solving:
                symbol = "[%s]%s[/%s]" %(PATH_COLOR, PATH_SYMBOL, PATH_COLOR) if with_colors else PATH_SYMBOL
            else:    
                symbol = " "
        return symbol
    
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
                symbol = self.__get_cell_symbol(x, y)
                if self.get_cell_at_coordinates(x,y).has_right_wall():
                    mur = mur + "%s|" %(symbol)
                else:
                    mur = mur + "%s " %(symbol)
            grid = grid + "\n" + mur
            mur = '+'
            for x in range(width):
                if self.get_cell_at_coordinates(x,y).has_bottom_wall():
                    mur = mur + "-+"
                else:
                    mur = mur + " +" 
            grid = grid + "\n" + mur
        return grid