#!/usr/bin/python3
# -*- coding: utf-8 -*-

from tkinter import *

CAN_WIDTH = 800
CAN_HEIGHT = 600
BG_COLOR = 'black'
GRID_COLOR = 'yellow'

def draw_circle(canvas, event):
    ray = 5
    x, y = event.x, event.y
    canvas.create_oval(x - ray, y - ray,
                       x + ray, y + ray,
                       fill = 'red')
    canvas.update()
    
def draw_grid(canvas, width, height):
    DX = CAN_WIDTH // width
    DY = CAN_HEIGHT // height
    for y in range(height):
        for x in range(width):
            canvas.create_line(x * DX, y * DY,
                               (x + 1) * DX, y * DY,
                               fill=GRID_COLOR, width=1)
            canvas.create_line(x * DX, y * DY,
                               x * DX, (y + 1) * DY,
                               fill=GRID_COLOR, width=1)
    canvas.create_line(0, height * DY - 1,  width * DX - 1, height * DY - 1,
                       fill=GRID_COLOR, width=1)
    canvas.create_line(width * DX - 1, 0,  width * DX - 1, height * DY - 1,
                       fill=GRID_COLOR, width=1)
    
def main():
    win = Tk()
    win.title('Titre de la fenêtre')
    can = Canvas(win, bg=BG_COLOR, width=CAN_WIDTH, height=CAN_HEIGHT)
    can.bind('<Button-1>',
             lambda event: draw_circle(can,
                                       event))
    can.pack()
    draw_grid(can, 40, 30)
    win.mainloop()
    
if __name__ == '__main__':
    main()