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

fetch_input(14, 2022)

def soln_1():
    # parses input
    with open("input.txt", 'r') as file:
        # raw file
        raw:str = file.read().rstrip()
        raw = raw.split('\n')
        # extracts edge data
        edges:list = [list(line.split(' -> ')) for line in raw]
        # extracts the endpoints of each line segment of an edge
        edges = [[tuple([int(x) for x in point.split(',')]) for point in edge] for edge in edges]
        
    # constructs cave from edges
    # dictionary mapping of cave structure
    cave:dict = dict()
    
    # goes over all edges
    for edge in edges:
        # draws lines between all points in edges, starting point to ending point for each
        for i in range(len(edge) - 1):
            starting_point:tuple = edge[i]
            ending_point:tuple = edge[i + 1]

            starting_x, starting_y = starting_point
            ending_x, ending_y = ending_point
            
            # swap so iterating in right direction for range
            if starting_x > ending_x:
                starting_x, ending_x = ending_x, starting_x
            if starting_y > ending_y:
                starting_y, ending_y = ending_y, starting_y
            # goes through all x between starting and ending point
            for x in range(starting_x, ending_x + 1):
                # goes through all y between starting and ending point, lines so we don't need to worry about diagonals filling up the board
                for y in range(starting_y, ending_y + 1):
                    # point in edge
                    location:tuple = (x, y)
                    cave[location] = 0 # cave walls defined as 0
    
    # print(cave)
    ## finds the abyss, aka the height at which the lowest rock edge is and therefore defines infinity and beyond
    y_coords:list = [point[1] for edge in edges for point in edge]
    max_y:int = max(y_coords)
    del y_coords
    # point sand starts pouring in
    sand_drip:tuple = (500, 0)

    reached_abyss:bool = False
    # keeps going if not not in abyss
    while (not reached_abyss):
        # spawns sand
        sand_location:list = list(sand_drip)
        sand_live:bool = True

        while (sand_live):
            # checks if sand has made it to the abyss, if it has, quit and discard sand, it's gone
            if sand_location[1] >= max_y:
                reached_abyss = True
                break
            # checks if sand can fall straight down
            elif (sand_location[0], sand_location[1] + 1) not in cave:
                sand_location[1] += 1
            # checks left and down if cannot fall straight down
            elif (sand_location[0] - 1, sand_location[1] + 1) not in cave:
                sand_location[0] -= 1
                sand_location[1] += 1
            # checks if right and down if both checks above fail
            elif (sand_location[0] + 1, sand_location[1] + 1) not in cave:
                sand_location[0] += 1
                sand_location[1] += 1
            # if above conditions fail, sand cannot fall and becomes static
            else:
                cave[tuple(sand_location)] = 1
                sand_live = False

    num_sand:int = sum(cave.values())
    print(num_sand)
    copy_ans(num_sand)

# soln_1()

def soln_2():
    # parses input
    with open("input.txt", 'r') as file:
        # raw file
        raw:str = file.read().rstrip()
        raw = raw.split('\n')
        # extracts edge data
        edges:list = [list(line.split(' -> ')) for line in raw]
        # extracts the endpoints of each line segment of an edge
        edges = [[tuple([int(x) for x in point.split(',')]) for point in edge] for edge in edges]
        
    # constructs cave from edges
    # dictionary mapping of cave structure
    cave:dict = dict()
    
    # goes over all edges
    for edge in edges:
        # draws lines between all points in edges, starting point to ending point for each
        for i in range(len(edge) - 1):
            starting_point:tuple = edge[i]
            ending_point:tuple = edge[i + 1]

            starting_x, starting_y = starting_point
            ending_x, ending_y = ending_point
            
            # swap so iterating in right direction for range
            if starting_x > ending_x:
                starting_x, ending_x = ending_x, starting_x
            if starting_y > ending_y:
                starting_y, ending_y = ending_y, starting_y
            # goes through all x between starting and ending point
            for x in range(starting_x, ending_x + 1):
                # goes through all y between starting and ending point, lines so we don't need to worry about diagonals filling up the board
                for y in range(starting_y, ending_y + 1):
                    # point in edge
                    location:tuple = (x, y)
                    cave[location] = 0 # cave walls defined as 0
    
    # print(cave)
    ## finds the abyss, aka the height at which the lowest rock edge is and therefore defines infinity and beyond
    y_coords:list = [point[1] for edge in edges for point in edge]
    max_y:int = max(y_coords)
    del y_coords
    floor_y:int = max_y + 2
    # point sand starts pouring in
    sand_drip:tuple = (500, 0)

    # keeps going if not not in abyss
    while (sand_drip not in cave):
        # spawns sand
        sand_location:list = list(sand_drip)
        sand_live:bool = True

        while (sand_live):
            # checks if sand has made it to the floor, if so static
            if sand_location[1] + 1 == floor_y:
                cave[tuple(sand_location)] = 1
                sand_live = False
            # checks if sand can fall straight down
            elif (sand_location[0], sand_location[1] + 1) not in cave:
                sand_location[1] += 1
            # checks left and down if cannot fall straight down
            elif (sand_location[0] - 1, sand_location[1] + 1) not in cave:
                sand_location[0] -= 1
                sand_location[1] += 1
            # checks if right and down if both checks above fail
            elif (sand_location[0] + 1, sand_location[1] + 1) not in cave:
                sand_location[0] += 1
                sand_location[1] += 1
            # if above conditions fail, sand cannot fall and becomes static
            else:
                cave[tuple(sand_location)] = 1
                sand_live = False

    num_sand:int = sum(cave.values())
    print(num_sand)
    copy_ans(num_sand)

soln_2()