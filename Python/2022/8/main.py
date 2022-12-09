import sys
sys.path.append("../../")
from advent_io import *

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
        raw = file.read().rstrip()
        rows = raw.split('\n')
        rows = [list(row) for row in rows]
    
    for row in rows:
        for i in range(len(row)):
            row[i] = int(row[i])
    zeroes = [[0] * len(row) for row in rows]
    trees = np.array(rows)
    visible = np.array(zeroes)

    def check_trees_visible_up_down(trees, visible):
        for i in range(len(trees)):
            tallest_tree = -1
            for j in range(len(trees[i])):
                if tallest_tree < trees[i][j]:
                    visible[i][j] = 1
                    tallest_tree = trees[i][j]

    check_trees_visible_up_down(trees, visible)

    visible = np.rot90(visible)
    trees = np.rot90(trees)
    check_trees_visible_up_down(trees, visible)
    print(trees, visible)

    visible = np.rot90(visible)
    trees = np.rot90(trees)
    check_trees_visible_up_down(trees, visible)

    visible = np.rot90(visible)
    trees = np.rot90(trees)
    check_trees_visible_up_down(trees, visible)

    visible_trees = int(np.sum(visible))
    print(visible_trees)
    copy_ans(visible_trees)

soln_1()

def soln_2():
    pass

soln_2()