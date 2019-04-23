#!/usr/bin/env python3

import sys
from random import randint

size = 20 # square size
minecount = 25

#row = randint(0, size)
#col = randint(0, size)

opaque = "."
bomb = "X"

# we have 2 grids, one for the placement of the mines,
# the other, for the display of what has been uncovered
mines = [['' for x in range(size)] for y in range (size)]
revealed = [[opaque for x in range(size)] for y in range (size)]

#print(col + 1, row + 1)
#revealed[row][col] = bomb

# populate with bombs
def populate():
    todo = minecount
    while todo > 0:
        row = randint(0, size-1)
        col = randint(0, size-1)
        if mines[row][col] != bomb:
            mines[row][col] = bomb
            todo -= 1
        
    
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
            print("{:>3s}".format(col), end='')
        print("")
        

def kablooey(x, y):
    print(" BOOM! {},{} has a mine".format(x+1, y+1))
    print_grid(mines)
    sys.exit(1)

def guess():
    while True:
        print()
        s = input("guess row, col (q to quit): ")
        if s == 'q':
            sys.exit(0)
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
   print_grid(revealed)
       


