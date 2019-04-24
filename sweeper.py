#!/usr/bin/env python3

import sys
from random import randint

size = 20 # square size
minecount = 20
remaining = minecount

# try to avoid stack overflow
sys.setrecursionlimit(size * size * 10)

opaque = "."
bomb = "X"
clear = ''
mark = 'B'

# we have 2 grids, one for the placement of the mines,
# the other for the display of what has been uncovered
mines = [[clear for x in range(size)] for y in range (size)]
revealed = [[opaque for x in range(size)] for y in range (size)]

def is_a_bomb(x, y):
    try:
        # negatives work from end, so not throwing exception
        if (x < 0) or (y < 0):
            return 0
        return 1 if (mines[y][x] == bomb) else 0
    except:
        return 0

def nearby(x, y):
    # skip if the square is a bomb itself
    if (is_a_bomb(x, y) == 1):
        return 0 

    count = 0
    # clockwise evaluation
    count += is_a_bomb(x,   y-1) # top
    count += is_a_bomb(x+1, y-1) # top-right
    count += is_a_bomb(x+1, y)   # right
    count += is_a_bomb(x+1, y+1) # bottom-right
    count += is_a_bomb(x,   y+1) # bottom
    count += is_a_bomb(x-1, y+1) # bottom-left
    count += is_a_bomb(x-1, y)   # left
    count += is_a_bomb(x-1, y-1) # top-left
    return count

# populate with bombs
def populate():
    todo = minecount
    while todo > 0:
        row = randint(0, size-1)
        col = randint(0, size-1)
        if mines[row][col] != bomb:
            mines[row][col] = bomb
            todo -= 1
    # add 'nearby' counts
    for y in range(size):
        for x in range(size):
            count = nearby(x, y)
            if (count > 0):
                mines[y][x] = count

def print_grid(matrix):
    # print column heading
    print("   ", end='')
    for x in range(len(matrix)):
        print(" {:>2}".format(x+1), end='')
    print("")
    # print matrix
    for line, row in enumerate(matrix):
        print(" {:>2}".format(line+1), end='')
        for col in row:
            print("{:>3s}".format(str(col)), end='')
        print("")
        

def kablooey(x, y):
    print(" BOOM! {},{} has a mine".format(x+1, y+1))
    print_grid(mines)

def outside(x, y):
    return ((x < 0) or (y < 0) or (x >= size) or (y >= size))

def clear_tiles(x, y):
    # boundary check
    if outside(x, y):
        return 

    # already cleared?
    if revealed[y][x] == clear:
        return 

    tile = mines[y][x]
    try:
        if (tile == clear):
            revealed[y][x] = tile
        elif (int(tile) > 0):
            revealed[y][x] = tile
            return
    except:
        pass

    try:
        clear_tiles(x-1, y) # left
        clear_tiles(x+1, y) # right
        clear_tiles(x, y-1) # up
        clear_tiles(x, y+1) # down
        return
    except:
        print("Unexpected error:", sys.exc_info()[0])


def guess():
    while True:
        print()
        s = input("({}) [b] row col (q to quit): ".format(remaining))
        if len(s) == 0:
            print_grid(revealed)
            continue
        if s == 'q':
            print()
            sys.exit(0)
        # cheat mode
        if s == 'x':
            print_grid(mines)
            continue
        defuse = False
        try:
            if s[0] in ('b', 'B'):
                defuse = True
                s = s[1:].strip()
            row, col = s.split(" ")
            x = int(col)
            y = int(row)
            if (x < 1) or (x > size):
                print("col: {} -- out of range (1 - {})".format(col, size))
                continue
            if (y < 1) or (y > size):
                print("row: {} -- out of range (1 - {})".format(row, size))
                continue
            return defuse, x-1, y-1
        except:
            print("invalid input:", s)

def confirm():
    for y in range(size):
        for x in range(size):
            if (revealed[y][x] == mark) and mines[y][x] != bomb:
                return "There is not a bomb at {},{}".format(x+1, y+1)
    return "Congratulations! You swept the mines!"

populate()
while remaining > 0:
   print_grid(revealed)
   defuse, row, col = guess()
   if defuse:
        remaining -= 1
        revealed[row][col] = mark
        continue
   if mines[row][col] == bomb:
       kablooey(col, row)
       sys.exit(1)
   clear_tiles(col, row)

print(confirm())

