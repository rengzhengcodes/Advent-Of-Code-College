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

fetch_input(19, 2022)

"""
NOTES:
1. ALL robots need ORE
2. ALL obsidian-collecting robots need CLAY
3. ALL geode robots need OBSIDIAN
"""


def soln_1():
    # parses input
    with open("input.txt", 'r') as file:
        # raw file
        raw:str = file.read().rstrip()
        # blueprints
        blueprint_book:list = raw.split('\n')
        # separates the blueprint ID and the costs per robot
        blueprint_book = [[int(num) for num in re.findall(r'\d+', string)] for string in blueprint_book]
        # tracks blueprints by number
        blueprints:dict = dict()

        # assigns blueprints to dict with cost
        for (
                blueprintID, ore_ore_cost, clay_ore_cost, 
                obsidian_ore_cost, obsidian_clay_cost, 
                geode_ore_cost, geode_obsidian_cost
        ) in blueprint_book:
            # cost in (ore, clay, obsidian) format
            blueprints[np.uint8(blueprintID)] = (
                # ore robot cost
                (ore_ore_cost, 0, 0),
                # clay robot cost
                (clay_ore_cost, 0, 0),
                # obsidian robot cost
                (obsidian_ore_cost, obsidian_clay_cost, 0),
                # geode robot cost
                (geode_ore_cost, 0, geode_obsidian_cost)
            )

        @cache
        def find_max_blueprint(
                blueprint_id:int, resources:tuple, robots:tuple, time_left:int=24
            ) -> int:
            """
            Finds the max geodes in a given time

            blueprint_id:int
                The id of the blueprint
            resource_count:tuple
                (ore, clay, obsidian)
            robot_count:tuple
                (ore, clay, obsidian, geode)
            time_left:int
                Time left
            
            Returns: max geodes from this point
            """
            # end condition: times up!
            if time_left == 0:
                return 0
            
            # tracks max branch gain
            max_EV:int = 0
            # vectorizes resources
            resources:np.ndarray = np.array(resources)
            # calculates gain this turn for raw resources
            gain:np.ndarray = np.array(robots[0:3])
            
            # gets blueprint out
            blueprint:tuple = blueprints[blueprint_id]

            # goes through all robot in tuple
            for i in range(4):
                # vectorizes current robot cost
                robot_cost:np.ndarray = np.array(blueprint[i])
                # net resources if we build a robot
                net:np.ndarray = resources - robot_cost

                # checks we don't go negative
                if not (np.any(net < 0)):
                    # builds robot
                    new_robots:list = list(robots)
                    new_robots[i] += 1
                    new_robots:tuple = tuple(new_robots)

                    # builds robot, recurses, finds expected value
                    value:int = find_max_blueprint(blueprint_id, tuple(net + gain), new_robots, time_left - 1)
                    if value > max_EV:
                        max_EV = value

            # no build robot
            value:int = find_max_blueprint(blueprint_id, tuple(resources + gain), robots, time_left - 1)
            if value > max_EV:
                max_EV = value
            
            # returns max subbranch + geodes generated this branch
            return max_EV + robots[-1]
        
        max_geodes:int = find_max_blueprint(1, (0, 0, 0), (1, 0, 0, 0))
        print(max_geodes)
soln_1()