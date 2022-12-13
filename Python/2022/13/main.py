import sys
sys.path.append("../../")
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

# imports eval that is safe
from ast import literal_eval

fetch_input(13, 2022)

def soln_1():
    # parses input
    with open("input.txt", 'r') as file:
        # raw file
        raw:str = file.read().rstrip()
        # signal pairs
        signal_pairs_raw:list[str] = raw.split("\n\n")
        # splits into signal pairs in list
        signal_pairs:list = [list(signal_pair.split('\n')) for signal_pair in signal_pairs_raw]
        # evaluates each
        signal_pairs = [(literal_eval(signal0), literal_eval(signal1)) for signal0, signal1 in signal_pairs]
    
    # Parse later
    # def parse_input(input:str, holder:list) -> None:
    #     """
    #     Parses input. We can just use eval but it's more safe parsing.

    #     input:str:
    #         The input string we're parsing
    #     holder:list:
    #         The list we're mutating
    #     """
    #     # elements of the input list
    #     elements:list[str] = in

    #     for i in range(len(input)):
    #         char = input[i]
    #         match (char):
    #            # inputs sublist
    #             case '[':
    #                 sub_list = list()
    #                 holder.append(sub_list)
    #                 parse_input(input)
    #             # exits at list end
    #             case ']':
    #                 return
    #             # basecase of int
    #             case _:
    #                 holder.append(int(char))

    def solve(left:list, right:list) -> bool:
        # blank checks
        if left is None and right is not None:
            return True
        elif left is None and right is None:
            return None
        elif left is not None and right is None:
            return False
        
        for i in range(len(left)):
            # if right runs out first, it's not correct
            if i >= len(right):
                return False
            
            # both are ints case
            if isinstance(left[i], int) and isinstance(right[i], int):
                if left[i] < right[i]:
                    return True
                elif left[i] > right[i]:
                    return False
            # both are lists case
            elif isinstance(left[i], list) and isinstance(right[i], list):
                # if we reached a resolution it's in the correct order, return it, else continue
                result = solve(left[i], right[i])
                if result is not None:
                    return result
            
            # one is a list
            else:
                # list int is put into, since we must typecast the int to a list
                constructed_list:list = list()

                # left is the int
                if isinstance(left[i], int):
                    constructed_list.append(left[i])
                    result = solve(constructed_list, right[i])
                # right is a list
                else:
                    constructed_list.append(right[i])
                    result = solve(left[i], constructed_list)

                # if we reach a conclusion, return it
                if result is not None:
                    return result
        
        # left ran out first it's true
        if len(left) < len(right):
            return True
        # else, left must be equal, so inconclusive
        else:
            return None
    
    # correct pair count
    index_sum:int = 0
    # 1 indexed
    index:int = 1
    for left, right in signal_pairs:
        if solve(left, right):
            index_sum += index
            print(index)

        index += 1
    
    print(index_sum)
    copy_ans(index_sum)

soln_1()