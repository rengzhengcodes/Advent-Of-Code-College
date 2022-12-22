"""
NOTICE:

The solve function for part 2 works, but assumes all inputs are unique. 
You simply have to add a check to see that the solve function does not return 
None so it doesn't keep swapping two identical values. This is easily done, but
was neglected for speedcoding + code speed running purposes. It was not inserted
later as the input does not require it and I currently cannot do the proper tests
myself in case my implementation is somehow messy. 
"""


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
    
    def solve(left:list, right:list) -> bool:
        """
        Determines whether or not left is in order relative to right

        left:list
            First signal in pair
        right:list
            Second signal in pair
        """
        
        ## blank checks
        # left length is 0, right > 0
        if left is None and right is not None:
            return True
        # left and right length == 0
        elif left is None and right is None:
            return None
        # left length > 0, right == 0
        elif left is not None and right is None:
            return False
        
        # goes through all elements of signal
        for i in range(len(left)):
            # if right runs out of elements first, it's not correct
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

        index += 1
    
    print(index_sum)
    copy_ans(index_sum)

# soln_1()

def soln_2():
    # parses input
    with open("input.txt", 'r') as file:
        # raw file
        raw:str = file.read().rstrip()
        # replaces spaces, puts them all in 1 block
        signals_raw:list[str] = raw.replace("\n\n", '\n')
        # splits into signals list
        signals:list = list(signals_raw.split('\n'))
        # evaluates each signal
        signals = [literal_eval(signal) for signal in signals]

    # appends distress signal packets
    signals.append([[2]])
    signals.append([[6]])
    
    def solve(left:list, right:list) -> bool:
        """
        Determines whether or not left is in order relative to right

        left:list
            First signal in pair
        right:list
            Second signal in pair
        """
        
        ## blank checks
        # left length is 0, right > 0
        if left is None and right is not None:
            return True
        # left and right length == 0
        elif left is None and right is None:
            return None
        # left length > 0, right == 0
        elif left is not None and right is None:
            return False
        
        # goes through all elements of signal
        for i in range(len(left)):
            # if right runs out of elements first, it's not correct
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
   
    # sorts the signals + distress packets, bubblesort style
    swapped = True
    while swapped:
        swapped = False
        for i in range(len(signals) - 1):
            if not solve(signals[i], signals[i+1]):
                # swap the two
                signals[i], signals[i + 1] = signals[i + 1], signals[i]
                # continue swapping
                swapped = True
    
    # finds dividers
    dividers:list = list()

    for i in range(len(signals)):
        signal = signals[i]
        # describes decoder
        if signal == [[2]] or signal == [[6]]:
            dividers.append(i + 1)
    
    # multiplies dividers
    decoder_key:int = int(np.prod(dividers, dtype=int))

    print(decoder_key)
    copy_ans(decoder_key)

soln_2()