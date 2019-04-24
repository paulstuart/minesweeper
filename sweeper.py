#!/usr/bin/env python3

import sys
from random import randint

size      = 20 # square size
minecount = 20
remaining = minecount

# try to avoid stack overflow
sys.setrecursionlimit(size * size * 10)

# grid markers
clear  = ''
opaque = "."
bomb   = "X"
mark   = 'B'

# we have 2 grids, one for the placement of the mines,
# the other for the display of what has been uncovered
mines    = [[clear  for x in range(size)] for y in range (size)]
revealed = [[opaque for x in range(size)] for y in range (size)]

def is_a_bomb(x, y):
    boom = ((0 < x < size) and (0 < y < size) and (mines[y][x] == bomb))
    return 1 if boom else 0

def nearby(x, y):
    # skip if the square is a bomb itself
    if (is_a_bomb(x, y) == 1):
        return 0 

    # clockwise evaluation makes it clear all neighbors are checked

    count = 0
    count += is_a_bomb(x,   y-1) # top
    count += is_a_bomb(x+1, y-1) # top-right
    count += is_a_bomb(x+1, y)   # right
    count += is_a_bomb(x+1, y+1) # bottom-right
    count += is_a_bomb(x,   y+1) # bottom
    count += is_a_bomb(x-1, y+1) # bottom-left
    count += is_a_bomb(x-1, y)   # left
    count += is_a_bomb(x-1, y-1) # top-left
    return count

def populate():
    # populate with bombs
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
        s = s.strip()
        print ("GUEES '{}'".format(s))
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
            row, col = s.split()
            x = int(col)
            y = int(row)
            # internally 0 based offset, but 1 based for user interaction
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

def game():
    global remaining
    populate()
    while remaining > 0:
        print_grid(revealed)
        defuse, row, col = guess()
        if defuse:
            remaining -= 1
            revealed[row][col] = mark
            continue

        if mines[row][col] == bomb:
            print(" BOOM! {},{} has a mine".format(col+1, row+1))
            print_grid(mines)
            sys.exit(1)

        # clearing a marked bomb?
        if revealed[row][col] == mark:
            remaining += 1

        clear_tiles(col, row)

    # game complete, show results
    print(confirm())

game()
