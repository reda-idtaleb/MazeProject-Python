"""
AUTHOR: ID-TALEB Réda
Project-name: PyMaze
"""
import random
from types import CellType


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
       >>> cell1.destroy_a_wall(cell2, "gauche")
       >>> cell1.get_left_wall()
       False
       >>> cell2.get_right_wall()
       False
       >>> cell1.is_closed()
       False
       >>> cell2.is_closed()
       False
    """
    # Dictionnaire qui représente deux cellules séparés par un mur. c'est à dire si le mur partagé est horizontal,
    # on constuit deux murs, le premier mur situe à droite du mur séparant,
    # et le deuxième mur situe à gauche du mur séparant. Et si le mur partagé est vertical, 
    # on construit le mur qui se situe en haut du mur partagé, et un autre mur qui se situe en bas.
    cell_pairs = {"haut": "bas", "bas": "haut", "droite": "gauche", "gauche": "droite"}  
                                                                                                                                              
    def __init__(self, x, y):
        """
        :return: a cell of a labyrinthe grid.
                 coordinate of a Cell, all the wall that are builded
                 
        :rtype: Cell
        :UC: none
        :Examples:

        >>> cel = Cell(0,0)
        >>> cel.is_closed()
        True
        >>> cell = Cell(0,1)
        >>> cell.is_closed()
        True
        >>> cel.destroy_a_wall(cell,"gauche")
        >>> cel.is_closed()
        False
        
        """
        # on créé une longueur et une largueur d'un labyrinthe
        self.x = x
        self.y = y
        # un dictionnaire qui représente les 4 murs qui entoure la cellule dans un labyrinthe, 
        # la valeur "True" veut dire que les murs existent.
        self.walls = {'haut': True, 'bas': True, 'gauche': True, 'droite': True}
    
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
        >>> destroyed_cell.destroy_a_wall(cell, "gauche")
        >>> destroyed_cell.is_closed()
        False

        """
        # Si un des murs n'existe pas, donc cette cellule n'est pas fermée, donc on renvoie False.
        # Si tous les murs existent, donc la cellule est fermée, donc on renvoie True
        for i in self.walls.values():
            if i == False:
                return False
        return True
    
    def destroy_a_wall(self, neighboor_cell, wall:str):
        """
        :param cell: (Cell) The neighboor cell.
        :param wall: (str) The string to destroy.
        :return: None
        :side effect: Modify a wall status. Destroy the corresponding wall that is passed as parameter. 
                      The wall shared between two cells.
        :UC: none
        
        :Examplez:

        >>> cell1 = Cell(0,0)
        >>> cell2 = Cell(0,1)
        >>> cell1.destroy_a_wall(cell2, "gauche")
        >>> cell1.is_closed()
        False
        >>> cell1.get_all_walls()
        {'haut': True, 'bas': True, 'gauche': False, 'droite': True}
        >>> cell2.get_all_walls()
        {'haut': True, 'bas': True, 'gauche': True, 'droite': False}
        """
        # si on souhaite détruire un mur entre deux cellules, 
        # il suffit de détruire un mur de la cellule courante(self).
        # En effet, puisque la cellule partage son mur avec la cellule voisine, 
        # donc automatiquement le mur de l'autre cellule est aussi détruit.
        self.walls[wall] = False
        neighboor_cell.walls[self.cell_pairs[wall]] = False
        
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
        >>> left_cell.destroy_a_wall(right_cell, "gauche")
        >>> left_cell.get_destroyed_walls()
        ['gauche']
        """
        l = []
        if not(self.is_closed()):
            for i in self.walls.keys():
                if self.walls[i] == False:
                    l = l + [i]
        return l
    
    def get_X_coordinate(self):
        """
        :return: the x coordinate of the cell.
        :rtype: (int)
        :UC: none
        
        :Examples:
        >>> cell = Cell(0,0)
        >>> cell.get_X_coordinate()
        0
        >>> cell = Cell(1,0)
        >>> cell.get_X_coordinate()
        1
        """
        return self.x
    
    def get_Y_coordinate(self):
        """
        :return: the y coordinate of the cell.
        :rtype: (int)
        :UC: none
        
        :Examples:
        >>> cell = Cell(0,0)
        >>> cell.get_Y_coordinate()
        0
        >>> cell = Cell(0,1)
        >>> cell.get_Y_coordinate()
        1
        """
        return self.y
    
    def get_right_wall(self):
        """
        :return: the right wall of the cell, if the wall exist we return True, False otherwise
        :rtype: (bool)
        :UC: none
        
        :Examples:
        >>> cel = Cell(0,0)
        >>> cel.get_right_wall()
        True
        >>> cell = Cell(0,1)
        >>> cel.destroy_a_wall(cell,"gauche")
        >>> cell.get_right_wall()
        False
        """
        return self.walls["droite"]
        
    def get_left_wall(self):
        """
        :return: the left wall of the cell, if the wall exist we return True, False otherwise
        :rtype: (bool)
        :UC: none
        
        :Examples:
        >>> cel = Cell(0,0)
        >>> cel.get_left_wall()
        True
        >>> cell = Cell(0,1)
        >>> cel.destroy_a_wall(cell,"droite")
        >>> cell.get_left_wall()
        False
        """
        return self.walls["gauche"]
        
    def get_top_wall(self):
        """
        :return: the wall at the top of the cell, if the wall exist we return True, False otherwise
        :rtype: (bool)
        :UC: none
        
        :Examples:
        >>> cel = Cell(0,0)
        >>> cel.get_top_wall()
        True
        >>> cell = Cell(0,1)
        >>> cel.destroy_a_wall(cell,"bas")
        >>> cell.get_top_wall()
        False
        """
        return self.walls["haut"]
        
    def get_bottom_wall(self):
        """
        :return: the wall at the bottom of the cell, if the wall exist we return True, False otherwise
        :rtype: (bool)
        :UC: none
        
        :Examples:
        >>> cel = Cell(0,0)
        >>> cel.get_bottom_wall()
        True
        >>> cell = Cell(0,1)
        >>> cel.destroy_a_wall(cell,"haut")
        >>> cell.get_bottom_wall()
        False
        
        """
        return self.walls["bas"]
    
    def get_all_walls(self):
        """
        :return:  All the wall of the cell.
        :rtype: (dict)
        :UC: none
        
        :Examples:
        >>> cel = Cell(0,0)
        >>> cel.get_all_walls()
        {'haut': True, 'bas': True, 'gauche': True, 'droite': True}
        >>> cell = Cell(0,1)
        >>> cel.destroy_a_wall(cell,"haut")
        >>> cel.get_all_walls()
        {'haut': False, 'bas': True, 'gauche': True, 'droite': True}
        """
        return self.walls
 
    def __repr__(self):
        """
        :return: a representation of self cell,
                 a cell is a tuple of coordinate x and y
        :rtype: (tuple)
        :UC: none
        :Example:
        >>> cell = Cell(0,0)
        >>> cell.__repr__()
        (0, 0)
        >>> cel = Cell(1,1)
        >>> cel.__repr__()
        (1, 1)
        
        """
        return (self.get_X_coordinate(), self.get_Y_coordinate())
    
    def __str__(self):
        return str((self.get_X_coordinate(), self.get_Y_coordinate()))
          
if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS, verbose=True)