'''
empty stack [0]
[3,[2,[1,[0]]]] stack that contains 3,2,1
3 is the top of the stack
'''

# creates a stack with x

totalItemsPopped = 0

def create(x): ##returns a stack with the first element
    s=[0] #null set empty set
    insert(s,x)
    return s    

def is_empty(s):
    return s==[0]

def insert(s,x):
    s[0]=[x,s[0]]

def remove(s):
    if is_empty(s): # underflow
        return 0
    x=s[0][0] #save top element
    s[0]=s[0][1] #remove that element from stack
    global totalItemsPopped
    totalItemsPopped += 1
    return x # return popped element

def getPopped():
    return totalItemsPopped 

