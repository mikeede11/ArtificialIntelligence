#search

import state
import frontier

popped = int(0)
totalMaxDepth = 0 #over 100 runs
totalPushed = 0
totalPopped = 0 


def search(n):
    global totalMaxDepth, totalPushed, totalPopped
    s=state.create(n) #creates the board and legal moves and shuffles the board (n^3 thing)
    # print(s) #display initial state
    f=frontier.create(s) # [stack with the game board/possible states of board, maxDepth of 1, game board, try next level, totalItemsPush*]  IDS
    while not frontier.is_empty(f):
        s=frontier.remove(f) #runs stack.remove on the stack that is located at first index in frontier. and it returns that popped item which is a possible next state
        # print("try this state")
        if state.is_target(s):          
            totalMaxDepth += f[1]
            totalPushed += f[4]
            totalPopped += frontier.getPopped()
            # print("The max Depth was: " + str(f[1]))
            # print("This is the number of states pushed: " + str(f[4]))
            # print("This is the number of states popped: " + str(frontier.getPopped()))
            return [s, f[1]]
        ns=state.get_next(s) #gets the list of possible next states (moves we can do)
        #print(ns)
        for i in ns:
            frontier.insert(f,i) #insert the possible next states onto the stack OH so the stack contains the states and each time we dont get the target state we put on the stack the possible other states from legal moves. we then examine each one iteratively. IDS set by max depth param f[1]
    return 0

def printResults(avgMaxDepth, avgPushed, avgPopped):
    print("Average depth: " + str(avgMaxDepth))
    print("Average number pushed: " + str(avgPushed))
    print("Average number popped: " + str(avgPopped))


for i in range(100):
    search(2)
print("Results for 100 runs of search(2)")
printResults(totalMaxDepth/100, totalPushed/100, totalPopped/100)
totalMaxDepth = 0
totalPushed = 0
totalPopped = 0

for i in range(100):
    search(3)
print("Results for 100 runs of search(3)")
printResults(totalMaxDepth/100, totalPushed/100, totalPopped/100)
totalMaxDepth = 0
totalPushed = 0
totalPopped = 0

#many search(4) executions will not complete in a bearable amount of time
#at first I thought this was my fault and something I messed iup in the code
#but after thinking about it the number of possibilities and therefore the upper 
#bound of the problem is way more than search(3) - like waaay more
# 16!/9! = 57657600 times slower. No wonder it doesnt finish - in fact if we estimate that 
# search(3) takes one second to complete search(4) can take almost 2 years to complete!!!!!
print("Results for 100 runs of search(4)")
for i in range(100):
    search(4)
printResults(totalMaxDepth/100, totalPushed/100, totalPopped/100)
totalMaxDepth = 0
totalPushed = 0
totalPopped = 0
