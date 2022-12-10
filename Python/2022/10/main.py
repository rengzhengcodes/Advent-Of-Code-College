import sys
sys.path.append("../../")
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

fetch_input(10, 2022)

def soln_1():
    # parses input
    with open("input.txt", 'r') as file:
        # raw file
        raw:str = file.read().rstrip()
        instructions = raw.split('\n')
        instructions = [tuple(instruction.split(' ')) for instruction in instructions]
    
    # 1-indexed cycles, not 0-indexed. "During" keyword makes it one indexed.
    cycle:int = 1
    # x register
    x:int = 1
    # the answer output
    ans:int = 0
    
    # checks to see if its one of the cycles where we collect data
    def cycle_check(cycle:int) -> bool:
        """
        Inputs a cycle. Checks to see if it's one of the cycles where we collect data.
        """

        return cycle == 20 or cycle == 60 or cycle == 100 or cycle == 140 or cycle == 180 or cycle == 220

    for instruction in instructions:
        match(instruction[0]):
            case 'noop':
                # noop doesn't do anything cycle 1
                cycle += 1

            case 'addx':
                cycle += 1

                # first cycle done, addx doesn't take effect
                if cycle_check(cycle):
                    ans += cycle * x

                # second cycle done, addx takes effect
                cycle += 1
                x += int(instruction[1])

        if cycle_check(cycle):
            ans += cycle * x

    print(ans)
    copy_ans(ans)

soln_1()

def soln_2():
    # parses input
    with open("input.txt", 'r') as file:
        # raw file
        raw:str = file.read().rstrip()
        instructions = raw.split('\n')
        instructions = [tuple(instruction.split(' ')) for instruction in instructions]
    
    # 1-indexed cycles, not 0-indexed
    cycle:int = 1
    # x register
    x:int = 1
    # crt screen
    crt = np.zeros((6, 40))

    def crt_check(cycle:int, x:int, crt = crt) -> bool:
        # cycles are 1-indexed, CRT is 0-indexed
        cycle -= 1
        # calculates vertical and horizontal CRT position off of cycle
        vertical = cycle // len(crt[0])
        horizontal = cycle % len(crt[0])
        # if horizontal encapsulates x-1, x, or x+1, draw a dot.
        if x - 1 <= horizontal <= x + 1:
            crt[vertical][horizontal] = 1

    for instruction in instructions:
        match(instruction[0]):
            case 'noop':
                crt_check(cycle, x)
                cycle += 1
            case 'addx':
                crt_check(cycle, x)
                cycle += 1
                crt_check(cycle, x)
                cycle += 1
                x += int(instruction[1])

    # builds string from crt
    output:str = ""
    for row in crt:
        for val in row:
            if val == 1:
                output += '#'
            else:
                output += '.'
        
        output += '\n'
    print(output)

soln_2()