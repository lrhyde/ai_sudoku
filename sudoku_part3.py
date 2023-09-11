# -*- coding: utf-8 -*-
"""
Created on Tue Nov 16 09:23:33 2021

@author: 1531402
"""

import math, sys, random, time

subblock_height = None
subblock_width  = None
symbol_set = None
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
puzzle = ""
neighbors = {}
closed = set()
constraints = set()

def sbw(n):
    if((int)(math.sqrt(n))-math.sqrt(n)==0): 
        return (int)(math.sqrt(n))
    for i in range(((int)(math.sqrt(n))+1), n):
        if(n%i==0): return i
    return None

def sbh(n):
    for j in range(1, ((int)(math.sqrt(n)+1))):
        i = (int)(math.sqrt(n)+1)-j
        if(n%i==0): return i
    return None

def symbols(n):
    if(n<=9):
        return [str(i) for i in range(1, n+1)]
    else:
        return [str(i) for i in range(1, 10)] + [alphabet[i] for i in range(0, n-9)]

def printboard(n):
    for i in range(n):
        for j in range(n):
            if(len(puzzle[n*i+j])>1): 
                print('.', end = " ")
            else: print(puzzle[n*i+j], end=" ")
        print()
        
def printboard(p, n):
    for i in range(n):
        for j in range(n):
            if(len(puzzle[n*i+j].strip())>1): 
                print('.', end = " ")
            else: print(puzzle[n*i+j], end=" ")
        print()
        
#def printdict(p, n)

def populateNeighbors(n, subblock_width, subblock_height):
    #BOX NEIGHBORS ARE WRONG
    for i in range(n):
        for j in range(n):
            #neighbors[n*i+j]
            one = [n*i+x for x in range(n)]
            two = [n*x+j for x in range(n)]
            row= (int)(i/subblock_height)
            col= (int)(j/subblock_width)
            three = []
            for x in range(subblock_height):
                for y in range(subblock_width):
                    three.append(n*(subblock_height*row+x)+ (subblock_width*col)+y)
            neighbors[n*i+j] = [one, two, three]
        #print()
        
def populateConstraintSets(n, subblock_width, subblock_height):
    global constraints
    for i in range(n):
        for j in range(n):
            #neighbors[n*i+j]            
            row= (int)(i/subblock_height)
            col= (int)(j/subblock_width)
            three = []
            for x in range(subblock_height):
                for y in range(subblock_width):
                    three.append(n*(subblock_height*row+x)+ (subblock_width*col)+y)
            constraints.add(tuple(three))
        #print()
        one = tuple([n*i+x for x in range(n)])
        two = tuple([n*x+i for x in range(n)])
        constraints.add(one)
        constraints.add(two)

def countSymbols(symbol_set, puzzle):
    for symbol in symbol_set:
        print(symbol + ": " + str(puzzle.count(symbol)))

def csp_backtracking(state):
    if is_possible(state): return state
    #if not is_viable(state): return None
    #    if(state[0]=='6' and state[2]=='4'): 
    #    printboard(state, n)
    #    print()
    #print(state)
    var = get_next_unassigned_var(state)
    if(var==-1):
        if is_possible(state): return state
        return None
    for val in get_sorted_values(state, var): 
        #new_state[var]=val
        new_state = state[0:var] + val + state[var+1:]
        result = csp_backtracking(new_state)
        if (not result ==None):
            return result
    return None

def csp_backtracking_with_forward_looking(board): #debug constraint
    if is_possible2(board): return board
    var = get_most_constrained_var(board) # Note the change here!
    for val in get_sorted_values2(board, var):
        new_board = board.copy() # VERY IMPORTANT!
        new_board[var]=val
        checked_board = forward_looking(new_board)
        if checked_board is not None:
            checked_board = constraint_propagation(checked_board)
            if(checked_board is not None):
                print(str(countSolved(checked_board)))
                result = csp_backtracking_with_forward_looking(checked_board)
                if result is not None:
                    return result
    return None

def countSolved(board):
    count=0
    for i in range(len(board)):
        if(len(board[i])==1): count+=1
    return count

def get_most_constrained_var(board):
    mindex = 0
    for i in range(len(board)):
        if((len(board[mindex])>len(board[i]) or len(board[mindex])==1) and not len(board[i])==1): mindex=i
    return mindex

def get_sorted_values2(board, var):
    return board[var]

def interpret_board(initial):
    s = ""
    for i in range(len(symbol_set)):
        s+=symbol_set[i]
    board = {}
    for i in range(len(initial)):
        if(initial[i]=='.'):
            #board[i]=symbol_set.copy()
            board[i]=""+s
        else: board[i]=initial[i]
    return board
"""
1. Make a list of all indices that have one possible solution (or, alternately, are solved).
2. For each index in this list, loop over all other indices in that index’s set of neighbors, and remove the value at the solved index from each one. If any of these becomes solved, add them to the list of solved indices.
3. If any index becomes empty, then a bad choice has been made and the function needs to immediately return something that clearly indicates failure (like “None”).
4. Continue until the list is empty.
"""

def forward_looking(board): #possible logic problem??
    if is_possible2(board): return board
    oneList = []
    #closed = set()
    global closed
    for i in range(len(board)):
        if(len(board[i])==1): 
            oneList.append(i)
            closed.add(i)
    while(len(oneList)>0):
        current = oneList.pop()
        #if(current==31): 
            #print("hi debugger")
        for neighbor in neighbors[current][0] + neighbors[current][1] + neighbors[current][2]:
            if(not len(board[neighbor])==1 and board[current] in board[neighbor] and not neighbor==current): 
                if(len(board[neighbor])==1): return None
                #board[neighbor].remove(board[current])
                board[neighbor] = board[neighbor].replace(board[current], '')
                
            if(len(board[neighbor])==1 and not neighbor==current and board[neighbor]==board[current]): return None
            if(len(board[neighbor])==1 and not neighbor==current): 
                #board[neighbor] = board[neighbor][0]
                if(neighbor not in closed): 
                    oneList.append(neighbor)
                    closed.add(neighbor)
            if(len(board[neighbor])==0): return None
    return board

def is_possible2(state):
    """
    #if('.' in state): return False
    for key in neighbors:
        for index in range(n):
            #print(neighbors[key][0])
            if(state[neighbors[key][0][index]]==state[key]):
                if(not neighbors[key][0][index]==key): return False
            if(state[neighbors[key][1][index]][0]==state[key][0]):
                if(not neighbors[key][1][index]==key): return False
            if(state[neighbors[key][2][index]][0]==state[key][0]):
                if(not neighbors[key][2][index]==key): return False
    return True
"""
    for index in state:
        if(len(state[index])>1): return False
    return True

def is_possible(state):
    """
    if('.' in state): return False
    for key in neighbors:
        for index in range(n):
            #print(neighbors[key][0])
            if(state[neighbors[key][0][index]]==state[key]):
                if(not neighbors[key][0][index]==key): return False
            if(state[neighbors[key][1][index]]==state[key]):
                if(not neighbors[key][1][index]==key): return False
            if(state[neighbors[key][2][index]]==state[key]):
                if(not neighbors[key][2][index]==key): return False
    return True
"""
    return ("." not in state)

def get_next_unassigned_var(state):
    return state.find('.')
    
def get_sorted_values(state, var):
    
    copysym = symbol_set.copy()
    #print(copysym)
    """
    for symbol in symbol_set:
        for thing in set(neighbors[var][0])|set(neighbors[var][1])|set(neighbors[var][2]):
            if(state[thing]==symbol and symbol in copysym): copysym.remove(symbol)
    return copysym 
"""
    for index in neighbors[var][0] + neighbors[var][1] + neighbors[var][2]:
        if(state[index] in copysym): copysym.remove(state[index])
    return copysym
    #return symbol_set
    
def constraint_propagation2(board): 
    #make a list of the indices w symbol, if length is 1 set
    bobo = board.copy()
    ss = {}
    for char in symbol_set:
        ss[char] = []
    for cs in constraints:
        for i in range(len(cs)):
            for char in board[cs[i]]:
                ss[char].append(cs[i])
        for key in ss:
            if(len(ss[key])==1): board[ss[key][0]]=key
    return forward_looking(board)

def constraint_propagation(board): 
    #make a list of the indices w symbol, if length is 1 set
    global constraints
    bobo = board.copy()
    for cs in constraints:
        #print(cs)
        temp = ""
        for i in range(len(cs)):
            temp+=(board[cs[i]])
        for symbol in symbol_set:
            if(symbol not in temp): return None
            elif(temp.count(symbol)>1): break
            else: 
                #constraint set is a set of indices
                #take the index that contains the value
                #set it to that value
                for i in range(len(cs)):
                    if(symbol in board[cs[i]]):
                        board[cs[i]]=symbol
                        break
    #if(bobo==board): return None
    return forward_looking(board)

filename = sys.argv[1]    
with open(filename) as f:  
    puzzlecount = 0
    t = time.perf_counter()
    for line in f:
        #puzzle = line.strip()
        puzzle = "58.7.....6.....2.......3...1...6......4...3.....5.......3.92....2......5.......1."
        #puzzle = "....8.4....2....1..6.......59....1.....6.2.......7.......5...6.4..1.....3...4...."
        n = (int)(math.sqrt(len(puzzle)))
        #global symbol_set
        symbol_set = symbols(n)
        puzzle = interpret_board(puzzle)
        subblock_width = sbw(n)
        subblock_height = sbh(n)
        q = populateNeighbors(n, subblock_width, subblock_height)
        populateConstraintSets(n, subblock_width, subblock_height)
        printboard(puzzle, n)
        print()
        
        t1= time.perf_counter()
        puzzle = constraint_propagation(puzzle)
        t2 = time.perf_counter()
        puzzle = forward_looking(puzzle)
        #printboard(puzzle, n)
        solved = csp_backtracking_with_forward_looking(puzzle)
        puzzle = solved
        t3 = time.perf_counter()
        #print()
        #print(solved)
        printboard(solved, n)
        print(str(t2-t1))
        print(str(t3-t2))
        ##########countSymbols(symbol_set, solved)
        ##########print(solved)
        print()
        break
    t2 = time.perf_counter()
    print(str(t2-t))