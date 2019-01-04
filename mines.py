#!/usr/bin/python
import random
import re

"""

The minefield is represented by a 2D array as follows

Matrix init
* = uncovered space
B = uncovered mine

Open action
' '  = cleared space
1..8 = there are surrounding mines

Mark action
M = marked mine
I = incorrectly marked mine
X = detonated mine

The minefield is initially generated with just uncovered spaces and bombs,
as the user traverses the field they are marked, pending user input

"""

# We create a 2D array minefield, the size of the array is passed in
# as well as the difficulty, which determines how many bombs will be 
# placed in the array. The bombs are randomly generated. Bombs are 
# stored as 'B' chars, blanks are stored as '*" chars.
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
    return mine_matrix

# The mine field is printed here, dependant on the reveal flag. If the reveal
# flag is enabled the matrix is revealed to the user, if not, only actioned
# items are revealed as well as unactioned spaces.
# This function also determines if the matrix is solved.
def printField(mine_matrix, field_width, field_height, reveal):
    print
    solved = True
    spacer = 7
    
    # Traverse the matrix and print rows whilst checking conditions
    for i in range(field_height):
        if i == (field_height/2):
            print 'y %3s |' % (field_height -i -1),
        else:
            print '%5s |' % (field_height -i -1),
        for j in range(field_width):
            if reveal:
                print '%2s' % (mine_matrix[i][j]),
            elif mine_matrix[i][j] == 'I':
                print '%2s' % "M",
            elif mine_matrix[i][j] in [' ','M'] + range(1,8):
                print '%2s' % (mine_matrix[i][j]),
            else:
                print '%2s' % "*",

                # If any stars are printed, then matrix is unsolved
                solved = False
        print
    print ' '*spacer,

    # Print bottom row of matrix display
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

    return solved

# This is X, > 100 will break display
field_width = 5 

# This is Y
field_height = 7

# Number of bombs, difficulty > field_width * field_height will break
difficulty = 10

# Create minefield
mine_matrix = createField(field_width, field_height, difficulty)

turns_used = 0
marked_counter = 0

#Loop for user input
while True:
    
    # Check and see if the matrix is solved whilst printing it
    if printField(mine_matrix, field_width, field_height, False):
        print "you win!\n"
        break
    
    print ('Number of bombs in matrix: {}\nBombs marked: {}\nTurns used: {}\n'
          .format(difficulty, marked_counter, turns_used))
    print ('Enter x, y coordinate you wish to mark or open\n'
          'Example o4, 1 to open 4, 1 or m3, 2 to mark 3, 2')
    input_value = raw_input("Which coordinate (quit to end)? :  ")
    if input_value in ('quit','q'):
        break

    # See if user input follows the correct formula using regex.
    # Must start with either o or m followed by a coordinate, a comma,
    # null or more whitespace and another coordinate.
    # Three groups are captured as user input, 1 is action, 2 is x coordinate,
    # and 3 is y coodinate.
    
    args = re.search ("^([om]{1})(\d+),\s*(\d+)$", input_value)

    # Ensure input is in bounds
    if not args:
        print '\n***invalid input***\n'
        
        #Go to next iteration of while loop, is this bad programming?
        continue
    else:
        action = args.group(1)
        x = int (args.group(2)) 
        y = field_height - int (args.group(3)) - 1
    
    # Check to see if this coordinate can be actionable
    if int (args.group(2)) > field_width -1:
        print '\nx coordinate cannot exceed {}'.format(field_width -1)
    elif int (args.group(3)) > field_height -1:
        print '\ny coordinate cannot exceed {}'.format(field_height -1)
    elif mine_matrix[y][x] in [' ','M','I'] + range(1,8):
        print '\nYou\'ve already taken action on this coordinate'

    # Execute valid user action
    else:
        turns_used += 1

        if marked_counter > difficulty:
            print "You ran out of turns!"
            printField(mine_matrix, field_width, field_height, True)

        # Case marking a bomb incorrectly
        if not mine_matrix[y][x] == "B" and action == "m":
            mine_matrix[y][x] = "I"
            marked_counter += 1
        
        # Case marking a bomb correctly
        elif mine_matrix[y][x] == "B" and action == "m":
            mine_matrix[y][x] = "M"
            marked_counter += 1
   
        # Case opening a bomb   
        elif mine_matrix[y][x] == "B" and action == "o":
            print "\nYou set off a bomb!"
            mine_matrix[y][x] = "X"
            printField(mine_matrix, field_width, field_height, True)
            break

        # Case opening an empty space
        else:
            bomb_counter = 0

            for i in [-1, 0, 1]:
                for j in [-1, 0, 1]:

                    #Ask for forgiveness and check our surroundings
                    if not i == j == 0:
                        try:
                            if mine_matrix[y-i][x-j] == "B":
                                bomb_counter += 1
                        except IndexError:
                                pass

            # Replace empty space '*' with either a bomb counter or blank                
            if bomb_counter == 0:
                mine_matrix[y][x] = " "
            else:
                mine_matrix[y][x] = bomb_counter
