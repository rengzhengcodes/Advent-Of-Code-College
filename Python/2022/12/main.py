import sys
sys.path.append("../")
from advent_io import *

# type hinting
from typing import Union
from numbers import Number
# imports iterable type for type hinting
from collections.abc import Iterable

# imports a stack-like object
from collections import deque

# import pandas and StringIO to feed data into pandas
from io import StringIO
import pandas as pd
import regex as re

# imports numpy for np.ndarray abuse
import numpy as np

# imports sleep in case we want to do step-by-step prints
from time import sleep

# imports add for map
from operator import add

# imports dedent to removes indent from multiline strings
from textwrap import dedent

fetch_input(12, 2022)

def soln_1():
    # parses input
    with open("input.txt", 'r') as file:
        # raw file
        raw:str = file.read().rstrip()
        # turns it into a list of list of chars
        raw:list[list[str]] = [list(string) for string in raw.split('\n')]
        # turns it into elevation map by turning to ascii then 0-indexing to a
        raw = [[ord(char) - 97 for char in row] for row in raw]
        # converts raw to np.ndarray because numpy has built-in methods for locating
        terrain:np.ndarray = np.array(raw)

    # finds E in map
    E_val:int = ord('E') - 97
    location_end:tuple = tuple(np.where(terrain == E_val))
    # sets end to z level
    terrain[(location_end[0], location_end[1])] = ord('z') - 97

    # finds S in map
    S_val:int = ord('S') - 97
    location_start:tuple = tuple(np.where(terrain == S_val))
    # sets start to a level
    terrain[(location_start[0], location_start[1])] = ord('a') - 97

    # set of orthogonal directions representing movement options
    directions = (
        np.array((0, 1)),
        np.array((0, -1)),
        np.array((1, 0)),
        np.array((-1, 0)))

    # Runs cellular automata to find the steps needed to reach the end
    cells:np.ndarray = np.zeros(terrain.shape, dtype=int)
    # cells to negative as you can't take negative steps
    cells -= np.ones(terrain.shape, dtype = int)
    
    # seeds the cell
    cells[location_start] = 0

    # runs the cellular automata simulation
    # if no cell has reached the end yet, continue
    step = 0
    while (cells[location_end] < 0):
        # optimization to ensure you only grab head value to not repeat calculations
        step += 1
        # iterates over rows
        for i in range(len(cells)):
            # iterates over cols
            for j in range(len(cells[0])):
                # runs only if a virtual step has reached here
                locale = np.array((i, j))
                
                # runs only if it's the head (aka not calculated before)
                if cells[tuple(locale)] == (step - 1):
                    # could use steps - 1, but i think this is less expensive than that versus utilization
                    cell_val = cells[tuple(locale)]
                    
                    # heads in all directions
                    for direction in directions:
                        # gets movement direction location
                        new_tile_locale = np.add(locale, direction)

                        # prevents wrap around or out of index
                        if new_tile_locale[0] < 0 or new_tile_locale[0] >= terrain.shape[0]:
                            continue
                        elif new_tile_locale[1] < 0 or new_tile_locale[1] >= terrain.shape[1]:
                            continue
                        
                        # for readability
                        new_tile_steps_val = cells[tuple(new_tile_locale)]
                        
                        # checks we are going up at most 1
                        if (terrain[tuple(new_tile_locale)] - terrain[tuple(locale)]) <= 1:
                            # checks we're only overwriting more steps or unstepped locales
                            # second part of or unnecessary since we always go by biggest value, but there because im pretty sure python short circuits
                            if new_tile_steps_val < 0 or new_tile_steps_val > cell_val:
                                cells[tuple(new_tile_locale)] = cell_val + 1

    steps:int = int(cells[location_end][0])
    print(steps)
    copy_ans(steps)

# soln_1()

def soln_2():
    # parses input
    with open("input.txt", 'r') as file:
        # raw file
        raw:str = file.read().rstrip()
        # turns it into a list of list of chars
        raw:list[list[str]] = [list(string) for string in raw.split('\n')]
        # turns it into elevation map by turning to ascii then 0-indexing to a
        raw = [[ord(char) - 97 for char in row] for row in raw]
        terrain:np.ndarray = np.array(raw)

    # finds E in map
    E_val:int = ord('E') - 97
    location_end:tuple = tuple(np.where(terrain == E_val))
    # sets end to z level
    terrain[(location_end[0], location_end[1])] = ord('z') - 97

    # finds S in map
    S_val:int = ord('S') - 97
    location_start:tuple = tuple(np.where(terrain == S_val))
    # sets start to a level
    terrain[(location_start[0], location_start[1])] = ord('a') - 97

    # set of orthogonal directions representing movement options
    directions = (
        np.array((0, 1)),
        np.array((0, -1)),
        np.array((1, 0)),
        np.array((-1, 0))
    )

    # Runs cellular automata to find the steps needed to reach the end
    cells:np.ndarray = np.zeros(terrain.shape, dtype=int)
    # cells to negative as you can't take negative steps
    cells -= np.ones(terrain.shape, dtype = int)
    
    ## seeds the cell
    # iterates over rows
    for i in range(terrain.shape[0]):
        # iterates over cols
        for j in range(terrain.shape[1]):
            # only seeds terrain = 'a'
            if terrain[(i, j)] == 0:
                cells[(i, j)] = 0

    # runs the cellular automata simulation
    # if no cell has reached the end yet, continue
    step = 0
    while (cells[location_end] < 0):
        # optimization to ensure you only grab head value to not repeat calculations
        step += 1
        # iterates over rows
        for i in range(cells.shape[0]):
            # iterates over cols
            for j in range(cells.shape[1]):
                # runs only if a virtual step has reached here
                locale = np.array((i, j))

                # only checks greatest values, not calculated
                if cells[tuple(locale)] == (step - 1):
                    # could use steps - 1, still think it's less hard on the CPU to store
                    cell_val = cells[tuple(locale)]

                    # goes in all possible movement directions
                    for direction in directions:
                        # gets the location of the tile movement
                        new_tile_locale = np.add(locale, direction)

                        # prevents wrap around or out of index
                        if new_tile_locale[0] < 0 or new_tile_locale[0] >= terrain.shape[0]:
                            continue
                        elif new_tile_locale[1] < 0 or new_tile_locale[1] >= terrain.shape[1]:
                            continue
                        
                        # for readability
                        new_tile_steps_val = cells[tuple(new_tile_locale)]
                        
                        # checks we are going up at most 1
                        if (terrain[tuple(new_tile_locale)] - terrain[tuple(locale)]) <= 1:
                            # checks we're only overwriting more steps or unstepped locales
                            # second or i think is still uneccessary as you're either overwriting the same value or a lower one, the latter which is covered by first check 
                            # still there for safety
                            if new_tile_steps_val < 0 or new_tile_steps_val > cell_val:
                                cells[tuple(new_tile_locale)] = step

    steps:int = int(cells[location_end][0])
    print(steps)
    copy_ans(steps)

soln_2()