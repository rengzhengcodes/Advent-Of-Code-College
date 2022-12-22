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
                # creates new vector object for surface position
                vector:list = list(center)
                # finds surface by offsetting from center
                vector[i] += num
                # tuples vector so can be added to set
                vector:tuple = tuple(vector)

                # checks if it's in repeated, if it is, it's already an unexposed
                # edge so skip
                if vector in repeated:
                    continue
                # if it's in unrepeated, it's actually repeated so move to repeated
                elif vector in unrepeated:
                    unrepeated.remove(vector)
                    repeated.add(vector)
                # if it's new (at least to us), add to unrepeated
                else:
                    unrepeated.add(vector)
    
    surface_area:int = len(unrepeated)
    print(surface_area)
    copy_ans(surface_area)

# soln_1()

def soln_2():
    # parses input
    with open("input.txt", 'r') as file:
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
                # creates a list from center, copies values
                vector:list = list(center)
                # modifies list to get surface vector
                vector[i] += num
                # tuples surface vector so it's addable to a set
                vector:tuple = tuple(vector)

                # if vector is already established to be repeated, continue
                if vector in repeated:
                    continue
                # if vector is in unrepeated, it's actually repeated, move
                # to repeated
                elif vector in unrepeated:
                    unrepeated.remove(vector)
                    repeated.add(vector)
                # if it's new to us, add to unrepeated
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

    # axes where NO lava is (highest and lowest), allowing us to make a "container"
    # big enough for water to flow around it
    lower_bounds:tuple = (min(x_coords) - 1, min(y_coords) - 1, min(z_coords) - 1)
    upper_bounds:tuple = (max(x_coords) + 1, max(y_coords) + 1, max(z_coords) + 1)

    del x_coords, y_coords, z_coords

    # cellular automata to find touchable surfaces
    def water_flow(
        start:tuple, lower_bounds:tuple = lower_bounds, 
        surfaces:set=surfaces, upper_bounds:tuple=upper_bounds
    ) -> int:
        """
        Finds surfaces touched if we put the lava droplet in water
        
        start:tuple
            starting cube position
        lower_bounds:tuple
            Lower bounds of box, inclusive
        upper_bounds:tuple
            Upper bounds of box, inclusive
        cube_centers:tuple
            Cube centers.
        touched:set
            Tracks all faces we touch
        
        Returns:
            Number of touched surfaces.
        """
        # active positions
        active = set()
        active.add(start)

        # visited positions
        visited:set = set()
        visited |= cube_centers

        # touched surfaces
        touched:set = set()

        while len(active) > 0:
            # gets an active position and removes from active
            position = active.pop()
            # notes we've been here, and block off the droplet itself
            visited.add(position)

            # checks if this cell touches any surface of cube
            for i in range(3):
                # we go by 1/2 because the center is 1/2 distance from everything,
                # anything else would miscount. Float safe as power of 2
                for num in {-1/2, 1/2}:
                    # creates vector, copied from current position values
                    vector:list = list(position)
                    # modifies vector to get surface
                    vector[i] += num
                    # makes surface hashable by tupleifying
                    vector:tuple = tuple(vector)

                    # adds to touched if we touch a surface
                    if vector in surfaces:
                        touched.add(vector)

            # calculates valid surrounding cells to flow to
            for i in range(3):
                for num in {-1, 1}:
                    # modifying the one coord value in question for orthogonal movement
                    modified_coord:int = position[i] + num

                    # if not in bounds/container, continue, disregard point
                    if not (lower_bounds[i] <= modified_coord <= upper_bounds[i]):
                        continue

                    # else, calculate new coordinate and make hashable by tupleifying
                    vector:list = list(position)
                    vector[i] = modified_coord
                    vector:tuple = tuple(vector)

                    # if new coordinate has been visited or is solid, continue
                    if vector in visited:
                        continue

                    # adds valid cell to active
                    active.add(vector)
        
        return len(touched)
    
    touched_surface_area:int = water_flow((0, 0, 0))
    print(touched_surface_area)
    copy_ans(touched_surface_area)

soln_2()