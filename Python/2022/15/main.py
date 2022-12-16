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

fetch_input(15, 2022)

def soln_1():
    # parses input
    with open("input.txt", 'r') as file:
        # raw file
        raw:str = file.read().rstrip()
        raw = raw.split('\n')
        # splits to sensor, beacon pairs
        pairs:list = [list(line.split(": ")) for line in raw]
        pairs = [[sensor.split(" at ")[1].split(", "), beacon.split(" at ")[1].split(", ")] for sensor, beacon in pairs]
        # extracts sensor and beacon into integer base pairs
        pairs = [
                    (
                        tuple([int(val.split('=')[1]) for val in sensor]),
                        tuple([int(val.split('=')[1]) for val in beacon])
                    )
                    for sensor, beacon in pairs
                ]
    
    # finds map bounds
    x_vals:list = [elem[0] for pair in pairs for elem in pair]
    y_vals:list = [elem[1] for pair in pairs for elem in pair]
    x_bounds:tuple = (min(x_vals), max(x_vals))
    y_bounds:tuple = (min(y_vals), max(y_vals))

    def calc_manhattan_dist(loc0:tuple, loc1:tuple) -> int:
        """
        Calculates the manhattan distance between 2 locations

        loc1:tuple
            Position 1
        loc2:tuple
            Position 2
        
        Returns:
        Manhattan distance
        """
        manhattan_distance:int = sum([abs(loc0[i] - loc1[i]) for i in range(len(loc0))])
        return manhattan_distance
    
    # corresponds sensor to its maximum distance given nearest beacon
    sensor_max_dist:dict = dict()
    for sensor, beacon in pairs:
        # notes distance from each sensor to closest beacon
        sensor_max_dist[sensor] = calc_manhattan_dist(sensor, beacon)
    
    y = 2000000
    # calculates number of no beacons in y=2000000
    no_beacons:int = 0
    for x in range(x_bounds[0], x_bounds[1] + 1):
        empty:bool = True
        current_location:tuple = (x, y)

        for sensor, max_dist in sensor_max_dist.items():
            if calc_manhattan_dist(sensor, current_location) <= max_dist:
                empty = False
                break
        
        if not empty:
            no_beacons += 1
    
    """
    # counts the area before the x_bound. 
    # The x_bound represents the entity object limit, 
    # so with the way things are set up we only need to
    # calculate past the bounds so long as no beacon can be there
    """
    # if it's possible for a beacon to be there
    possible:bool = False

    x = x_bounds[0] - 1
    while(not possible):
        possible = True
        current_location:tuple = (x, y)
        for sensor, max_dist in sensor_max_dist.items():
            if calc_manhattan_dist(sensor, current_location) <= max_dist:
                possible = False
                break
        
        if not possible:
            no_beacons += 1
            x -= 1
    
    """
    Counts area after the x bound for similar logic
    """
    # if it's possible for a beacon to be there
    possible:bool = False

    x = x_bounds[1] + 1
    while(not possible):
        possible = True
        current_location:tuple = (x, y)
        for sensor, max_dist in sensor_max_dist.items():
            if calc_manhattan_dist(sensor, current_location) <= max_dist:
                possible = False
                break
        
        if not possible:
            no_beacons += 1
            x += 1

    # removes beacons from full
    counted_beacons = set()
    for signal, beacon in pairs:
        if beacon not in counted_beacons and beacon[1] == y:
            counted_beacons.add(beacon)
            no_beacons -= 1

    print(no_beacons)
    copy_ans(no_beacons)

# soln_1()

def soln_2():
    """
    DISCLAIMER::::
    Checked reddit hints to solve this solution, never checked actual solution but did glean that there's only 1 possible sensor spot in the search space meant it must be at a point where the edges of 4 sensors are off by 1.
    """
    # parses input
    with open("input.txt", 'r') as file:
        # raw file
        raw:str = file.read().rstrip()
        raw = raw.split('\n')
        # splits to sensor, beacon pairs
        pairs:list = [list(line.split(": ")) for line in raw]
        pairs = [[sensor.split(" at ")[1].split(", "), beacon.split(" at ")[1].split(", ")] for sensor, beacon in pairs]
        # extracts sensor and beacon into integer base pairs
        pairs = [
                    (
                        tuple([int(val.split('=')[1]) for val in sensor]),
                        tuple([int(val.split('=')[1]) for val in beacon])
                    )
                    for sensor, beacon in pairs
                ]
    
    # sets map bounds
    x_bounds = (0, 4000000) 
    y_bounds = (0, 4000000)

    def calc_manhattan_dist(loc0:tuple, loc1:tuple) -> int:
        """
        Calculates the manhattan distance between 2 locations

        loc1:tuple
            Position 1
        loc2:tuple
            Position 2
        
        Returns:
        Manhattan distance
        """
        manhattan_distance:int = sum([abs(loc0[i] - loc1[i]) for i in range(len(loc0))])
        return manhattan_distance
    
    # corresponds sensor to its maximum distance given nearest beacon
    sensor_max_dist:dict = dict()
    for sensor, beacon in pairs:
        # notes distance from each sensor to closest beacon
        sensor_max_dist[sensor] = calc_manhattan_dist(sensor, beacon)
    
    print("Max distances calculated")
    
    # finds all points just out of sensor range
    sensor_bounds:set = set()
    for sensor, dist in sensor_max_dist.items():
        x_off = 0
        y_off = dist + 1
        sensor = np.array(sensor)
        point = np.array((x_off, y_off)) + sensor
        while (tuple(point) not in sensor_bounds):
            # only adds points in bound
            if x_bounds[0] <= point[0] <= x_bounds[1] and y_bounds[0] <= point[1] <= y_bounds[1]:
                sensor_bounds.add(tuple(point))
    
            if y_off > 0:
                x_off += 1
                y_off -= 1
            elif x_off > 0:
                x_off -= 1
                y_off -= 1
            elif y_off < 0:
                x_off -= 1
                y_off += 1
            else:
                x_off += 1
                y_off += 1
            
            point = sensor + np.array((x_off, y_off))

    print("Bounds Calculated")
    print("# of Bounds: " + str(len(sensor_bounds)))
    
    # progress checkpoints
    checkpoint:int = len(sensor_bounds) // 20

    # goes through all the sensor bounds to find uncovered
    uncovered = set()
    # progress
    progress = 0
    for bound in sensor_bounds:
        for sensor, dist in sensor_max_dist.items():
            coverage = False
            if calc_manhattan_dist(bound, sensor) <= dist:
                coverage = True
                break
        
        if coverage is False:
            uncovered.add(bound)
        
        progress += 1
        if progress % checkpoint == 0:
            print(f"Progress: {progress}/{len(sensor_bounds)}")


    beacon:tuple = list(uncovered)[0]
    tuning_frequency:int = beacon[0] * 4000000 + beacon[1]
    tuning_frequency = int(tuning_frequency)
    print(tuning_frequency)
    copy_ans(tuning_frequency)

soln_2()