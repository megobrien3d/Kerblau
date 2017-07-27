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


def delete_index(list, index):
    return list[0:index] + list[index+1::]

def square_center(xleft,ytop,xright,ybottom):
    return ((xleft+xright)/2, (ytop+ybottom)/2)


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

            new_xleft, new_ytop, new_xright, new_ybottom = xleft, ytop-SHOOTING_SPEED, xright, ybottom-SHOOTING_SPEED

            canvas.coords(shots[j], new_xleft, new_ytop, new_xright, new_ybottom)

            shots_coords[j] = new_xleft, new_ytop, new_xright, new_ybottom

            for i in xrange(0, len(board_squares)):

                (x_left, y_bottom, x_right, y_top) = sqr_coords[i]
                (shotx, shoty) = square_center(new_xleft, new_ytop, new_xright, new_ybottom)

                if (shotx >= x_left and shotx <= x_right and shoty >= y_bottom and shoty <= y_top):

                    kxleft, kytop, kxright, kybottom = min(new_xleft, x_left), max(new_ytop, y_top), max(new_xright, x_right), min(new_ybottom, y_bottom)      # kerblau coordinates

                    kerblau = canvas.create_rectangle(kxleft, kytop, kxright, kybottom, fill = 'orange')

                    canvas.delete(shots[j])
                    shots_coords = delete_index(shots_coords, j)
                    canvas.delete(board_squares[i])
                    sqr_coords = delete_index(sqr_coords, i)

                    canvas.delete(kerblau)


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
