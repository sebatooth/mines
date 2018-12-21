#!/usr/bin/python
import random
import re

"""

The minefield is represented by a 2D array as follows

Mine Field Legend

Matrix init
* = uncovered space
B = uncovered mine

Open action
' '  = cleared space
1..8 = there are surrounding mines

Mark action
M = marked mine
I = Incorrectly marked mine
X = Detonated mine

The minefield is initially generated with just uncovered spaces and bombs,
as the user traverses the field they are marked, pending user input

"""
def createField(field_width, field_height, difficulty):
    mine_matrix = []
    bomb_counter = 0
    bombs = random.sample(range(0, field_width * field_height,), difficulty)
    for i in range(field_height):
        mine_row = []
        for j in range(field_width):
            if bomb_counter in bombs:
                mine_row.append("B")
            else:
                mine_row.append("*")
            bomb_counter += 1
        mine_matrix.append(mine_row)
    # append number of bomb count, counter for turns used and bombs marked
    #mine_matrix.append([difficulty,0,0,'s',0,0])
    return mine_matrix

def printField(mine_matrix, field_width, field_height, reveal):
    print
    #print "Beware the mine field\n"
    spacer = 7
    for i in range(field_height):
        if i == (field_height/2):
            print 'y %3s |' % (field_height -i -1),
        else:
            print '%5s |' % (field_height -i -1),
        for j in range(field_width):
            if reveal:
                print '%2s' % (mine_matrix[i][j]),
            elif mine_matrix[i][j] in [' ','M'] + range(1,8):
                print '%2s' % (mine_matrix[i][j]),
            else:
                print '%2s' % "*",
        print
    print ' '*spacer,
    for i in range(field_width):
        if i < 10:
            print ' _',
        else:
            print '__',
    print
    print ' '*spacer,
    for i in range(field_width):
        print '%2s' % i,
    print "\n"
    print ' '*spacer+field_width/2*'   '+'x'

# This is X, > 100 will break display
field_width = 5

# This is Y
field_height = 5

# Number of bombs, difficulty > field_width * field_height will break
difficulty = 4

# Create minefield
mine_matrix = createField(field_width, field_height, difficulty)

marked_counter, turns_used = 0, 0
#Loop for user input
while True:
    printField(mine_matrix, field_width, field_height, False)
    print mine_matrix
    print ('Number of bombs in matrix: {}\nBombs marked: {}\nTurns used: {}\n'
          .format(difficulty, marked_counter, turns_used))
    print ('Enter x, y coordinate you wish to mark or open\n'
          'Example o4, 1 to open 4, 1 or m3, 2 to mark 3, 2')
    input_value = raw_input("Which coordinate (quit to end)? :  ")

    # See if user input follows the correct formula using regex.
    # Must start with either o or m followed by a coordinate, a comma,
    # null or more whitespace and another coordinate.
    # Three groups are captured as user input, 1 is action, 2 is x coordinate,
    # and 3 is y coodinate.
    
    args = re.search ("^([om]{1})(\d+),\s*(\d+)$", input_value)

    # Ensure input is in bounds
    if input_value in ('quit','q'):
        break
    elif not args:
        print '\n***invalid input***\n'
    elif int (args.group(2)) > field_width -1:
        print '\nx coordinate cannot exceed {}'.format(field_width -1)
    elif int (args.group(3)) > field_height -1:
        print '\ny coordinate cannot exceed {}'.format(field_height -1)
    else:
        turns_used += 1
        action = args.group(1)
        x = int (args.group(2)) 
        y = field_height - int (args.group(3)) - 1

        # Execute the valid user input action
        
        if marked_counter > difficulty:
            print "You ran out of turns!"
            printField(mine_matrix, field_width, field_height, True)

        # Case marking a bomb incorrectly
        if not mine_matrix[y][x] == "B" and action == "m":
            mine_matrix[y][x] = "I"
        
        # Case marking a bomb correctly
        elif mine_matrix[y][x] == "B" and action == "m":
            mine_matrix[y][x] = "M"
   
        # Case opening a bomb   
        elif mine_matrix[y][x] == "B" and action == "o":
            print "\nYou set off a bomb!"
            mine_matrix[y][x] = "X"
            printField(mine_matrix, field_width, field_height, True)
            break

        # Case opening an empty space
        else:
            bomb_counter = 0

            #Ask for forgiveness and check our surroundings
            #for i in [-1, 0, 1, -field_width, field_width]:
                #for j in [-1, 0, 1, -field_height, field_height]:
            try:
                if mine_matrix[y-1][x] == "B":
                    bomb_counter += 1
            except IndexError:
                pass
            try:
                if mine_matrix[y+1][x] == "B":
                    bomb_counter += 1
            except IndexError:
                pass
            try:
                if mine_matrix[y][x+1] == "B":
                    bomb_counter += 1
            except IndexError:
                pass
            try:
                if mine_matrix[y][x-1] == "B":
                    bomb_counter += 1
            except IndexError:
                pass
            try:
                if mine_matrix[y-1][x-1] == "B":
                    bomb_counter += 1
            except IndexError:
                pass
            try:
                if mine_matrix[y+1][x-1] == "B":
                    bomb_counter += 1
            except IndexError:
                pass
            try:
                if mine_matrix[y+1][x+1] == "B":
                    bomb_counter += 1
            except IndexError:
                pass
            try:
                if mine_matrix[y-1][x+1] == "B":
                    bomb_counter += 1
            except IndexError:
                pass
            if bomb_counter == 0:
                mine_matrix[y][x] = " "
            else:
                mine_matrix[y][x] = bomb_counter
