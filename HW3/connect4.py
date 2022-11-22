import copy
import numpy as np
import random
import sys
import colorama
from termcolor import colored  # can be taken out if you don't like it...

# # # # # # # # # # # # # # global values  # # # # # # # # # # # # # #
ROW_COUNT = 6
COLUMN_COUNT = 7

colorama.init()
RED_CHAR = colored('X', 'red')  # RED_CHAR = 'X'
BLUE_CHAR = colored('O', 'blue')  # BLUE_CHAR = 'O'

EMPTY = 0
RED_INT = 1
BLUE_INT = 2


# # # # # # # # # # # # # # functions definitions # # # # # # # # # # # # # #

def create_board(): #2d arr 6 rows 7 elems
    """creat empty board for new game"""
    board = np.zeros((ROW_COUNT, COLUMN_COUNT), dtype=int)
    return board


def drop_chip(board, row, col, chip): #drop this chip/int/1 or 2 at row col in board
    """place a chip (red or BLUE) in a certain position in board"""
    board[row][col] = chip


def is_valid_location(board, col): #comment below sums it up
    """check if a given column in the board has a room for extra dropped chip"""
    return board[ROW_COUNT - 1][col] == 0

def get_next_open_row(board, col): #finds the row height to put chip at if this column is chosen
    """assuming column is available to drop the chip,
    the function returns the lowest empty row  """
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

def print_board(board):
    """print current board with all chips put in so far"""
    # print(np.flip(board, 0))
    print(" 1 2 3 4 5 6 7 \n" "|" + np.array2string(np.flip(np.flip(board, 1)))
          .replace("[", "").replace("]", "").replace(" ", "|").replace("0", "_")
          .replace("1", RED_CHAR).replace("2", BLUE_CHAR).replace("\n", "|\n") + "|")

def game_is_won(board, chip):
    """check if current board contain a sequence of 4-in-a-row of in the board
     for the player that play with "chip"  """

    winning_Sequence = np.array([chip, chip, chip, chip])
    # Check horizontal sequences
    for r in range(ROW_COUNT):
        if "".join(list(map(str, winning_Sequence))) in "".join(list(map(str, board[r, :]))):
            return True
    # Check vertical sequences
    for c in range(COLUMN_COUNT):
        if "".join(list(map(str, winning_Sequence))) in "".join(list(map(str, board[:, c]))):
            return True
    # Check positively sloped diagonals
    for offset in range(-2, 4):
        if "".join(list(map(str, winning_Sequence))) in "".join(list(map(str, board.diagonal(offset)))):
            return True
    # Check negatively sloped diagonals
    for offset in range(-2, 4):
        if "".join(list(map(str, winning_Sequence))) in "".join(list(map(str, np.flip(board, 1).diagonal(offset)))):
            return True

def get_valid_locations(board): #makes list of valid columns
    valid_locations = []
    for col in range(COLUMN_COUNT):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations

def MoveRandom(board, color):
    valid_locations = get_valid_locations(board)
    column = random.choice(valid_locations)   # you can replace with input if you like... -- line updated with Gilad's code-- thanks!
    row = get_next_open_row(board, column)
    drop_chip(board, row, column, color)

def checkDown(board, color, row, col):
    if row == 0:
        return 0
    startColor = board[row - 1][col]
    if startColor == 0:
            return 0
    if startColor == color: #ok this is an opportunity for us to lengthen a segment
        if row - 3 >= 0 and board[row - 3][col] == board[row - 2][col] and board[row - 2][col] == board[row - 1][col]:
            return 150
        elif row - 2 >= 0 and board[row - 2][col] == board[row - 1][col]:
            return 8
        else:
            return 2
    
    if row - 3 >= 0 and board[row - 3][col] == board[row - 2][col] and board[row - 2][col] == board[row - 1][col]:
            return 50
    elif row - 2 >= 0 and board[row - 2][col] == board[row - 1][col]:
            return 6
    else:
            return 1

def heuristicValue(contiguousChips):
    value = 0
    if contiguousChips > 0:
        if contiguousChips == 1:
            value = 2
        elif contiguousChips == 2:
            value = 8
        else:
            value = 150
    elif contiguousChips < 0:
        if contiguousChips == -1:
            value = 1
        elif contiguousChips == -2:
            value = 6
        else:
            value = 50
    return value

def checkHorizontal(board, color, row, col):
    #similar to checkdown but instead change the columns
    leftValue = 0
    rightValue = 0
    leftEndChip = 1
    rightEndChip = 1
    if col - 1 >= 0:#check left side
        startColor = board[row][col - 1]
        if startColor != 0:
            if startColor == color: #in the case that the adjacent chip is the same color
                for i in range(1,4):
                    if col - i >= 0 and board[row][col - i] == startColor:
                        leftValue = i
                    elif col - i >= 0 and board[row][col - i] == 0:
                        leftEndChip = 0
                        break
                    else:
                        break
            else: #dif color
                for i in range(1,4):
                    if col - i >= 0 and board[row][col - i] == startColor:
                        leftValue = -i
                    elif col - i >= 0 and board[row][col - i] == 0:
                        leftEndChip = 0
                    else:
                        break

    if col + 1 < COLUMN_COUNT:#check right side
        startColor = board[row][col + 1]
        if startColor != 0:
            if startColor == color: #in the case that the adjacent chip is the same color
                for i in range(1,4):
                    if col + i < COLUMN_COUNT and board[row][col + i] == startColor:
                        rightValue = i
                    elif  col + i < COLUMN_COUNT and board[row][col + i] == 0:
                        rightEndChip = 0
                        break
                    else:
                        break #either the end of the board or the streak is broken - stop loop
            else: #dif color
                for i in range(1,4):
                    if col + i < COLUMN_COUNT and board[row][col + i] == startColor:
                        rightValue = -i
                    elif col + i < COLUMN_COUNT and board[row][col + i] == 0:
                        rightEndChip = 0
                        break
                    else:
                        break
    if leftValue > 0 and rightValue > 0:
        if leftValue + rightValue == 2 and leftEndChip == 0 and rightEndChip == 0:
            return 150
        elif leftValue + rightValue == 2:
            return 8
        else:
            return 150
    if leftValue < 0 and rightValue < 0:
        if leftValue + rightValue == -2 and leftEndChip == 0 and rightEndChip == 0:
            return 50
        elif leftValue + rightValue == -2:
            return 6
        else:
            return 50
    return heuristicValue(leftValue) + heuristicValue(rightValue)

def checkDiagonal1(board, color, row, col):
    #similar to checkdown but instead change the columns
    leftValue = 0
    rightValue = 0
    leftEndChip = 1
    rightEndChip = 1
    if col - 1 >= 0 and row - 1 >= 0:#check left side
        startColor = board[row - 1][col - 1]
        if startColor != 0:
            if startColor == color: #in the case that the adjacent chip is the same color
                for i in range(1,4):
                    r = row - i
                    c = col - i
                    if r >= 0 and c >= 0 and board[r][c] == startColor:
                        leftValue = i
                    elif r >= 0 and c >= 0 and board[r][c] == 0:
                        leftEndChip = 0
                    else:
                        break
            else: #dif color
                for i in range(1,4):
                    r = row - i
                    c = col - i
                    if r >= 0 and c >= 0 and board[r][c] == startColor:
                        leftValue = -i
                    elif r >= 0 and c >= 0 and board[r][c] == 0:
                        leftEndChip = 0
                        break
                    else:
                        break

    if row + 1 < ROW_COUNT and col + 1 < COLUMN_COUNT:#check right side
        startColor = board[row + 1][col + 1]
        if startColor != 0:
            if startColor == color: #in the case that the adjacent chip is the same color
                for i in range(1,4):
                    r = row + i
                    c = col + i
                    if r < ROW_COUNT and c < COLUMN_COUNT and board[r][c] == startColor:
                        rightValue = i
                    elif r < ROW_COUNT and c < COLUMN_COUNT and board[r][c] == 0:
                        rightEndChip = 0
                        break
                    else:
                        break #either the end of the board or the streak is broken - stop loop
            else: #dif color
                for i in range(1,4):
                    r = row + i
                    c = col + i
                    if r < ROW_COUNT and c < COLUMN_COUNT and board[r][c] == startColor:
                        rightValue = -i
                    elif r < ROW_COUNT and c < COLUMN_COUNT and board[r][c] == 0:
                        rightEndChip = 0
                        break
                    else:
                        break
    if leftValue > 0 and rightValue > 0:
        if leftValue + rightValue == 2 and leftEndChip == 0 and rightEndChip == 0:
            return 150
        elif leftValue + rightValue == 2:
            return 8
        else:
            return 150
    if leftValue < 0 and rightValue < 0:
        if leftValue + rightValue == -2 and leftEndChip == 0 and rightEndChip == 0:
            return 50
        elif leftValue + rightValue == -2:
            return 6
        else:
            return 50
    return heuristicValue(leftValue) + heuristicValue(rightValue)

    

def checkDiagonal2(board, color, row, col):
    leftValue = 0
    rightValue = 0
    leftEndChip = 1
    rightEndChip = 1
    if row + 1 < ROW_COUNT and col - 1 >= 0:#check left side
        startColor = board[row + 1][col - 1]
        if startColor != 0:
            if startColor == color: #in the case that the adjacent chip is the same color
                for i in range(1,4):
                    r = row + i
                    c = col - i
                    if r < ROW_COUNT and c >= 0 and board[r][c] == startColor:
                        leftValue = i
                    elif r < ROW_COUNT and c >= 0 and board[r][c] == 0:
                        leftEndChip = 0
                        break
                    else:
                        break
            else: #dif color
                for i in range(1,4):
                    r = row + i
                    c = col - i
                    if r < ROW_COUNT and c >= 0 and board[r][c] == startColor:
                        leftValue = -i
                    elif r < ROW_COUNT and c >= 0 and board[r][c] == 0:
                        leftEndChip = 0
                        break
                    else:
                        break

    if row - 1 >= 0 and col + 1 < COLUMN_COUNT:#check right side
        startColor = board[row - 1][col + 1]
        if startColor != 0:
            if startColor == color: #in the case that the adjacent chip is the same color
                for i in range(1,4):
                    r = row - i
                    c = col + i
                    if r >= 0 and c < COLUMN_COUNT and board[r][c] == startColor:
                        rightValue = i
                    elif r >= 0 and c < COLUMN_COUNT and board[r][c] == 0:
                        rightEndChip = 0
                        break
                    else:
                        break #either the end of the board or the streak is broken - stop loop
            else: #dif color
                for i in range(1,4):
                    r = row - i
                    c = col + i
                    if r >= 0 and c < COLUMN_COUNT and board[r][c] == startColor:
                        rightValue = -i
                    elif r >= 0 and c < COLUMN_COUNT and board[r][c] == 0:
                        rightEndChip = 0
                        break
                    else:
                        break
    if leftValue > 0 and rightValue > 0:
        if leftValue + rightValue == 2 and leftEndChip == 0 and rightEndChip == 0:
            return 150
        elif leftValue + rightValue == 2:
            return 8
        else:
            return 150
    if leftValue < 0 and rightValue < 0:
        if leftValue + rightValue == -2 and leftEndChip == 0 and rightEndChip == 0:
            return 50
        elif leftValue + rightValue == -2:
            return 6
        else:
            return 50
    return heuristicValue(leftValue) + heuristicValue(rightValue)

    #starting from row -1 for each consecutive color dhip you hit add to counter 
def evalMove(board, color, row, col):
    value = 0
    value += checkDown(board,color, row, col)
    value += checkHorizontal(board,color, row, col)
    value += checkDiagonal1(board,color, row, col)
    # print("Numbers for col: ", col)
    # print("CD: ", checkDown(board,color, row, col))
    # print("CH: ", checkHorizontal(board,color, row, col))
    # print("CD1: ", checkDiagonal1(board,color, row, col))
    # print("CD2: ", checkDiagonal2(board,color, row, col))
    value += checkDiagonal2(board,color, row, col)
    return value
    #yada
    #double trap???
    #special case horizontal with 2 chips and 

def agent1move(board, color):
    bestColumn = -1
    row = -1
    bestMoveValue = -sys.maxsize - 1
    currentMoveValue = -sys.maxsize - 1
    '''this method needs to put the color in each column, analyze the heuristic value for that color for each and then return the lowest one '''
    
    valid_locations = get_valid_locations(board)
    for col in valid_locations:
        row = get_next_open_row(board, col)
        currentMoveVal = evalMove(board, color, row, col)
        if currentMoveVal > bestMoveValue:
            bestMoveValue = currentMoveVal
            bestColumn = col
    return bestColumn

def moveHeuristic(board, color):
    column = agent1move(board, color) #analyze board state and pick the optimal column based on heuristic(s)
    row = get_next_open_row(board, column)
    drop_chip(board, row, column, color)

def lookAhead(board, color, moves):
    tree = 0
    #fill in


# # # # # # # # # # # # # # main execution of the game # # # # # # # # # # # # # #
agent1Wins = 0
randomAgentWins = 0
for i in range(100):
    turn = 0

    board = create_board()
    # print_board(board)
    game_over = False

    while not game_over:
        if turn % 2 == 0:#PLAYER 1 ME / MY AGENT
            moveHeuristic(board,RED_INT)

        if turn % 2 == 1 and not game_over:#PLAYER 2 RANDOM AGENT
            MoveRandom(board,BLUE_INT) #EXECUTE MOVE

        # print_board(board) #PRINT UPDATE
        
        #CHECK GAME STATUS AFTER EACH MOVE
        if game_is_won(board, RED_INT): 
            game_over = True
            agent1Wins += 1
            print(colored("Red wins!", 'red'))
        if game_is_won(board, BLUE_INT):
            game_over = True
            randomAgentWins += 1
            print_board(board)
            print(colored("Blue wins!", 'blue'))
        if len(get_valid_locations(board)) == 0:
            game_over = True
            print(colored("Draw!", 'blue'))
        turn += 1 #NO CONDITIONS ABOVE WAS TRUE game_over is still false well do it again. go to top

print("Agent 1 won ", agent1Wins, " times")
print("Random Agent won ", randomAgentWins, " times")
print("our Agents win Rate was ", agent1Wins/100, " % ")
#tmp = copy.deepcopy(board)