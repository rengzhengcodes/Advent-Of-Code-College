import sys
sys.path.append("../")
from advent_io import *

# type hinting
from typing import Union
from numbers import Number
# imports a stack-like object
from collections import deque
# import pandas and StringIO to feed data into pandas
from io import StringIO
from time import sleep
import numpy as np
import pandas as pd
import regex as re

fetch_input(8, 2022)

def soln_1():
    with open("input.txt", 'r') as file:
        raw:str = file.read().rstrip()
        # converts each row into its own list
        rows:list = raw.split('\n')
        # converts each char of string into its own list element
        rows:list[list[int]] = [list(row) for row in rows]
    
    # turns each char into an int so we can actually process it
    for row in rows:
        for i in range(len(row)):
            row[i] = int(row[i])
    
    # creates a numpy array representing tree heights and then one representing if they're visible by 1 if they are, 0 if they aren't
    trees:np.ndarray[int] = np.array(rows, int)
    visible:np.ndarray[int] = np.zeros((len(rows), len(rows[0])), int)

    def check_trees_visible_left_right(trees:np.ndarray, visible:np.ndarray) -> None:
        """
        Takes a trees numpy array and checks if a tree is visible left to right
        trees:
            numpy array of tree heights
        visible:
            numpy array representing if a tree is visible
        """
        # iterates along rows
        i:int
        for i in range(len(trees)):
            # trees can't be negative height, so this ensures we count all trees
            tallest_tree:int = -1

            # goes along the row
            j:int
            for j in range(len(trees[i])):
                # if a tree is taller than all previous, mark it visible and make it the tallest tree we've seen
                if tallest_tree < trees[i][j]:
                    visible[i][j] = 1
                    tallest_tree = trees[i][j]
    
    check_trees_visible_left_right(trees, visible)
    
    visible = np.rot90(visible)
    trees = np.rot90(trees)
    check_trees_visible_left_right(trees, visible)

    visible = np.rot90(visible)
    trees = np.rot90(trees)
    check_trees_visible_left_right(trees, visible)

    visible = np.rot90(visible)
    trees = np.rot90(trees)
    check_trees_visible_left_right(trees, visible)

    visible_trees:int = int(np.sum(visible))
    print(visible_trees)
    copy_ans(visible_trees)

soln_1()

def soln_2():
    with open("input.txt", 'r') as file:
        raw:str = file.read().rstrip()
        # converts each row into its own list
        rows:list = raw.split('\n')
        # converts each char of string into its own list element
        rows:list[list[int]] = [list(row) for row in rows]
    
    # turns each char into an int so we can actually process it
    for row in rows:
        for i in range(len(row)):
            row[i] = int(row[i])
    
    # creates a numpy array representing tree heights and then one representing if they're visible by 1 if they are, 0 if they aren't
    trees:np.ndarray[int] = np.array(rows, int)
    scenic:np.ndarray[int] = np.zeros((len(rows), len(rows[0])), int)

    def scenic_score(trees, y, x):
        # looks from the tree up
        up_dist:int = 0
        i:int
        for i in range(y - 1, -1, -1):
            if trees[i][x] >= trees[y][x]:
                up_dist = y - i
                break
        # if it hits edge without hitting tree >= to its height, use distance to edge
        if up_dist == 0:
            up_dist = y

        # looks from the tree down
        down_dist:int = 0
        i:int
        for i in range(y + 1, len(trees)):
            if trees[i][x] >= trees[y][x]:
                down_dist = i - y
                break
        # if it hits an edge without encountering a tree >= to its height
        if down_dist == 0:
            down_dist = len(rows) - 1 # stops counting current tree
            down_dist -= y # distance to edge      
        
        # looks from the tree left
        left_dist:int = 0
        i:int
        for i in range(x - 1, -1, -1):
            if trees[y][i] >= trees[y][x]:
                left_dist = x - i
                break
        # if it hits edge without hitting tree >= to its height, use distance to edge
        if left_dist == 0:
            left_dist = x
        
        # loosk from the tree right
        right_dist:int = 0
        i:int
        for i in range(x + 1, len(trees[y])):
            if trees[y][i] >= trees[y][x]:
                right_dist = i - x
                break
        # if it hits an edge without encountering a tree >= to its height
        if right_dist == 0:
            right_dist = len(rows) - 1 # stops counting current tree
            right_dist -= x # distance to edge   
        return up_dist * down_dist * left_dist * right_dist
    
    # goes through all trees and calculates a scenic
    i:int
    for i in range(len(trees)):
        j:int
        for j in range(len(trees)):
            scenic[i][j] = scenic_score(trees, i, j)
    
    print(scenic)
    max_scenic = int(np.amax(scenic))
    print(max_scenic)
    copy_ans(max_scenic)

soln_2()