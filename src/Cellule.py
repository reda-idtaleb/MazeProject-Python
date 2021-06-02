"""
AUTHOR: OUKOUKAS Ferial, ID-TALEB Réda
Projet: Labyrinthe
"""
import random


class Cell():
    
    """
       Create a Cell in the maze.
       A cell in the maze is a point which may be surrounded by walls in all directions,
       
       >>> cel = Cell(0,0)
       >>> cell = Cell(0,1)
       >>> cel.is_closed_cell()
       True
       >>> cell.is_closed_cell()
       True
       >>> cel.get_right_wall()
       True
       >>> cel.get_left_wall()
       True
       >>> cel.get_top_wall()
       True
       >>> cel.get_bottom_wall()
       True
       >>> cel.wall_destroyed_between_2_cells(cell,"gauche")
       >>> cel.get_left_wall()
       False
       >>> cell.get_right_wall()
       False
       >>> cel.is_closed_cell()
       False
       
    """
    paire_cellule = {"haut": "bas", "bas": "haut", "droite": "gauche", "gauche": "droite"}  # dictionnaire qui représente deux cellules séparés par un mur. c'est à dire si le mur partagé est horizontal, on constuit deux murs, le premier mur situe à droite du mur séparant,
                                                                                            # et le deuxième mur situe à gauche du mur séparant. Et si le mur partagé est horizontal, on construit le mur qui se situe en haut du mur partagé, et un autre mur qui se situe en bas.
                                                                                                                                              
    def __init__(self, x, y):
        """
        :return: a cell of a labyrinthe grid.
                 coordinate of a Cell, all the wall that are builded
                 
        :rtype: Cell
        :UC: none
        :Examples:

        >>> cel = Cell(0,0)
        >>> cel.is_closed_cell()
        True
        >>> cell = Cell(0,1)
        >>> cell.is_closed_cell()
        True
        >>> cel.wall_destroyed_between_2_cells(cell,"gauche")
        >>> cel.is_closed_cell()
        False
        
        """
        # on créé une longueur et une largueur d'un labyrinthe
        self.x = x
        self.y = y
        # un dictionnaire qui représente les 4 murs qui entoure la cellule dans un labyrinthe, la valeur "True" veut dire que les murs existent.
        self.wall = {'haut': True, 'bas': True, 'gauche': True, 'droite': True}
    
    def get_coordinate_x(self):
        """
        :return: the x coordinate of the cell.
        :rtype: (int)
        :UC: none
        
        :Examples:
        >>> cel = Cell(0,0)
        >>> cel.get_coordinate_x()
        0
        >>> cell = Cell(1,0)
        >>> cell.get_coordinate_x()
        1
        """
        return self.x
    
    def get_coordinate_y(self):
        """
        :return: the y coordinate of the cell.
        :rtype: (int)
        :UC: none
        
        :Examples:
        >>> cel = Cell(0,0)
        >>> cel.get_coordinate_y()
        0
        >>> cell = Cell(0,1)
        >>> cell.get_coordinate_y()
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
        >>> cel.wall_destroyed_between_2_cells(cell,"gauche")
        >>> cell.get_right_wall()
        False
        """
        return self.wall["droite"]
        
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
        >>> cel.wall_destroyed_between_2_cells(cell,"droite")
        >>> cell.get_left_wall()
        False
        """
        return self.wall["gauche"]
        
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
        >>> cel.wall_destroyed_between_2_cells(cell,"bas")
        >>> cell.get_top_wall()
        False
        """
        return self.wall["haut"]
        
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
        >>> cel.wall_destroyed_between_2_cells(cell,"haut")
        >>> cell.get_bottom_wall()
        False
        
        """
        return self.wall["bas"]
    
    def get_all_wall(self):
        """
        :return:  All the wall of the cell.
        :rtype: (dict)
        :UC: none
        
        :Examples:
        >>> cel = Cell(0,0)
        >>> cel.get_all_wall()
        {'haut': True, 'bas': True, 'gauche': True, 'droite': True}
        >>> cell = Cell(0,1)
        >>> cel.wall_destroyed_between_2_cells(cell,"haut")
        >>> cel.get_all_wall()
        {'haut': False, 'bas': True, 'gauche': True, 'droite': True}
        """
        return self.wall
 
    def __repre__(self):
        """
        :return: a representation of self cell,
                 a cell is a tuple of coordinate x and y
        :rtype: (tuple)
        :UC: none
        :Example:
        >>> cell = Cell(0,0)
        >>> cell.__repre__()
        (0, 0)
        >>> cel = Cell(1,1)
        >>> cel.__repre__()
        (1, 1)
        
        """
        cellule = (self.get_coordinate_x(), self.get_coordinate_y())
        return cellule
    
    def is_closed_cell(self):
        """
        :return: True if all the walls of self are closed , False otherwise
        :rtype: (bool)
        :UC: none
        :Example:

        >>> cel = Cell(0,0)
        >>> cel.is_closed_cell()
        True
        >>> cell = Cell(0,1) 
        >>> cel.wall_destroyed_between_2_cells(cell, "gauche")
        >>> cel.is_closed_cell()
        False

        """
        # Si un des murs n'existe pas, donc cette cellule n'est pas fermée, donc on renvoie False.
        # Si tous les murs existent, donc la cellule est fermée, donc on renvoie True
        for i in self.wall.values():
            if i == False:
                return False
        return True
    
    def wall_destroyed_between_2_cells(self, cell, wall):
        """
        :return: None
        :side effect: modify a wall, destroy the corresponding wall that is passed in parameter. The wall shared between two cells.
        :UC: none
        :Example:

        >>> cel = Cell(0,0)
        >>> cell = Cell(0,1)
        >>> cel.wall_destroyed_between_2_cells(cell, "gauche")
        >>> cel.is_closed_cell()
        False
        >>> cel.wall
        {'haut': True, 'bas': True, 'gauche': False, 'droite': True}
        >>> cell.wall
        {'haut': True, 'bas': True, 'gauche': True, 'droite': False}
        """
        # si on souhaite détruire un mur entre deux cellules, il suffit de détruire un mur de la cellule courante(self).
        # En effet, puisque la cellule partage son mur avec la cellule voisine, du coup automatiquement le mur de l'autre cellule est aussi détruit.
        self.wall[wall] = False
        cell.wall[self.paire_cellule[wall]] = False
        
        
    def is_not_closed_cell(self):
        """
        :return: a liste of neighboor cell which the wall are destroyed
        :rtype: (list)
        :UC: none
        :Example:

        >>> cel = Cell(0,0)
        >>> cel.is_closed_cell()
        True
        >>> cell = Cell(0,1) 
        >>> cel.wall_destroyed_between_2_cells(cell, "gauche")
        >>> cel.is_not_closed_cell()
        ['gauche']

        """
        l = []
        if not(self.is_closed_cell()):
            for i in self.wall.keys():
                if self.wall[i] == False:
                    l = l + [i]
        return l
    
          

          
          
if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS, verbose=True)
    
