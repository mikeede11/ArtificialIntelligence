# -*- coding: utf-8 -*-
import sys
"""DFS_queens.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1puD0kHn_0jLIZbtEOzNW4Atp2JNHcaYB

This is the notebook version of the code. I will use this to explain the homework.  I used parts of the code from: https://www.sanfoundry.com/python-program-solve-n-queen-problem-without-recursion/

As we did in class, we will represent the board as a one-dimensional array where each position in the arrray is the n'th queen's column value. So if the array is: [1, 3, 0, 2], then the first queen is in position 1 (from 0--3), the second queen is in position 3 (the last column), the third queen is in the first column and the last queen is the in the second position.
"""
columns = [] #columns is the locations for each of the queens
# columns[r] is a number c if a queen is placed at row r and column c.
size = 4
constraints_board = [[0 for i in range(size)] for j in range(size)] #0 means not constrained otherwise the number represents how many queens are constraining that spot
queen_constraints = [0 for i in range(size)] #an array representative of the constraints held by each corresponding queen
import random #hint -- you will need this for the following code: column=random.randrange(0,size)

"""Let's setup one iteration of the British Museum algorithm-- we'll put down 4 queens randomly."""

def place_n_queens(size):
    columns.clear()
    row = 0
    while row < size:
        column=random.randrange(0,size)
        columns.append(column)
        row+=1

place_n_queens(size)

"""Now, we can print the result with a simple loop:"""

def display():
    for row in range(len(columns)):
        for column in range(size):
            if column == columns[row]:
                print('♛', end=' ')
            else:
                print(' .', end=' ')
        print()

def proximity_heuristic(queen):
    if(not next_row_is_safe(queen)):
        return sys.maxsize
    #prioritize right
    if len(columns) == 0:
        return 0
    prev_queen = columns.pop()
    columns.append(prev_queen)
    if prev_queen < queen:
        return abs(prev_queen - queen)  
    else:
        return (prev_queen - queen) * 2 

def display_constraints():
    for row in range(size):
        for column in range(size):
            print(constraints_board[row][column], end=' ')
        print()

#presupposes it has a constraints board to work with
#returns the number of additional constraints that this queen/column would generate on the rest of the board
#***
def num_constraints(queen):
    if(not next_row_is_safe(queen)):
        return sys.maxsize
    constraints = 0
    constraints += check_down(queen) #should be zero
    # print("down constraints are: ", constraints)
    constraints += check_left_diagonal(queen)
    # print("left diag constraints added on: ", constraints)
    constraints += check_right_diagonal(queen)
    # print("right diag constraints added on: ", constraints)
    return constraints

def check_down(queen):
    constraints = 0
    starting_row = len(columns) + 2
    if starting_row < size:
        for row in range(starting_row, size):
            if constraints_board[row][queen] == False:# try both overlap and new constraints - if overlap make sureto reverse the sort array
                constraints += 1
    return constraints

def check_left_diagonal(queen):
    constraints = 0
    column = queen - 1
    row = len(columns) + 2
    if row < size:
        while column > -1 and row < size:
            if constraints_board[row][column] == False:
                constraints +=1
            column -= 1
            row += 1
    return constraints

def check_right_diagonal(queen):
    constraints = 0
    column = queen + 1
    row = len(columns) + 2
    if row < size:
        while column < size and row < size:
            if constraints_board[row][column] == False:
                constraints+=1
            column += 1
            row += 1
    return constraints
#adds the constraints by the most recently inserted queen
#***
def add_constraints():
    queen = columns.pop()
    columns.append(queen)
    starting_row = len(columns) + 1
    add_down(queen, starting_row)
    add_left_diag(queen, starting_row)
    add_right_diag(queen, starting_row)

def count_complete_constraints():
    total_constraints = 0
    for row, column in enumerate(columns):
        queen_constraints[row] = constraints_board[row][column]
        total_constraints += constraints_board[row][column]
    return total_constraints

def count_constraints(queen):
    row = columns.index(queen)

def add_complete_constraints():
    for row, column in enumerate(columns):
        add_vertical_constraints(column)
        add_diag1_constraints(row, column)
        add_diag2_constraints(row, column)

def add_vertical_constraints(column):
    for row in range(len(columns)):
        constraints_board[row][column] += 1

def add_diag1_constraints(row, column):
    r = row
    c = column
    #go to corner
    while r < size - 1 and c > 0:
        r+=1
        c-=1
    while r > -1 and c < size:
        if r != row or c != column:
            constraints_board[r][c]+=1
        r -= 1
        c += 1

def add_diag2_constraints(row, column):
    r = row
    c = column
    #go to corner
    while r > 0 and c > 0:
        r-= 1
        c-= 1
    while r < size and c < size:
        if r != row or c != column:
            constraints_board[r][c]+=1
        r += 1
        c += 1

def remove_vertical_constraints(column):
    for row in range(len(columns)):
        constraints_board[row][column] -= 1

def remove_diag1_constraints(row, column):
    r = row
    c = column
    #go to corner
    while r < size - 1 and c > 0:
        r+=1
        c-=1
    while r > -1 and c < size:
        if r != row or c != column:
            constraints_board[r][c]-=1
        r -= 1
        c += 1

def remove_diag2_constraints(row, column):
    r = row
    c = column
    #go to corner
    while r > 0 and c > 0:
        r-= 1
        c-= 1
    while r < size and c < size:
        if r != row or c != column:
            constraints_board[r][c]-=1
        r += 1
        c += 1

def add_down(queen, starting_row):
    if starting_row < size:
        for row in range(starting_row, size):
            constraints_board[row][queen]+=1

def add_left_diag(queen, starting_row):
    row = starting_row
    column = queen - 1
    if row < size:
        while column > -1 and row < size:
            constraints_board[row][column]+=1
            column -= 1
            row += 1

def add_right_diag(queen, starting_row):
    row = starting_row
    column = queen + 1
    if row < size:
        while column < size and row < size:
            constraints_board[row][column]+=1
            column += 1
            row += 1

def remove_constraints(queen):
    if queen == -1:
        return
    starting_row = len(columns) + 2#BIG FIX?
    remove_down(queen,starting_row)
    remove_left_diag(queen, starting_row)
    remove_right_diag(queen, starting_row)

def remove_down(queen, starting_row):
    if starting_row < size:
        for row in range(starting_row, size):
            constraints_board[row][queen]-=1

def remove_left_diag(queen, starting_row):
    row = starting_row
    column = queen - 1
    if row < size:
        while column > -1 and row < size:
            constraints_board[row][column]-=1
            column -= 1
            row += 1

def remove_right_diag(queen, starting_row):
    row = starting_row
    column = queen + 1
    if row < size:
        while column < size and row < size:
            constraints_board[row][column]-=1
            column += 1
            row += 1

#solved = False;
#while solved == False:
place_n_queens(size)
    #is_kosher_board(size)

display()
print(columns)

"""This of course is not necessary legal, so we'll write a simple DFS search with backtracking:"""

def solve_queen(size):
    columns.clear()
    number_of_moves = 0 #where do I change this so it counts the number of Queen moves?
    number_of_iterations = 0  
    row = 0
    column = 0
    # iterate over rows of board
    while True:
        #place queen in next row
        ''''print(columns)
        print("I have ", row, " number of queens put down")
        display()
        print(number_of_moves)'''
        while column < size:
            number_of_iterations+=1

            if next_row_is_safe(column):
                place_in_next_row(column)
                row += 1
                column = 0
                break
            else:
                column += 1
        # if I could not find an open column or if board is full
        if (column == size or row == size):
            number_of_iterations+=1
            # if board is full, we have a solution
            if row == size:
                print("I did it! Here is my solution")
                display()
                #print(number_of_moves)
                return number_of_iterations, number_of_moves
            # I couldn't find a solution so I now backtrack
            prev_column = remove_in_current_row()
            if (prev_column == -1): #I backtracked past column 1
                print("There are no solutions")
                #print(number_of_moves)
                return number_of_iterations, number_of_moves
            # try previous row again
            row -= 1
            # start checking at column = (1 + value of column in previous row)
            column = 1 + prev_column


def solve_queen_with_heuristic(size):
    columns.clear()
    number_of_moves = 0 #where do I change this so it counts the number of Queen moves?
    number_of_iterations = 0  
    row = 0
    column = 0
    columns_by_preference = list(range(0, size))
    i = 0
    # iterate over rows of board
    while True:
        #place queen in next row
        # display()
        ''''print(columns)
        print("I have ", row, " number of queens put down")
        display()
        print(number_of_moves)'''
        h_array = sorted(columns_by_preference, key=num_constraints) #.sort(key=num_constraints)
        #print(h_array)
        while i < size:
            number_of_iterations+=1
            column = h_array[i]

            if num_constraints(column) != sys.maxsize:#this if may be redundant
                # print("putting queen down")
                place_in_next_row(column)
                add_constraints()
                # display_constraints()
                h_array = sorted(columns_by_preference, key=num_constraints)
                row += 1
                i = 0
                break
            else:
                #print("no good spot, lets try to go back...")
                i = size # end it it must be no good the code below will update to try the index that we need
        # if I could not find an open column or if board is full
        if (i == size or row == size):
            # print("ok either we solved it or this was a bad layout...go back...")
            number_of_iterations+=1
            # if board is full, we have a solution
            if row == size:#b/c row is only incrememnted when we can legally put down a piece - if we get to the last row we must have put down all pieces legally
                print("I did it! Here is my solution")
                display()
                #print(number_of_moves)
                return number_of_iterations, number_of_moves
            # I couldn't find a solution so I now backtrack
            prev_column = remove_in_current_row()
            remove_constraints(prev_column)
            # display_constraints()
            # print("removed queen and constraints")
            if (prev_column == -1): #I backtracked past column 1
                print("There are no solutions")
                #print(number_of_moves)
                return number_of_iterations, number_of_moves
            # try previous row again
            row -= 1
            # start checking at column = (1 + value of column in previous row)
            h_array = sorted(columns_by_preference, key=num_constraints)
            i = h_array.index(prev_column) + 1
            # print(h_array)
            # print(num_constraints(h_array[0]))
            # print(num_constraints(h_array[1]))
            # print("next index attempt will be ", i)
            #column = 1 + prev_column#get the index of the value of prev_column in the h_array that represents the previous row

def solve_queen_with_proximity_heuristic(size):

    columns.clear()
    number_of_moves = 0 #where do I change this so it counts the number of Queen moves?
    number_of_iterations = 0  
    row = 0
    column = 0
    columns_by_preference = list(range(0, size))
    i = 0
    # iterate over rows of board
    while True:
        #place queen in next row
        # display()
        ''''print(columns)
        print("I have ", row, " number of queens put down")
        display()
        print(number_of_moves)'''
        h_array = sorted(columns_by_preference, key=proximity_heuristic) #.sort(key=num_constraints)
        #print(h_array)
        while i < size:
            number_of_iterations+=1
            column = h_array[i]

            if num_constraints(column) != sys.maxsize:#this if may be redundant
                # print("putting queen down")
                place_in_next_row(column)
                # display_constraints()
                h_array = sorted(columns_by_preference, key=proximity_heuristic)
                row += 1
                i = 0
                break
            else:
                #print("no good spot, lets try to go back...")
                i = size # end it it must be no good the code below will update to try the index that we need
        # if I could not find an open column or if board is full
        if (i == size or row == size):
            # print("ok either we solved it or this was a bad layout...go back...")
            number_of_iterations+=1
            # if board is full, we have a solution
            if row == size:#b/c row is only incrememnted when we can legally put down a piece - if we get to the last row we must have put down all pieces legally
                print("I did it! Here is my solution")
                display()
                #print(number_of_moves)
                return number_of_iterations, number_of_moves
            # I couldn't find a solution so I now backtrack
            prev_column = remove_in_current_row()
            # display_constraints()
            # print("removed queen and constraints")
            if (prev_column == -1): #I backtracked past column 1
                print("There are no solutions")
                #print(number_of_moves)
                return number_of_iterations, number_of_moves
            # try previous row again
            row -= 1
            # start checking at column = (1 + value of column in previous row)
            h_array = sorted(columns_by_preference, key=proximity_heuristic)
            i = h_array.index(prev_column) + 1

# def best_move(row, column):
#     r = row - 1
#     c = column - 1
#     min_pos_val = sys.maxsize
#     best_row = -1
#     best_column = -1
#     for i in range(3):
#         for j in range(3):
#             if r > -1 and r < size and column > -1 and column < size and (not (r == row and c == column)):
#                 if constraints_board[r][c] <  min_pos_val:
#                     min_pos_val = constraints_board[r][c]
#                     best_row = r
#                     best_column = c
#             c +=1
#         c = column - 1
#         r += 1
#     actual_board[row][column] = False
#     actual_board[best_row][best_column] = True
#     return best_row, best_column

def move_queen_with_most_constraints():
    max_constraints_val = max(queen_constraints)#here i get the value of the # of constrsints of the most constrained queen
    index_with_most_constraints = queen_constraints.index(max_constraints_val)#this is the index in colums of the most constrained queen which is also the row of that queen
    # best_row, best_column = best_move(index_with_most_constraints, columns[index_with_most_constraints])
    index_with_min_constraints = constraints_board[index_with_most_constraints].index(min(constraints_board[index_with_most_constraints]))#this is the minimally constrained column in that row - lets try to move the queen here
    remove_vertical_constraints(columns[index_with_most_constraints])
    remove_diag1_constraints(index_with_most_constraints, columns[index_with_most_constraints])
    remove_diag2_constraints(index_with_most_constraints, columns[index_with_most_constraints])
    columns[index_with_most_constraints] = index_with_min_constraints
    add_vertical_constraints(columns[index_with_most_constraints])
    add_diag1_constraints(index_with_most_constraints, columns[index_with_most_constraints])
    add_diag2_constraints(index_with_most_constraints, columns[index_with_most_constraints])

    #thats is also the row

def solve_queen_stochastically():
    global columns
    global constraints_board
    least_constraints_columns = [0 for i in range(size)]
    least_constraints = sys.maxsize
    constraints = 0
    num_of_iterations = 0
    for i in range(100):#restart 20 times
        for i in range(size * 100):#try to get a goodboard 100X
            place_n_queens(size)
            num_of_iterations += 1
            if is_kosher_board(size):#is it kosher? if not lets do some climbing
                return num_of_iterations
            add_complete_constraints()#set up the constraints 
            constraints = count_complete_constraints() #count them and get array
            if constraints < least_constraints: #test them - if its good save it
                least_constraints = constraints
                for i in range(len(columns)):
                    least_constraints_columns[i] = columns[i]
            #clear board - were going to try again
            constraints_board = [[0 for i in range(size)] for j in range(size)]
        columns = least_constraints_columns #ok this is the board were working with
        add_complete_constraints() #reset those constraints of it

        if is_kosher_board(size):#is it kosher? if not lets do some climbing
            return num_of_iterations
        prev_constraints = sys.maxsize
        while True:#lets try 1000 times to make this board perfect
            #hill climbing
            if is_kosher_board(size):
                break
            #take the queen with most constraints and move her to a column of least constraints
            move_queen_with_most_constraints()
            num_of_iterations +=1
            #remove those old constraints and add the new ones - technically we just need to do that for one addition and one subtraction
            #but for simplicitly wee=ll just re add all constraints whis is good b/c.
            #first lets try to remove indivdually in move_queen_with_most_constraints() function
            #if that makes problems then just clear constraints board and then add them and count them
            current_constraints = count_complete_constraints()#reorders queen_constraints array
            if is_kosher_board(size):
                break
            if(current_constraints < prev_constraints):
                prev_constraints = current_constraints
            else:
                break
        if is_kosher_board(size):
            break
    return num_of_iterations
"""This code is nice, but it uses three functions:

1. place_in_next_row

2. remove_in_current_row

3. next_row_is_safe

That we now have to define


"""

def place_in_next_row(column):
    columns.append(column)
 
def remove_in_current_row():
    if len(columns) > 0:
        return columns.pop()
    return -1
 
def next_row_is_safe(column):
    row = len(columns) 
    # check column
    for queen_column in columns: #down in same line
        if column == queen_column:
            return False
 
    # check diagonal
    for queen_row, queen_column in enumerate(columns): #(row, column) check right diag
        if queen_column - queen_row == column - row:
            return False
 
    # check other diagonal
    for queen_row, queen_column in enumerate(columns): #im guessing check left
        if ((size - queen_column) - queen_row
            == (size - column) - row):
            return False
    return True

def my_next_row_is_safe(column, virtual_columns):
    row = len(virtual_columns) 
    # check column
    for queen_column in virtual_columns:
        if column == queen_column:
            return False
 
    # check diagonal
    for queen_row, queen_column in enumerate(virtual_columns):
        if queen_column - queen_row == column - row:
            return False
 
    # check other diagonal
    for queen_row, queen_column in enumerate(virtual_columns):
        if ((size - queen_column) - queen_row
            == (size - column) - row):
            return False
    return True

def is_kosher_board(size):
    virtual_columns = []
    virtual_columns.append(columns[0]) #place the first queen of the supposed solution
    solved = True
    for i in range(1,size):
        if(my_next_row_is_safe(columns[i], virtual_columns)):
            virtual_columns.append(columns[i])
        else:
            solved = False
            break
    return solved
    
def british_museum_algorithm():
    solved = False
    iterations = 0
    while solved == False:
        iterations+=1
        place_n_queens(size)
        solved = is_kosher_board(size)
    # display()
    # print(columns)
    # print('British Museum Algorithm took ' + str(iterations) + ' iterations to solve')
    return iterations

#british_museum_algorithm()

#size = int(input('Enter n: '))
num_iterations=0
number_moves = 0
#for i in range(0, 100):
#    columns = [] #columns is the locations for each of the queens
#heuristic #1 lets try to place the next queen a horses distance away from the prev queen - this is the minimum distance - my intuition is that the reason this is good is because the constraints created by this heuristic overlapps largely with the constraints already there.
#Basically place the queen in the next row two positions forward. if it surpasses size then wrap around . 
#possible improvements are if wrap around just try the first sloT
#instead of horse dist focus directly on the piece that is kosher and overlsaps the most with the current constraints.
size = 8
iterations_array_dfs = []
iterations_array_dfs_hueristic = []
iterations_array_stochastic = []
def print_comparison():
    print("    |   DFS            |  DFS With Heuristic     |  Stochastic Algorithm    | ")
    for i in range(len(iterations_array_dfs)):
        print("_____________________________________________")
        print(i + 4, "   |     ", iterations_array_dfs[i], "       |       ", iterations_array_dfs_hueristic[i], "            | ", iterations_array_stochastic[i])#, round(iterations_array_dfs[i]/iterations_array_dfs_hueristic[i], 1))


# british_museum_algorithm()
# print("Because of its ineffectiveness we will just display this algorithm for the 8 queens problem")
# size = 4
# while size < 12:
    
#     num_iterations, number_moves=solve_queen(size)
#     iterations_array_dfs.append(num_iterations)
#     # print('DFS with Backtracking took ' + str(num_iterations) + ' iterations to solve')
#     # print(columns)
#     constraints_board = [[0 for i in range(size)] for j in range(size)]
#     num_iterations, number_moves=solve_queen_with_heuristic(size)
#     iterations_array_dfs_hueristic.append(num_iterations)
#     # print('DFS with P-HEURISTIC took ' + str(num_iterations) + ' iterations to solve')
#     # print(columns)
#     queen_constraints = [0 for i in range(size)]
#     constraints_board = [[0 for i in range(size)] for j in range(size)]
#     num_iterations = solve_queen_stochastically()
#     iterations_array_stochastic.append(num_iterations)
#     print(is_kosher_board(size))
#     size+=1
# print_comparison()


size = 4
sum = 0
trials = 100
for i in range(trials):
    sum += british_museum_algorithm()
print("The Average for the British Museum Algorithm for a board of size 4 is: ", sum/trials)

num_iterations, number_moves=solve_queen(size)
print("While dfs did it in: ", num_iterations)

constraints_board = [[0 for i in range(size)] for j in range(size)]
num_iterations, number_moves=solve_queen_with_heuristic(size)
print("And dfs with heuristic did it in: ", num_iterations)

size = 8
sum = 0
num_iterations, number_moves=solve_queen(size)
print("The number of iterations of DFS with Backtracking for the 8 Queens problem is: ", num_iterations)
print('This was only done once since it is deterministic')

constraints_board = [[0 for i in range(size)] for j in range(size)]
num_iterations_heuristic, number_moves=solve_queen_with_heuristic(size)

print("The number of iterations of DFS with my Heuristic for the 8 Queens problem is: ", num_iterations_heuristic)
print("This is ", round(num_iterations/num_iterations_heuristic, 2), "X faster than plain DFS")


size = 8
sum = 0
print("Hold On just a second.... (executing our stochastic algorithm 100X)")
for i in range(100):
    constraints_board = [[0 for i in range(size)] for j in range(size)]
    queen_constraints = [0 for i in range(size)]
    sum += solve_queen_stochastically()
stochastic_avg = sum/100
print("Stochastic Average for 8 Queens run 100X: ", round(stochastic_avg, 2))
print("This is ", round(num_iterations/stochastic_avg, 2), "X the speed of regular DFS")
print("Admittedly our stochastic Algorithm doesnt work quite so well")
print("But our DFS with heuristic does! In fact it was 40,000X faster than regular DFS for the 30 Queens problem!!!")
"""Now what?  Can you implement the British Museum Algorithm?  How many iterations did it take to solve the 4 queens problem?  How many did it take to solve the 8 queens (if at all)?"""