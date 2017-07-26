
# start_time = time.time()
#
# end_time = time.time()
#
# print(end_time - start_time)
#
# SCREEN_WIDTH = Tk().winfo_screenwidth()
# SCREEN_HEIGHT = Tk().winfo_screenheight()
#
# root = Tk()
# root.geometry('360x480+460+180')
#
# lbl = Label(root, text='Hello Fam.')
# lbl.pack()
#
# canvas = Canvas(root)
# canvas.pack()
#
# def test():
#     lbl['text'] = 'Goodbye!'
#
# btn = Button(root, text='Byebye', command=test)
# btn.pack()

# def update_player_pos(ppx,ppy,direction):
#     player_color = '#000000' #black
#
#     if direction == 'w': # up
#         ppy = ppy + 1
#     elif direction == 'a': # left
#         ppx = ppx - 1
#     elif direction == 's': # down
#         ppy = ppy - 1
#     elif direction == 'd': # right
#         ppx = ppx + 1
#     canvas.create_rectangle(ppx,ppy,ppx+TERRAIN_WIDTH,ppy+GAME_HEIGHT,fill=player_color)
#
#     return (ppx,ppy)


# IDEAr: have the terrain move randomly either up down left or right for a period of time


# generate "terrain" continuously
    # terrain gets more frequent as game goes on and game gets faster
# show person on the board and allow them to move side to side / shoot
# destroy "terrain" if the person hits it
# end game if the person gets hit by "terrain"


# Generate terrain
    # ten pixels: good size
    # it'd be cool to autoset the screen to come up in an aesthetically pleasing location (center-ish), but I might not be able to do so

from Tkinter import *

import time
import math
import random


TERRAIN_SPEED = 5
TERRAIN_DIFFICULTY = 10
TERRAIN_WIDTH = 10
TERRAIN_HEIGHT = 10

SHOOTING_SPEED = 10
PLAYER_SPEED = 5

GAME_WIDTH = 360
GAME_HEIGHT = 480
UPPER_CORNER_X = 460
UPPER_CORNER_Y = 180


root = Tk()
root.geometry('{}x{}+{}+{}'.format(GAME_WIDTH+10, GAME_HEIGHT+10, UPPER_CORNER_X, UPPER_CORNER_Y))

def zeros(n):
    return ([0]*n)

def starting_board():
    board = []
    row_terrain = []

    for row in xrange(0, GAME_WIDTH/TERRAIN_WIDTH):
        row_terrain = zeros(int(GAME_HEIGHT/TERRAIN_HEIGHT))

        for index in xrange(0, GAME_HEIGHT/TERRAIN_HEIGHT):
            block_probability = 2*math.log(TERRAIN_DIFFICULTY*0.2+1)/GAME_WIDTH*100

            if random.uniform(0,100) <= block_probability:
                row_terrain[index] = 1

        board.append(row_terrain)

    return board


def update_board(board):
    new_row_terrain = []
    board = board[:-1] # drops the last row

    for index in xrange(0,GAME_WIDTH/TERRAIN_WIDTH):
        block_probability = math.log(TERRAIN_DIFFICULTY*0.1+1)/(GAME_WIDTH*10)*100

        if random.uniform(0,100) <= block_probability:
            row_terrain[index] = 1

    board.append(row_terrain)
    return board

canvas = Canvas(root)
canvas.pack()
canvas.config(height=1000,width=1000)

# rect = canvas.create_rectangle(10,10,20,20,fill='#000000')

def show_board(board):

    board_squares = []
    sqr_coords = []

    for row in xrange(0,len(board)):
        for index in xrange(0,len(board[row])):
            if board[row][index] == 1:
                x_left, y_top, x_right, y_bottom = row*TERRAIN_WIDTH+5, index*TERRAIN_HEIGHT+5, (row+1)*TERRAIN_WIDTH+5, (index+1)*TERRAIN_HEIGHT+5

                board_squares.append(canvas.create_rectangle(x_left, y_top, x_right, y_bottom, fill='#000fff000'))

                sqr_coords.append((x_left, y_top, x_right, y_bottom))

    return (board_squares, sqr_coords)


def main():
    board = starting_board()
    (board_squares, sqr_coords) = show_board(board)
    shots = []
    shots_coords = []
    (ppx,ppy) = (15, GAME_HEIGHT - 15)
    player = canvas.create_rectangle(ppx,ppy,ppx+TERRAIN_WIDTH,ppy+TERRAIN_HEIGHT,fill='#000000')   # initializes player



    def move_terrain():

        for i in xrange(0, len(board_squares)):
            (x_left, y_top, x_right, y_bottom) = sqr_coords[i]
            canvas.coords(board_squares[i], x_left, y_top+TERRAIN_SPEED, x_right, y_bottom+TERRAIN_SPEED)

            sqr_coords[i] = x_left, y_top+TERRAIN_SPEED, x_right, y_bottom+TERRAIN_SPEED

        for j in xrange(0, len(shots)):
            (xleft, ytop, xright, ybottom) = shots_coords[j]
            canvas.coords(shots[j], xleft, ytop-SHOOTING_SPEED, xright, ybottom-SHOOTING_SPEED)

            shots_coords[j] = xleft, ytop-SHOOTING_SPEED, xright, ybottom-SHOOTING_SPEED

        root.after(2000/TERRAIN_SPEED, move_terrain)


    def key(event):
        direction = event.char

        ppx, ppy, _, _ = canvas.coords(player)

        x = ppx
        y = ppy

        # if ppy > 360 and ppy < 480 and ppx > 5 and ppx < 355:  #when player speed changes, this could potentially be a problem

        if direction == 'a':
            if ppx > 10 - PLAYER_SPEED:
                x = ppx - 1*PLAYER_SPEED

        elif direction == 'd':
            if ppx < 360 - PLAYER_SPEED:
                x = ppx + 1*PLAYER_SPEED

        elif direction == 'w':
            if ppy > 420 - PLAYER_SPEED:
                y = ppy - 1*PLAYER_SPEED

        elif direction == 's':
            if ppy < 465 + PLAYER_SPEED:
                y = ppy + 1*PLAYER_SPEED

        canvas.coords(player, x, y, x + TERRAIN_WIDTH, y + TERRAIN_HEIGHT)

        if direction == 'j':
            xleft, ytop, xright, ybottom = ppx + TERRAIN_WIDTH/2, ppy - TERRAIN_HEIGHT/2, ppx + TERRAIN_WIDTH/2 + 2, ppy - TERRAIN_HEIGHT/2 + 2
            shots.append(canvas.create_rectangle(xleft, ytop, xright, ybottom, fill = 'red'))
            shots_coords.append((xleft, ytop, xright, ybottom))


    root.after(2000/TERRAIN_SPEED, move_terrain)
    root.bind("<Key>", key)
    root.mainloop()


main()
raw_input()
