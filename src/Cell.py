"""
AUTHOR: ID-TALEB Réda
Project-name: PyMaze
"""
import random


class Cell():
    
    """
       Create a Cell in the maze.
       A cell in the maze is a point which may be surrounded by walls in all directions,
       
       :Examples:
       
       >>> cell1 = Cell(0,0)
       >>> cell2 = Cell(0,1)
       >>> cell1.is_closed()
       True
       >>> cell2.is_closed()
       True
       >>> cell1.destroy_a_wall(cell2, "left")
       >>> cell1.has_left_wall()
       False
       >>> cell2.has_right_wall()
       False
       >>> cell1.is_closed()
       False
       >>> cell2.is_closed()
       False
    """
    # The top of a cell is the bottom of the cell above it and vice versa.
    # The right of a cell is the left of its side cell and vice versa.
    __cell_pairs = {"top": "bottom", 
                    "bottom": "top", 
                    "right": "left", 
                    "left": "right"}  
                                                                                                                                              
    def __init__(self, x, y):
        """
        Create a cell specified by its (x, y) coordinates.
        Initially, all the walls of a cell exist.
        :param x: (int) The X coordinate of a cell.
        :param y: (int) The Y coordinate of a cell.
                 
        :UC: none
        :Examples:

        >>> cel = Cell(0, 0)
        >>> cel.is_closed()
        True
        >>> cell = Cell(0, 1)
        >>> cell.is_closed()
        True
        >>> cel.destroy_a_wall(cell, "left")
        >>> cel.is_closed()
        False
        """
        # create the coordinates of a cell
        self.__x = x
        self.__y = y
        # a dictionary that represents the 4 walls surrounding the cell in a labyrinth,
        # the value "True" means the walls exist.
        self.__walls = {'top': True, 'bottom': True, 'left': True, 'right': True}
    
    def is_closed(self):
        """
        :return: True if all the walls of self are closed , False otherwise
        :rtype: (bool)
        :UC: none
        :Example:

        >>> destroyed_cell = Cell(0,0)
        >>> destroyed_cell.is_closed()
        True
        >>> cell = Cell(0,1) 
        >>> destroyed_cell.destroy_a_wall(cell, "left")
        >>> destroyed_cell.is_closed()
        False

        """
        for i in self.__walls.values():
            if i == False:
                return False
        return True
    
    def destroy_a_wall(self, neighboor_cell, wall:str):
        """
        :param cell: (Cell) The neighboor cell.
        :param wall: (str) A wall of the self cell to destroy.
        :return: None
        :side effect: Modify a wall status. Destroy the corresponding wall that is passed as parameter. 
                      The wall shared between two cells.
        :UC: none
        
        :Examplez:

        >>> cell1 = Cell(0,0)
        >>> cell2 = Cell(0,1)
        >>> cell1.destroy_a_wall(cell2, "left")
        >>> cell1.is_closed()
        False
        >>> cell1.get_all_walls()
        {'top': True, 'bottom': True, 'left': False, 'right': True}
        >>> cell2.get_all_walls()
        {'top': True, 'bottom': True, 'left': True, 'right': False}
        """
        #If you want to destroy a wall between two cells, 
        # all you have to do is destroy a wall of the current cell (self). 
        # Indeed, since the cell shares its wall with the neighboring cell, 
        # therefore automatically the wall of the other cell is also destroyed.
        self.__walls[wall] = False
        neighboor_cell.__walls[self.__cell_pairs[wall]] = False
        
    def get_destroyed_walls(self):
        """
        :return: a list of neighboor cells which the wall are destroyed.
        :rtype: (list)
        :UC: none

        :Examples:

        >>> left_cell = Cell(0,0)
        >>> left_cell.is_closed()
        True
        >>> right_cell = Cell(0,1) 
        >>> left_cell.destroy_a_wall(right_cell, "left")
        >>> left_cell.get_destroyed_walls()
        ['left']
        """
        l = []
        if not(self.is_closed()):
            for i in self.__walls.keys():
                if self.__walls[i] == False:
                    l = l + [i]
        return l
    
    def get_X_coordinate(self):
        """
        :return: the x coordinate of the cell.
        :rtype: (int)
        :UC: none
        
        :Examples:
        >>> cell = Cell(1,0)
        >>> cell.get_X_coordinate()
        1
        """
        return self.__x
    
    def get_Y_coordinate(self):
        """
        :return: the y coordinate of the cell.
        :rtype: (int)
        :UC: none
        
        :Examples:
        >>> cell = Cell(0, 1)
        >>> cell.get_Y_coordinate()
        1
        """
        return self.__y
    
    def get_coordinates(self):
        """
        Get the X and Y coordinates of a cell.
        :return: (tuple) The (x, y) coordinates of a cell.
        
        :Examples:
        >>> cell = Cell(0, 0)
        >>> cell.get_coordinates()
        (0, 0)
        """
        return (self.get_X_coordinate(), self.get_Y_coordinate())
        
    def has_right_wall(self):
        """
        :return: the right wall of the cell, if the wall exist we return True, False otherwise
        :rtype: (bool)
        :UC: none

        :Examples:
        >>> cell1 = Cell(0, 0)
        >>> cell1.has_right_wall()
        True
        >>> cell2 = Cell(0, 1)
        >>> cell1.destroy_a_wall(cell2, "right")
        >>> cell2.has_left_wall()
        False
        """
        return self.__walls["right"]
        
    def has_left_wall(self):
        """
        :return: the left wall of the cell, if the wall exist we return True, False otherwise
        :rtype: (bool)
        :UC: none
        
        :Examples:
        >>> cell1 = Cell(0, 0)
        >>> cell1.has_left_wall()
        True
        >>> cell2 = Cell(0, 1)
        >>> cell1.destroy_a_wall(cell2, "right")
        >>> cell2.has_left_wall()
        False
        """
        return self.__walls["left"]
        
    def has_top_wall(self):
        """
        :return: the wall at the top of the cell, if the wall exist we return True, False otherwise
        :rtype: (bool)
        :UC: none
        
        :Examples:
        >>> cel = Cell(0,0)
        >>> cel.has_top_wall()
        True
        >>> cell = Cell(0,1)
        >>> cel.destroy_a_wall(cell,"bottom")
        >>> cell.has_top_wall()
        False
        """
        return self.__walls["top"]
        
    def has_bottom_wall(self):
        """
        :return: the wall at the bottom of the cell, if the wall exist we return True, False otherwise
        :rtype: (bool)
        :UC: none
        
        :Examples:
        >>> cel = Cell(0,0)
        >>> cel.has_bottom_wall()
        True
        >>> cell = Cell(0,1)
        >>> cel.destroy_a_wall(cell,"top")
        >>> cell.has_bottom_wall()
        False
        
        """
        return self.__walls["bottom"]
    
    def get_all_walls(self):
        """
        :return:  All the wall of the cell.
        :rtype: (dict)
        :UC: none
        
        :Examples:
        >>> cel = Cell(0,0)
        >>> cel.get_all_walls()
        {'top': True, 'bottom': True, 'left': True, 'right': True}
        >>> cell = Cell(0,1)
        >>> cel.destroy_a_wall(cell,"top")
        >>> cel.get_all_walls()
        {'top': False, 'bottom': True, 'left': True, 'right': True}
        """
        return self.__walls
        
    def __repr__(self):
        """
        :return: a representation of self cell,
                 a cell is a tuple of coordinate x and y
        :rtype: (tuple)
        :UC: none
        
        :Examples:
        >>> cell = Cell(0,0)
        >>> cell.__repr__()
        '(0, 0)'        
        """
        return str((self.get_X_coordinate(), self.get_Y_coordinate()))
    
    def __str__(self):
        """
        :Examples:
        >>> cell = Cell(0,0)
        >>> cell.__repr__()
        '(0, 0)' 
        """
        return str((self.get_X_coordinate(), self.get_Y_coordinate()))
          
if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS, verbose=True)