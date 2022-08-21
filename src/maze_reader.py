from maze import Maze
from tkinter import filedialog as fd

from constants import STARTING_SYMBOL, FINISHED_SYMBOL

def __clean_lines(lines:list[str]):
    cleaned_list = [line.strip(" \n") for line in lines]
    return [line for line in cleaned_list if line] 


def __parse(lines):
    from collections import namedtuple
    assert(int(lines[0]))
    assert(int(lines[1]))
    
    width = int(lines[0])
    height = int(lines[1])
    grid:list = lines[2:]

    expected_width, expected_height = width*2+1, height*2+1
    is_same_length = [len(line) == (expected_width) for line in grid]
    
    if not all(is_same_length):
        raise ParseException("The grid lines don't have the expected(%s) width." %(width)) 
    
    if len(grid) != expected_height:
        raise ParseException("The grid don't have the expected(%s) height." %(height)) 
           
    for i in range(len(grid)):
        if (i%2) == 0:
            if ("+" or "-") not in grid[i]:
                raise ParseException("Unrecognized character in : " + grid[i])
        else:
            if ("|" or " ") not in grid[i]:
                raise ParseException("Unrecognized character in : " + grid[i])
    
    Maze = namedtuple("Maze", "width height grid")
    return Maze(width, height, grid)

    
def read_maze_from_file():
    """
    A function that will read a file and that returns the labyrinth of the type Labyrinth.
    """
    selected_file = fd.askopenfilename(title="Open a file",
                                       filetypes=(('text files', '*.txt'),))
    if not selected_file:
        raise FileNotFoundError("No file is selected.")

    with open(selected_file, "r") as file:
        lines = __clean_lines(file.readlines())
        parsed = __parse(lines)
        maze = Maze(parsed.width, parsed.height) 
        
        maze.get_starting_cell().unset_starting_cell()
        maze.get_goal_cell().unset_goal_cell()
        
        x, y = 0, 0
        for l in range(len(parsed.grid)):
            if l % 2:
                line_length = len(parsed.grid[0])
                for i in range(line_length):
                    if (i % 2) == 0:
                        if (parsed.grid[l][i] == ' '):            
                            cell1 = maze.get_cell_at_coordinates(x, y)
                            cell2 = maze.get_cell_at_coordinates(x+1, y)
                            cell1.destroy_a_wall(cell2, "right")
                            if(parsed.grid[l+1][i-1] == ' '):
                                cell3 = maze.get_cell_at_coordinates(x, y+1)
                                cell1.destroy_a_wall(cell3, "bottom")
                            x += 1    
                        elif (parsed.grid[l][i] == '|') and i > 0:
                            cell1 = maze.get_cell_at_coordinates(x, y)
                            if(parsed.grid[l+1][i-1] == ' '):
                                cell3 = maze.get_cell_at_coordinates(x, y+1)
                                cell1.destroy_a_wall(cell3, "bottom") 
                            x += 1  
                    else:
                        if parsed.grid[l][i] == STARTING_SYMBOL:
                            start_cell = maze.get_cell_at_coordinates(x, y)
                            maze.set_starting_cell(start_cell)
                        elif parsed.grid[l][i] == FINISHED_SYMBOL:
                            goal_cell = maze.get_cell_at_coordinates(x, y)
                            maze.set_goal_cell(goal_cell)    
                y += 1
                x = 0
    return maze     

class ParseException(Exception):
    pass