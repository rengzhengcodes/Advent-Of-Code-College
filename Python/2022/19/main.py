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
            blueprints[np.uint8(blueprintID)] = (
                # ore robot cost
                np.array((ore_ore_cost, 0, 0)),
                # clay robot cost
                np.array((clay_ore_cost, 0, 0)),
                # obsidian robot cost
                np.array((obsidian_ore_cost, obsidian_clay_cost, 0)),
                # geode robot cost
                np.array((geode_ore_cost, 0, geode_obsidian_cost)),
                # max resource/turn needed for each resource
                np.array((
                    max((ore_ore_cost, clay_ore_cost, obsidian_ore_cost, geode_ore_cost)),
                    obsidian_clay_cost,
                    geode_obsidian_cost
                ))
            )

        print(blueprints)

    # ids for all robots
    ORE:int = 0
    CLAY:int = 1
    OBSI:int = 2
    GEODE:int = 3

    def unpack_values(
        data:np.uint64, resource:np.uint8
    ) -> np.uint16:
        """
        Unpacks ore, clay, obsidian out of a uint64

        data:np.uint64
            The data in question in the format of parity_ore_clay_obsidian
        resource:np.uint8
            The resource we're trying to access
        """
        mask:np.uint64 = 0x1FFFFF
        shift:int = None
        match resource:
            case [ORE]:
                shift = 64 // 3 * 3
            case [CLAY]:
                shift = 64 // 3 * 2
            case [OBSI]:
                shift = 64 // 3 
            case _:
                raise ValueError(resource)
        
        mask = mask << shift
        return (data & mask) >> shift

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
        # end condition: times up! (Or it's 1 and nothing done matters)
        if time_left <= 1:
            assert time_left >= 0
            return 0
        
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
        for robot in range(4):
            # if producing the max amount we can use per turn, don't need more of this robot
            if robot != GEODE and blueprint[-1][robot] <= robots[robot]:
                continue

            # vectorizes current robot cost
            robot_cost:np.ndarray = blueprint[robot]
            # net resources if we build a robot
            net:np.ndarray = resources - robot_cost
            # removes positive values
            np.clip(net, a_min=None, a_max=0)
            # checks if we produce all resources for this robot
            if np.logical_and(robot_cost.astype(bool), ~gain.astype(bool)).any():
                continue
            
            # calculates the turns to build the robot with negative net values
            for resource in range(len(net)):
                if net[resource] >= 0:
                    net[resource] = 0
                else:
                    assert gain[resource] > 0 and net[resource] < 0
                    # turns to achieve net with current gain
                    time:float = net[resource] / gain[resource]
                    # ceilings the value to calculate min terms needed
                    net[resource] = ceil(time * -1)
                assert net[resource] >= 0 and isinstance(net[resource], np.int64), f"{net[resource]}"
            
            # calculates turns needed to get all resources AND build
            turns:int = net.max() + 1
            
            # if turns > turns left, 0 more geodes gotten
            if turns -1 >= time_left:
                value:int = 0
            else:
                # declared to save operations from a boolean check
                value:int = 0

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
                    blueprint_id, tuple(resources - robot_cost + (gain * turns)), 
                    new_robots, time_left - turns
                )          
            
            if value > max_EV:
                max_EV = value
        
        # returns max subbranch
        return max_EV
    
    total_quality:int = 0
    for id in blueprints:
        max_geodes:int = find_max_blueprint(id, (0, 0, 0), (1, 0, 0))
        quality_level:int = max_geodes * id
        total_quality += quality_level
    
    print(total_quality)
    copy_ans(int(total_quality))

# soln_1()

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
            blueprints[np.uint8(blueprintID)] = (
                # ore robot cost
                np.array((ore_ore_cost, 0, 0)),
                # clay robot cost
                np.array((clay_ore_cost, 0, 0)),
                # obsidian robot cost
                np.array((obsidian_ore_cost, obsidian_clay_cost, 0)),
                # geode robot cost
                np.array((geode_ore_cost, 0, geode_obsidian_cost)),
                # max resource/turn needed for each resource
                np.array((
                    max((ore_ore_cost, clay_ore_cost, obsidian_ore_cost, geode_ore_cost)),
                    obsidian_clay_cost,
                    geode_obsidian_cost
                ))
            )

        print(blueprints)

    # ids for all robots
    ORE:int = 0
    CLAY:int = 1
    OBSI:int = 2
    GEODE:int = 3

    def unpack_values(
        data:np.uint64, resource:np.uint8
    ) -> np.uint16:
        """
        Unpacks ore, clay, obsidian out of a uint64

        data:np.uint64
            The data in question in the format of parity_ore_clay_obsidian
        resource:np.uint8
            The resource we're trying to access
        """
        mask:np.uint64 = 0x1FFFFF
        shift:int = None
        match resource:
            case [ORE]:
                shift = 64 // 3 * 3
            case [CLAY]:
                shift = 64 // 3 * 2
            case [OBSI]:
                shift = 64 // 3 
            case _:
                raise ValueError(resource)
        
        mask = mask << shift
        return (data & mask) >> shift

    """
    keeps track of the maximum branch value so far
    
    OF STRUCTURE MAX_BRANCH[id]

    optimization from: https://www.reddit.com/r/adventofcode/comments/zpihwi/comment/j0tls7a/
    """
    max_branch:dict = dict()

    @cache
    def find_max_blueprint(
            blueprint_id:int, resources:tuple, robots:tuple, current_value:int, time_left:int=32
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
        if time_left <= 1:
            return 0
        # end condition: best possible Geode gain is worst than best current branch
        elif time_left * (time_left - 1) / 2 + current_value <= max_branch[id]:
            return 0
        # tracks max branch gain
        max_EV:int = 0
        # vectorizes resources
        resources:np.ndarray = np.array(resources)
        # calculates gain per turn until next robot
        gain:np.ndarray = np.array(robots)
        
        # gets blueprint out
        blueprint:tuple = blueprints[blueprint_id]

        # goes through all robot in tuple
        for robot in range(4):
            # if producing the max amount we can use per turn, don't need more of this robot
            if robot != GEODE: 
                # optimization from https://www.reddit.com/r/adventofcode/comments/zpy5rm/2022_day_19_what_are_your_insights_and/
                # essentially, a robot must be able to pay itself off
                if gain[robot] * time_left + resources[robot] >= time_left * blueprint[-1][robot]:
                    continue

            # vectorizes current robot cost
            robot_cost:np.ndarray = blueprint[robot]
            # checks if we produce all resources for this robot
            if np.logical_and(robot_cost, np.logical_not(gain)).any():
                continue
            # net resources if we build a robot
            net:np.ndarray = resources - robot_cost
            # removes positive values
            np.clip(net, a_min=None, a_max=0)
            
            # calculates the turns to build the robot with negative net values
            for resource in range(len(net)):
                if net[resource] >= 0:
                    net[resource] = 0
                else:
                    # turns to achieve net with current gain
                    time:float = net[resource] / gain[resource]
                    # ceilings the value to calculate min terms needed
                    net[resource] = ceil(time * -1)
            
            # calculates turns needed to get all resources AND build
            turns:int = net.max() + 1
            
            # if turns > turns left, 0 more geodes gotten
            if turns + 1 >= time_left:
                value:int = 0
            else:
                # declared to save operations from a boolean check
                value:int = 0

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
                    blueprint_id, tuple(resources - robot_cost + (gain * turns)), 
                    new_robots, value + current_value, time_left - turns
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
        print(id)
        # prevents keyerror
        max_branch[id] = 0
        # calculation
        max_geodes:int = find_max_blueprint(id, (0, 0, 0), (1, 0, 0), 0)
        quality_product *= max_geodes
        find_max_blueprint.cache_clear()
    
    print(quality_product)
    copy_ans(int(quality_product))

soln_2()