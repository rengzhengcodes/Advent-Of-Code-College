import sys
sys.path.append("../")
from advent_io import *

# type hinting
from typing import Union
from numbers import Number

# math
from math import *

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
    with open("example.txt", 'r') as file:
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
            # cost in np.uint 16, 5 bits per building resource.
            blueprints[np.uint8(blueprintID)] = (
                # ore robot cost
                (ore_ore_cost, 0, 0),
                # clay robot cost
                (clay_ore_cost, 0, 0),
                # obsidian robot cost
                (obsidian_ore_cost, obsidian_clay_cost, 0),
                # geode robot cost
                (geode_ore_cost, 0, geode_obsidian_cost),
                # max resource/turn needed for each resource
                (
                    max((ore_ore_cost, clay_ore_cost, obsidian_ore_cost, geode_ore_cost)),
                    obsidian_clay_cost,
                    geode_obsidian_cost
                )
            )

        print(blueprints)

        @cache
        def find_max_blueprint(
                blueprint_id:int, resources:tuple, robots:tuple, time_left:int=24
            ) -> int:
            """
            Finds the max geodes in a given time

            blueprint_id:int
                The id of the blueprint
            resources:tuple
                (ore, clay, obsidian)
            robot_count:tuple
                (ore, clay, obsidian)
            time_left:int
                Time left
            
            Returns: max geodes from this point
            """
            # end condition: times up!
            if time_left == 0:
                return 0
            elif time_left < 0:
                raise ValueError(f"time_left: {time_left}")
            
            # tracks max branch gain
            max_EV:int = 0
            # vectorizes resources
            resources:np.ndarray = np.array(resources)
            # makes sure resources are nonnegative
            assert (resources >= 0).all()
            # calculates gain per turn until next robot
            gain:np.ndarray = np.array(robots)
            
            # gets blueprint out
            blueprint:tuple = blueprints[blueprint_id]

            # goes through all robot in tuple
            for i in range(4):
                # if producing the max amount we can use per turn, don't need more of this robot
                if i != 3 and blueprint[-1][i] <= robots[i]:
                    continue
                # vectorizes current robot cost
                robot_cost:np.ndarray = np.array(blueprint[i])
                # net resources if we build a robot
                net:np.ndarray = resources - robot_cost
                # only calculates negative values
                np.clip(net, a_min=None, a_max=0)
                # checks if we produce all resources for this robot
                if np.logical_and(robot_cost.astype(bool), ~gain.astype(bool)[0:3]).any():
                    continue
                # calculates the turns to build the robot with negative net values
                for j in range(len(net)):
                    if net[j] >= 0:
                        net[j] = 0
                    else:
                        assert gain[j] != 0 and net[j] < 0
                        net[j] = net[j] / gain[j]
                        # ceilings the value to calculate min terms needed
                        net[j] = ceil(net[j] * -1)
                        assert net[j] >= 0
                # calculates turns needed to get all resources AND build
                turns:int = net.max() + 1
                # if turns > turns left, 0 more geodes gotten
                if turns > time_left:
                    value:int = 0
                else:
                    # declared to save operations from a boolean check
                    value:int = 0
                    # if building a geode robot, credit immediately to not store
                    if i == 3:
                        # -1 on top of build turn because 1 more turn to get first geode
                        value += max(0, time_left - turns)
                        new_robots:tuple = robots     
                    # else store robot count
                    else:
                        # robots after build
                        new_robots:list = list(robots)
                        new_robots[i] += 1
                        new_robots:tuple = tuple(new_robots)
                    
                    value += find_max_blueprint(
                        blueprint_id, tuple(resources + gain * turns - robot_cost), 
                        new_robots, time_left - turns
                    )          
                
                if value > max_EV:
                    max_EV = value
            
            # returns max subbranch
            return max_EV
        
        max_geodes:int = find_max_blueprint(1, (0, 0, 0), (1, 0, 0))
        print(max_geodes)

soln_1()