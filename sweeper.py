#!/usr/bin/env python3

import sys
from random import randint

size = 20 # square size
minecount = 25
sys.setrecursionlimit(size * size * 10)
#row = randint(0, size)
#col = randint(0, size)

opaque = "."
bomb = "X"
clear = ''

# we have 2 grids, one for the placement of the mines,
# the other, for the display of what has been uncovered
mines = [[clear for x in range(size)] for y in range (size)]
revealed = [[opaque for x in range(size)] for y in range (size)]

#print(col + 1, row + 1)
#revealed[row][col] = bomb

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
    print_grid(mines)
    print()
    # add 'nearby' counts
    for y in range(size-1):
        for x in range(size-1):
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
        print("outside: {},{}".format(x,y))
        return 

    print("clear {},{}: {}".format(x,y, revealed[y][x]))
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
        print("TILE:", tile)
    except:
        print("WTF error:", sys.exc_info()[0])
        pass

    fail = False
    try:
        clear_tiles(x-1, y) # left
        clear_tiles(x+1, y) # right
        clear_tiles(x, y-1) # up
        clear_tiles(x, y+1) # down
        return
    except SystemExit:
        print('fuk it')
        raise SystemExit
    except:
        print("Unexpected error:", sys.exc_info()[0])


def guess():
    while True:
        print()
        s = input("guess row, col (q to quit): ")
        if s == 'q':
            print()
            sys.exit(0)
        # cheat mode
        if s == 'x':
            print_grid(mines)
            continue
        row, col = s.split(",")
        try:
            x = int(col)
            y = int(row)
            if (x < 1) or (x > size):
                print("col: {} -- out of range (1 - {})".format(col, size))
                continue
            if (y < 1) or (y > size):
                print("row: {} -- out of range (1 - {})".format(row, size))
                continue
            return x-1, y-1
        except:
            print("invalid input:", s)

# main loop
populate()
remaining = minecount
print_grid(mines)
while remaining > 0:
   row, col = guess()
   if mines[row][col] == bomb:
       kablooey(col, row)
       sys.exit(1)
   clear_tiles(col, row)
   print_grid(revealed)
       


