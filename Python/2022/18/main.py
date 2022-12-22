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

# soln_1()

def soln_2():
    # parses input
    with open("example.txt", 'r') as file:
        # raw file
        raw:str = file.read().rstrip()
        # cube center string representation
        raw:list = raw.split('\n')
        # turns them into tuples
        cube_centers:set = set([tuple([int(val) for val in line.split(',')]) for line in raw])

    # defines surfaces
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
            # anything else would miscount. Float safe as power of 2
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
    
    # renames unrepeated
    surfaces:set = unrepeated

    # creates bounding box for space
    x_coords:list = list()
    y_coords:list = list()
    z_coords:list = list()
    
    for cube in cube_centers:
        x_coords.append(cube[0])
        y_coords.append(cube[1])
        z_coords.append(cube[2])

    # coords are all positive numbers so lower_bounds is just origin. ALSO! It means it's unoccupied
    lower_bounds:tuple = (0, 0, 0)
    upper_bounds:tuple = (max(x_coords) + 1, max(y_coords) + 1, max(z_coords) + 1)

    del x_coords, y_coords, z_coords

    # cellular automata to find touchable surfaces
    visited:set = set()
    touched:set = set()
    def water_flow(
        position:tuple, lower_bounds:tuple = lower_bounds, surfaces:set=surfaces,
        upper_bounds:tuple=upper_bounds, visited:set=visited, 
        touched:set=touched
    ):
        """
        Finds surfaces touched if we put the lava droplet in water
        
        position:tuple
            current cube position
        lower_bounds:tuple
            Lower bounds of box, inclusive
        upper_bounds:tuple
            Upper bounds of box, inclusive
        visited:set
            Locations already assumed by cell
        touched:set
            Tracks all faces we touch
        """
        # notes we've been here
        visited.add(position)

        # checks if this cell touches any surface of cube
        for i in range(3):
            # we go by 1/2 because the center is 1/2 distance from everything,
            # anything else would miscount. Float safe as power of 2
            for num in {-1/2, 1/2}:
                vector:list = list(position)
                vector[i] += num
                vector:tuple = tuple(vector)
                # adds to touched if we touch a surface
                if vector in surfaces:
                    touched.add(vector)

        # recursively calls to go to surrounding cells
        for i in range(3):
            for num in {-1, 1}:
                modified_coord:int = position[i] + num
                # if not in bounds, continue
                if not (lower_bounds[i] <= modified_coord <= upper_bounds[i]):
                    continue

                # else, calculate new coordinate
                vector:list = list(position)
                vector[i] = modified_coord
                vector:tuple = tuple(vector)

                # if new coordinate has been visited or is solid, continue
                if vector in cube_centers or vector in visited:
                    continue

                # repeat for new coord
                water_flow(vector)

    water_flow((0, 0, 0))
    
    touched_surface_area:int = len(touched)
    print(touched_surface_area)
    copy_ans(touched_surface_area)

soln_2()