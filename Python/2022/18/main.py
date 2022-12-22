import sys
sys.path.append("../")
from advent_io import *

# type hinting
from typing import Union
from numbers import Number

# math
import math

# imports collections
import collections

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

# imports caching function for recursion
from functools import cache, lru_cache

# imports itertools
import itertools as it

# imports deepcopy function
from copy import deepcopy

fetch_input(18, 2022)

def soln_1():
    # parses input
    with open("input.txt", 'r') as file:
        # raw file
        raw:str = file.read().rstrip()
        # cube center string representation
        raw:list = raw.split('\n')
        # turns them into tuples
        cube_centers:list = [tuple([int(val) for val in line.split(',')]) for line in raw]
        
    # finds surface area
    """
    We can draw a unique point at the center of every unique face.
    Using crystal notation, and shifting so one center face point
    is the origin, we can use vectors to point to represent every
    unique face.

    By tracking which center point is not repeated, and then counting
    the number of center points not repeated, we can find the surface
    area
    """
    # points not yet repeated
    unrepeated:set = set()
    # points repeated
    repeated:set = set()

    for center in cube_centers:
        for i in range(3):
            # we go by 1/2 because the center is 1/2 distance from everything,
            # anything else would miscount
            for num in {-1/2, 1/2}:
                vector:list = list(center)
                vector[i] = center[i] + num
                vector:tuple = tuple(vector)
                if vector in repeated:
                    continue
                elif vector in unrepeated:
                    unrepeated.remove(vector)
                    repeated.add(vector)
                else:
                    unrepeated.add(vector)
    
    surface_area:int = len(unrepeated)
    print(surface_area)
    copy_ans(surface_area)

soln_1()