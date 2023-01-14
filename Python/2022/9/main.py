import sys
sys.path.append("../")
from advent_io import *

# type hinting
from typing import Union
from numbers import Number
# imports iterable type
from collections.abc import Iterable
# imports a stack-like object
from collections import deque
# import pandas and StringIO to feed data into pandas
from io import StringIO
from time import sleep
import numpy as np
import pandas as pd
import regex as re
# imports add for map
from operator import add

fetch_input(9, 2022)

def soln_1():
    # parses input
    with open("input.txt", 'r') as file:
        # raw file
        raw:str = file.read().rstrip()
        # splits raw into instruction subsets
        instructions = raw.split('\n')
        # separates instruction components and ints second char of instruction
        instructions = [(direction, int(amount)) for direction, amount in [instruction.split(' ') for instruction in instructions]]

    # defines starting positions
    positions:dict = {
        'head': np.array([0, 0]),
        'tail': np.array([0, 0])
    }

    # turns U, R, D, L into actual directions
    directions:dict = {
        'U': np.array((0, 1)),
        'R': np.array((1, 0)),
        'D': np.array((0, -1)),
        'L': np.array((-1, 0))
    }

    # the map of locations we've visited
    move_map:dict = dict()
    # marks initial starting position in move_map
    move_map[tuple(positions['tail'])] = 1

    def adjacent(pos1:Iterable, pos2:Iterable) -> bool:
        """
        Calculates if something is adjacent with something else. Adjacency means 1 or less away on orthogonal directions.
        pos1:Iterable
            The first position
        pos2:Iterable
            The second position
        """
        adjacent = True
        for i in range(len(pos1)):
            if abs(pos1[i] - pos2[i]) > 1:
                adjacent = False
                return adjacent
        
        return adjacent

    def move_rope(instruction:tuple, rope:dict = positions, instruction_set:dict = directions, move_map:dict = move_map) -> None:
        """
        Changes the rope position based on the instruction tuple passed in and the way we're supposed to interpret the instruction set
        rope:dict
            Head and tail position
        instruction:tuple
            The instruction being passed in
        instruction_set:dict
            The correspondance of an instruction with a direction
        move_map:dict
            The places we've visited, stored as location: bool pairs
        """
        # gets the direction the head is moving
        direction = instruction_set[instruction[0]]

        # moves step by step
        for i in range(instruction[1]):
            rope['head'] += direction

            # checks to see if adjacent, if not moves rope tail moves closer to head by missing value
            if not adjacent(rope['head'], rope['tail']):
                rope['tail'] += np.sign(rope['head'] - rope['tail'])
                # notes new tail position has been visited
                move_map[tuple(rope['tail'])] = 1
            
    for instruction in instructions:
        move_rope(instruction)    

    total_spots = sum(move_map.values())
    print(total_spots)
    copy_ans(total_spots)

soln_1()

def soln_2():
    # parses input
    with open("input.txt", 'r') as file:
        # raw file
        raw:str = file.read().rstrip()
        # splits raw into instruction subsets
        instructions = raw.split('\n')
        # separates instruction components and ints second char of instruction
        instructions = [(direction, int(amount)) for direction, amount in [instruction.split(' ') for instruction in instructions]]

    # defines starting positions
    positions:dict = {
        'head': np.array([0, 0]),
        '1': np.array([0, 0]),
        '2': np.array([0, 0]),
        '3': np.array([0, 0]),
        '4': np.array([0, 0]),
        '5': np.array([0, 0]),
        '6': np.array([0, 0]),
        '7': np.array([0, 0]),
        '8': np.array([0, 0]),
        'tail': np.array([0, 0])
    }

    # turns U, R, D, L into actual directions
    directions:dict = {
        'U': np.array((0, 1)),
        'R': np.array((1, 0)),
        'D': np.array((0, -1)),
        'L': np.array((-1, 0))
    }

    # the map of locations we've visited
    move_map:dict = dict()
    # marks initial starting position in move_map
    move_map[tuple(positions['tail'])] = 1

    def adjacent(pos1:Iterable, pos2:Iterable) -> bool:
        """
        Calculates if something is adjacent with something else. Adjacency means 1 or less away on orthogonal directions.
        pos1:Iterable
            The first position
        pos2:Iterable
            The second position
        """
        adjacent = True
        for i in range(len(pos1)):
            if abs(pos1[i] - pos2[i]) > 1:
                adjacent = False
                return adjacent
        
        return adjacent

    def move_rope(instruction:tuple, rope:dict = positions, instruction_set:dict = directions, move_map:dict = move_map) -> None:
        """
        Changes the rope position based on the instruction tuple passed in and the way we're supposed to interpret the instruction set
        rope:dict
            Head and tail position
        instruction:tuple
            The instruction being passed in
        instruction_set:dict
            The correspondance of an instruction with a direction
        move_map:dict
            The places we've visited, stored as location: bool pairs
        """
        # gets the direction the head is moving
        direction = instruction_set[instruction[0]]
        # parts of the rope
        rope_parts = list(rope.keys())

        # moves step by step
        for i in range(instruction[1]):
            rope['head'] += direction

            for j in range(len(rope_parts) - 1):
                # checks to see if adjacent, if not moves rope tail moves closer to head by missing value
                if not adjacent(rope[rope_parts[j]], rope[rope_parts[j + 1]]):
                    rope[rope_parts[j + 1]] += np.sign(rope[rope_parts[j]] - rope[rope_parts[j + 1]])
            
            # notes new tail position has been visited
            move_map[tuple(rope['tail'])] = 1
            
    for instruction in instructions:
        move_rope(instruction)    

    total_spots = sum(move_map.values())
    print(total_spots)
    copy_ans(total_spots)

soln_2()