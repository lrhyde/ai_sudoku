# -*- coding: utf-8 -*-
"""
Created on Thu Nov  4 15:02:08 2021

@author: 1531402
"""

import math, sys, random

subblock_height = None
subblock_width  = None
symbol_set = None
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
puzzle = ""
neighbors = {}

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
            print(puzzle[n*i+j], end=" ")
        print()
        
def printboard(p, n):
    for i in range(n):
        for j in range(n):
            print(p[n*i+j], end=" ")
        print()

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

def csp_backtracking_with_forward_looking(board):
    if is_possible2(board): return board
    var = get_most_constrained_var(board) # Note the change here!
    for val in get_sorted_values2(board, var):
        new_board = board.copy() # VERY IMPORTANT!
        new_board[var]=[val]
        checked_board = forward_looking(new_board)
        if checked_board is not None:
            result = csp_backtracking_with_forward_looking(checked_board)
            if result is not None:
                return result
    return None

def get_most_constrained_var(board):
    mindex = 0
    for i in range(board):
        if((len(board[mindex])>len(board[i]) or len(board[mindex])==1) and not len(board[i]==1)): mindex=i
    return mindex

def get_sorted_values2(board, var):
    return board[var]

def interpret_board(initial):
    board = {}
    for i in range(len(initial)):
        if(initial[i]=='.'):
            board[i]=symbol_set.copy()
        else: board[i]=initial[i]
    return board
"""
1. Make a list of all indices that have one possible solution (or, alternately, are solved).
2. For each index in this list, loop over all other indices in that index’s set of neighbors, and remove the value at the solved index from each one. If any of these becomes solved, add them to the list of solved indices.
3. If any index becomes empty, then a bad choice has been made and the function needs to immediately return something that clearly indicates failure (like “None”).
4. Continue until the list is empty.
"""

def forward_looking(board):
    oneList = []
    closed = set()
    for i in range(len(board)):
        if(len(board[i])==1): oneList.append(i)
        closed.add(i)
    while(len(oneList)>0):
        current = oneList.pop()
        for neighbor in neighbors[current][0] + neighbors[current][1] + neighbors[current][2]:
            if(board[current] in board[neighbor]): 
                if(len(board[neighbor])==1): return None
                board[neighbor].remove(board[current])
            if(len(board[neighbor])==1): 
                board[neighbor] = board[neighbor][0]
                if(neighbor not in closed): oneList.add(neighbor)
                closed.add(neighbor)
            if(len(board[neighbor])==0): return None
    return board

def is_possible2(state):
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

def is_viable(state):
    #if('.' in state): return False
    for key in neighbors:
        for index in range(n):
            #print(neighbors[key][0])
            if(state[neighbors[key][0][index]]==state[key]):
                if(not state[key]=='.' and not neighbors[key][0][index]==key): return False
            if(state[neighbors[key][1][index]]==state[key]):
                if(not state[key]=='.' and not neighbors[key][1][index]==key): return False
            if(state[neighbors[key][2][index]]==state[key]):
                if(not state[key]=='.' and not neighbors[key][2][index]==key): return False
    return True
    
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

filename = sys.argv[1]    
with open(filename) as f:  
    puzzlecount = 0
    for line in f:
        puzzle = line.strip()
        n = (int)(math.sqrt(len(puzzle)))
        #global symbol_set
        symbol_set = symbols(n)
        #puzzle = interpret_board(puzzle)        
        subblock_width = sbw(n)
        subblock_height = sbh(n)
        #print(subblock_width)
        #print(subblock_height)
        q = populateNeighbors(n, subblock_width, subblock_height)
        ##########printboard(puzzle, n)
        ##########print()
        #print(get_sorted_values(puzzle, 0)) 
        #print(get_sorted_values(puzzle, 2)) 
        #print(get_sorted_values(puzzle, 3)) 
        #print(get_sorted_values(puzzle, 4)) 
        solved = csp_backtracking(puzzle)
        #puzzle = forward_looking(puzzle)
        #solved = csp_backtracking_with_forward_looking(puzzle)
        #puzzle = solved
        ##########printboard(solved, n)
        ##########countSymbols(symbol_set, solved)
        print(solved)
        print()
        #break