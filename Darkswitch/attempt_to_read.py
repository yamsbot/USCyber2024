#!/usr/bin/env python3

'''
either my memory dump is bad, this script is bad, or the flag is just nearly impossible to make out...
i actually didnt solve this because i cant read the fucking flag

long story short the binary has a bunch of anti debug protections that it checks before executing
but once the program is running you can do whatever you want. the process clones itself and the parent 
traces the child. a little game pops up where you can move around and toggle areas la la la anyways the child will send
1 of 3 signals to the parent, the parent will then check the "win" condition to see if its been satisfied. this is where we get 
the memory dump from. its a (i think) 10x224 grid, if we take every 4 bytes and check if the first byte is 01 or 00 we can set
the grid accordingly. based on that we get the monstrosity you see in the output.. my best guess was:

    FFCTF{1lghT_tH3_pl4N3t_l63e9y87}

to your eyes, this could be completely off and i would not be suprised i am looking at this "flag" after being up for over 24 hours
trying to make any sense of it. really wish i couldve gotten the points for this but its no big deal.

Really if those extra 8 bytes werent appended to the flag i probably wouldve gotten this. there are a few in that last
block that are just completely fucked and i really dont know if its me or just how the flag was created
'''

def main():
    # rows and columns from dumped child process (see image)
    ROWS = 10
    COLS = 224

    with open('memory_dump', 'rb') as f:
        data = f.read()

    grid = [[' ' for _ in range(COLS)] for _ in range(ROWS)]

    index = 0
    for row in range(ROWS):
        for col in range(COLS):
            value = data[index]
            if value == 1:
                grid[row][col] = "$"   #'█'
            else:
                grid[row][col] = ' '
            index += 4

    for row in grid:
        print(''.join(row))

if __name__ == '__main__':
    main()
