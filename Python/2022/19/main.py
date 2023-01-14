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
            # cost in np.uint 16, 5 bits per building resource.
            blueprints[blueprintID] = (
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

    # ids for all robots
    ORE:int = 0
    CLAY:int = 1
    OBSI:int = 2
    GEODE:int = 3

    """
    keeps track of the maximum branch value so far
    
    OF STRUCTURE MAX_BRANCH[id]

    optimization from: https://www.reddit.com/r/adventofcode/comments/zpihwi/comment/j0tls7a/
    """
    max_branch:dict = dict()

    @cache
    def find_max_blueprint(
            blueprint_id:int, resources:tuple, robots:tuple, current_value:int, time_left:int=24
        ) -> int:
        """
        Finds the max geodes in a given time

        blueprint_id:int
            The id of the blueprint
        resources:tuple
            (ore, clay, obsidian)
        robot_count:tuple
            (ore, clay, obsidian)
        current_value:int
            Guaranteed value of this branch
        time_left:int
            Time left
        
        Returns: max geodes from this point
        """
        # end condition: times up! (Or it's 1 and nothing done matters)
        # end condition: best possible Geode gain is worst than best current branch
        if time_left <= 1 or time_left * (time_left - 1) / 2 + current_value <= max_branch[id]:
            return 0
        # tracks max branch gain
        max_EV:int = 0
        
        # gets blueprint out
        blueprint:tuple = blueprints[blueprint_id]

        # goes through all robot in tuple
        for robot in range(4):
            # optimization from https://www.reddit.com/r/adventofcode/comments/zpy5rm/2022_day_19_what_are_your_insights_and/
            # essentially, a robot must be able to pay itself off
            if robot != GEODE and robots[robot] * time_left + resources[robot] >= time_left * blueprint[-1][robot]:
                continue

            # pulls out current robot cost
            robot_cost:tuple = blueprint[robot]
            # calculates turns to get all resources
            turns:int = 0
            cant_make:bool = False
            for i in range(len(robots)):
                # checks if we produce all resources for this robot
                if robot_cost[i] and not robots[i]:
                    cant_make = True
                    break
                # checks if costs more than we have, and div by 0 check
                if robot_cost[i] > resources[i] and robots[i] != 0:
                    # calculates turns it takes if we need to produce
                    temp:int = ceil(-1 * (resources[i] - robot_cost[i]) / robots[i])
                    # replaces turns needed if turns needed for this resource is greater than the others
                    if temp > turns:
                        turns = temp
            if cant_make:
                continue
            # accounts for build time
            turns += 1
            
            # declared to save operations from a boolean check
            value:int = 0
            # if turns >= turns left, 0 more geodes gotten
            if turns < time_left:
                # if building a geode robot, credit immediately to not store Geode robot population
                if robot == GEODE:
                    value += time_left - turns
                    new_robots:tuple = robots     
                # else store robot count
                else:
                    # robots after build
                    new_robots:list = list(robots)
                    new_robots[robot] += 1
                    new_robots:tuple = tuple(new_robots)
                
                value += find_max_blueprint(
                    blueprint_id, tuple([resources[i] - robot_cost[i] + (robots[i] * turns) for i in range(3)]), 
                    new_robots, value + current_value, time_left - turns
                )          
            
            if value > max_EV:
                max_EV = value
        
        # if we have improvement on max_branch, replace max_branch, else kill branch
        if max_EV + current_value > max_branch[id]:
            # returns max subbranch
            max_branch[id] = max_EV + current_value
        
        return max_EV
    
    total_quality:int = 0
    for id in blueprints:
        # prevents keyerror
        max_branch[id] = 0
        # calculation
        max_geodes:int = find_max_blueprint(id, (0, 0, 0), (1, 0, 0), 0)
        quality_level:int = max_geodes * id
        total_quality += quality_level
    
    print(total_quality)
    copy_ans(int(total_quality))

soln_1()

def soln_2():
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
            # cost in np.uint 16, 5 bits per building resource.
            blueprints[blueprintID] = (
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

    # ids for all robots
    ORE:int = 0
    CLAY:int = 1
    OBSI:int = 2
    GEODE:int = 3

    """
    keeps track of the maximum branch value so far
    
    OF STRUCTURE MAX_BRANCH[id]

    optimization from: https://www.reddit.com/r/adventofcode/comments/zpihwi/comment/j0tls7a/
    """
    max_branch:dict = dict()

    def encode(data:tuple[int]) -> np.uint64:
        """
        Enocdes a tuple of form (ORE, CLAY, OBSI) into one np.uint32 in 10 bit increments with 2 leading 0s
        
        data:tuple[int]
            The data to be encoded in ORE, CLAY, OBSI order.
        
        return: np.uint32
            np.uint32 encoding the data in OBSI_CLAY_ORE order
        """
        answer:np.uint32 = np.uint32(0)
        offset:int = 0
        for resource in data:
            answer = answer | (resource << (10 * offset))
            offset += 1
        return answer
            
    def decode(data:np.uint32, resource:int) -> np.uint32:
        """
        Decodes the data from encode based on fixed resource type. Encode expected of form (ORE, CLAY, OBSI)

        data:np.uint32
            The data bitstring.
        resource:int
            The number corresponding to resource
        
        return: np.uint32
            Prevents errors in bitshifts for reencode options
        """
        assert resource in range(3)

        return (data & (0x3FF << (resource * 10))) >> (resource * 10)

    @cache
    def find_max_blueprint(
            blueprint_id:int, resources:np.uint32, robots:np.uint32, current_value:int, time_left:int=32
        ) -> int:
        """
        Finds the max geodes in a given time

        blueprint_id:int
            The id of the blueprint
        resources:np.uint32
            (ore, clay, obsidian)
        robot_count:np.uint32
            (ore, clay, obsidian)
        current_value:int
            Guaranteed value of this branch
        time_left:int
            Time left
        
        Returns: max geodes from this point
        """
        resources:tuple = tuple([decode(resources, resource) for resource in range(3)])
        robots:tuple = tuple([decode(robots, resource) for resource in range(3)])

        # end condition: times up! (Or it's 1 and nothing done matters)
        # end condition: best possible Geode gain is worst than best current branch
        if time_left <= 1 or time_left * (time_left - 1) / 2 + current_value <= max_branch[id]:
            return 0
        # tracks max branch gain
        max_EV:int = 0
        
        # gets blueprint out
        blueprint:tuple = blueprints[blueprint_id]

        # goes through all robot in tuple
        for robot in range(4):
            # optimization from https://www.reddit.com/r/adventofcode/comments/zpy5rm/2022_day_19_what_are_your_insights_and/
            # essentially, a robot must be able to pay itself off
            if robot != GEODE and robots[robot] * time_left + resources[robot] >= time_left * blueprint[-1][robot]:
                continue

            # pulls out current robot cost
            robot_cost:tuple = blueprint[robot]
            # calculates turns to get all resources
            turns:int = 0
            cant_make:bool = False
            for i in range(len(robots)):
                # checks if we produce all resources for this robot
                if robot_cost[i] and not robots[i]:
                    cant_make = True
                    break
                # checks if costs more than we have, and div by 0 check
                if robot_cost[i] > resources[i] and robots[i] != 0:
                    # calculates turns it takes if we need to produce
                    temp:int = ceil(-1 * (resources[i] - robot_cost[i]) / robots[i])
                    # replaces turns needed if turns needed for this resource is greater than the others
                    if temp > turns:
                        turns = temp
            if cant_make:
                continue
            # accounts for build time
            turns += 1
            
            # declared to save operations from a boolean check
            value:int = 0
            # if turns >= turns left, 0 more geodes gotten
            if turns < time_left:
                # if building a geode robot, credit immediately to not store Geode robot population
                if robot == GEODE:
                    value += time_left - turns
                    new_robots:tuple = robots     
                # else store robot count
                else:
                    # robots after build
                    new_robots:list = list(robots)
                    new_robots[robot] += 1
                    new_robots:tuple = tuple(new_robots)
                
                value += find_max_blueprint(
                    blueprint_id, encode(tuple([resources[i] - robot_cost[i] + (robots[i] * turns) for i in range(3)])), 
                    encode(new_robots), value + current_value, time_left - turns
                )          
            
            if value > max_EV:
                max_EV = value
        
        # if we have improvement on max_branch, replace max_branch, else kill branch
        if max_EV + current_value > max_branch[id]:
            # returns max subbranch
            max_branch[id] = max_EV + current_value
        
        return max_EV
    
    quality_product:int = 1
    for id in range(1, 4):
        # prevents keyerror
        max_branch[id] = 0
        # calculation
        max_geodes:int = find_max_blueprint(id, encode((0, 0, 0)), encode((1, 0, 0)), 0)
        quality_product *= max_geodes
        find_max_blueprint.cache_clear()
    
    print(quality_product)
    copy_ans(int(quality_product))

soln_2()