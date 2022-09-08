#search

import state
import frontier

totalPushed = 0
totalPopped = 0 
totalPathCost = 0

def search(n):
    global totalPathCost, totalPushed, totalPopped
    s=state.create(n)
    # print(s)
    # print("bricks out of place: " + str(state.hdistance1(s)))
    # print("Total Manhattan Distance: " + str(state.hdistance2(s)))
    f=frontier.create(s)
    while not frontier.is_empty(f):
        s=frontier.remove(f)
        if state.is_target(s):
            totalPushed += f[1]
            totalPopped += f[1] - len(f[0])
            totalPathCost += state.path_len(s)
            # print("The # of items pushed: " + str(f[1]))
            # print("This is the number of states popped: " + str(f[1] - len(f[0])))
            # print("The total path cost is: " + str(state.path_len(s)))
            return [s, f[1]]
        ns=state.get_next(s)
        for i in ns:
            frontier.insert(f,i)
    return 0

def printResults(avgCost, avgPushed, avgPopped):
    print("Average Path Cost: " + str(avgCost))
    print("Average number pushed: " + str(avgPushed))
    print("Average number popped: " + str(avgPopped))

print("Results for 100 runs of search(4)")
for i in range(100):
    search(4)
print("Results for 100 runs of search(4) using the h2 heuristic (Manhattan Distance) with A* weight")
printResults(totalPathCost/100, totalPushed/100, totalPopped/100)
totalMaxDepth = 0
totalPushed = 0
totalPopped = 0





