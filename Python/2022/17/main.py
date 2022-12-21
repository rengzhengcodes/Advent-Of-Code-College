import sys
sys.path.append("../../")
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

fetch_input(17, 2022)

def soln_1():
    # parses input
    with open("input.txt", 'r') as file:
        # raw file
        stream:str = file.read().rstrip()
    
    # dict to tuple of shape. index 0 is bottom layer.
    shapes:dict = {
        '-': (
            np.uint8(0b00_11_11_0_0)
        ),
        '+': (
            np.uint8(0b00_01_00_0_0),
            np.uint8(0b00_11_10_0_0),
            np.uint8(0b00_01_00_0_0),
        ),
        '⅃': (
            np.uint8(0b00_11_10_0_0),
            np.uint8(0b00_00_10_0_0),
            np.uint8(0b00_00_10_0_0)
        ),
        '|': (
            np.uint8(0b00_10_00_0_0),
            np.uint8(0b00_10_00_0_0),
            np.uint8(0b00_10_00_0_0),
            np.uint8(0b00_10_00_0_0)
        ),
        '*': (
            0b00_11_00_0_0,
            0b00_11_00_0_0
        )
    }

    # converts to tuple for iterative purposes, above is just for human readability
    shapes:tuple = tuple(shapes.values())
    
    # array of levels. levels[0] is  floor. Put in class to prevent bad accesses.
    levels:list = [np.uint8(0xFE)]

    class Rock:
        def __init__(self, shape:np.ndarray, occupied:list, level:int):
            """
            shape:np.ndarray
                The array representing the shape, where the top value is the bottom
            occupied:list
                Reference to the occupied section
            level:int
                The level of the bottom of the shape
            """
            self.shape:np.ndarray = shape
            self.occupied:list = occupied
            self.level:int = level
            self.shadow:np.uint8 = np.uint8(0)
            # creates a shadow of the shape
            for elem in shape:
                self.shadow = self.shadow | elem
        
        def __detect_stop__(self) -> bool:
            """
            Detects if a downward movement would cause the rock to run into something.
            
            Returns:
                If a rock will stop.
            """
            occupied_subset:list = self.occupied[self.level - 1:self.level - 1 + self.shape.shape[0]]
            # print(occupied_subset, self.level)
            
            # rectifies subset list if it's at the top
            if len(occupied_subset) != self.shape.shape[0]:
                while len(occupied_subset) < self.shape.shape[0]:
                    occupied_subset.append(np.uint8(0))
            
            return np.bitwise_and(self.shape, occupied_subset).any()

        def __detect_wall_collision__(self, stream:str) -> bool:
            """
            Detects if a certain jet stream will collide into a wall

            stream:str
                A char representing stream direction
            
            Returns:
                If a shift will hit a wall.
            """
            occupied_subset:list = self.occupied[self.level:self.level + self.shape.shape[0]]
            
            if len(occupied_subset) != self.shape.shape[0]:
                while len(occupied_subset) < self.shape.shape[0]:
                    occupied_subset.append(np.uint8(0))
            
            occupied_subset:np.ndarray = np.array(occupied_subset)
            # moves terrain relative to shape instead of shape relative to terrain
            if stream == '<':
                occupied_subset = occupied_subset >> 1
            elif stream == '>':
                occupied_subset = occupied_subset << 1

            return (
                (stream == '<' and (self.shadow & 0x80)) or 
                (stream == '>' and (self.shadow & 0x02)) or
                np.bitwise_and(occupied_subset, self.shape).any()
            )

        def __debug_print__(self, active = False):
            """
            Creates a print like the step by step for the example
            """
            if not active:
                return
            
            # list of occupied string representation per level
            levels = self.occupied
            print_list = list()
            for level in self.occupied:
                level = np.binary_repr(level, 8)
                print_list.append(level.replace('1', '#').replace('0', ' '))
            
            # creates space for the shape
            while len(print_list) < self.level + len(self.shape):
                print_list.append(' ' * 8)

            # inserting the shape being moved
            for i in range(len(self.shape)):
                level:int = self.level + i
                line_rep:str = np.binary_repr(self.shape[i], 8)
                # print(line_rep)
                for j in range(len(line_rep)):
                    if line_rep[j] == '1':
                        print_list[level] = print_list[level][0:j] + '@' + print_list[level][j+1:]

            print_list = print_list[::-1]
            print_str:list = ''
            for elem in print_list:
                print_str += elem + '\n'
            
            print(print_str)

                
        def move(self, stream:str) -> bool:
            """
            Does the movement operation for the falling rock

            stream:str
                A char representing stream direction.
            
            Returns:
                If the rock will continue moving
            """
            self.__debug_print__(False)
            # if you aren't moving into a wall, shift the shape
            if not self.__detect_wall_collision__(stream):
                if stream == '<':
                    self.shape = self.shape << 1
                    self.shadow = self.shadow << 1
                elif stream == '>':
                    self.shape = self.shape >> 1
                    self.shadow = self.shadow >> 1

            # if you're not stopping, fall 1
            if not self.__detect_stop__():
                self.level -= 1
            # if you are stopping
            else:
                # go through every element in the shape
                for i in range(len(self.shape)):
                    # calculate its absolute level
                    index:int = self.level + i
                    
                    # if something else in the level
                    if index < len(self.occupied):
                        # modify the level to account for this rock
                        self.occupied[index] = self.occupied[index] | self.shape[i]
                    
                    # if only this rock at the level
                    else:
                        # append yourself to the list
                        self.occupied.append(self.shape[i])
                
                # return you are no longer moving
                return False

            return True

        def __str__(self):
            """
            Returns the shape of the falling object and its level.
            """
            temp:list = list(self.shape)[::-1]
            string:str = ""
            for elem in temp:
                string += str(bin(elem)) + '\n'
            string += f"Level: {self.level}"
            return string

    rocks:int = 2022
    stream_pos:int = 0
    for i in range(rocks):
        # print(i, np.array(shapes[i % len(shapes)], ndmin=1))
        falling:Rock = Rock(
            np.array(shapes[i % len(shapes)], ndmin=1), 
            levels,
            len(levels) + 3
        )

        while falling.move(stream[stream_pos % len(stream)]):
            stream_pos += 1
            # print(falling)
        
        # one more stream call after it stops moving
        stream_pos += 1

    height:int = len(levels) - 1
    print(height)
    copy_ans(height)

# soln_1()

def soln_2():
    # parses input
    with open("input.txt", 'r') as file:
        # raw file
        stream:str = file.read().rstrip()
    
    # dict to tuple of shape. index 0 is bottom layer.
    shapes:dict = {
        '-': (
            np.uint8(0b00_11_11_0_0)
        ),
        '+': (
            np.uint8(0b00_01_00_0_0),
            np.uint8(0b00_11_10_0_0),
            np.uint8(0b00_01_00_0_0),
        ),
        '⅃': (
            np.uint8(0b00_11_10_0_0),
            np.uint8(0b00_00_10_0_0),
            np.uint8(0b00_00_10_0_0)
        ),
        '|': (
            np.uint8(0b00_10_00_0_0),
            np.uint8(0b00_10_00_0_0),
            np.uint8(0b00_10_00_0_0),
            np.uint8(0b00_10_00_0_0)
        ),
        '*': (
            0b00_11_00_0_0,
            0b00_11_00_0_0
        )
    }

    # converts to tuple for iterative purposes, above is just for human readability
    shapes:tuple = tuple(shapes.values())
    
    # array of levels. levels[0] is  floor. Put in class to prevent bad accesses.
    levels:list = [np.uint8(0xFE)]

    class Rock:
        def __init__(self, shape:np.ndarray, occupied:list, level:int) -> None:
            """
            shape:np.ndarray
                The array representing the shape, where the top value is the bottom
            occupied:list
                Reference to the occupied section
            level:int
                The level of the bottom of the shape
            """
            self.shape:np.ndarray = shape
            self.occupied:list = occupied
            self.level:int = level
            self.shadow:np.uint8 = np.uint8(0)
            # creates a shadow of the shape
            for elem in shape:
                self.shadow = self.shadow | elem
        
        def __detect_stop__(self) -> bool:
            """
            Detects if a downward movement would cause the rock to run into something.
            
            Returns:
                If a rock will stop.
            """
            occupied_subset:list = self.occupied[self.level - 1:self.level - 1 + self.shape.shape[0]]
            # print(occupied_subset, self.level)
            
            # rectifies subset list if it's at the top
            if len(occupied_subset) != self.shape.shape[0]:
                while len(occupied_subset) < self.shape.shape[0]:
                    occupied_subset.append(np.uint8(0))
            
            return np.bitwise_and(self.shape, occupied_subset).any()

        def __detect_wall_collision__(self, stream:str) -> bool:
            """
            Detects if a certain jet stream will collide into a wall

            stream:str
                A char representing stream direction
            
            Returns:
                If a shift will hit a wall.
            """
            occupied_subset:list = self.occupied[self.level:self.level + self.shape.shape[0]]
            
            if len(occupied_subset) != self.shape.shape[0]:
                while len(occupied_subset) < self.shape.shape[0]:
                    occupied_subset.append(np.uint8(0))
            
            occupied_subset:np.ndarray = np.array(occupied_subset)
            # moves terrain relative to shape instead of shape relative to terrain
            if stream == '<':
                occupied_subset = occupied_subset >> 1
            elif stream == '>':
                occupied_subset = occupied_subset << 1

            return (
                (stream == '<' and (self.shadow & 0x80)) or 
                (stream == '>' and (self.shadow & 0x02)) or
                np.bitwise_and(occupied_subset, self.shape).any()
            )

        def __debug_print__(self, active:bool = False) -> None:
            """
            Creates a print like the step by step for the example
            """
            if not active:
                return
            
            # list of occupied string representation per level
            print_list = list()
            for level in self.occupied:
                level = np.binary_repr(level, 8)
                print_list.append(level.replace('1', '#').replace('0', ' '))
            
            # creates space for the shape
            while len(print_list) < self.level + len(self.shape):
                print_list.append(' ' * 8)

            # inserting the shape being moved
            for i in range(len(self.shape)):
                level:int = self.level + i
                line_rep:str = np.binary_repr(self.shape[i], 8)
                # print(line_rep)
                for j in range(len(line_rep)):
                    if line_rep[j] == '1':
                        print_list[level] = print_list[level][0:j] + '@' + print_list[level][j+1:-1]

            print_list = print_list[::-1]
            print_str:list = ''
            for elem in print_list:
                print_str += elem + '\n'
            
            print(print_str)

                
        def move(self, stream:str) -> bool:
            """
            Does the movement operation for the falling rock

            stream:str
                A char representing stream direction.
            
            Returns:
                If the rock will continue moving
            """
            self.__debug_print__(False)
            # if you aren't moving into a wall, shift the shape
            if not self.__detect_wall_collision__(stream):
                if stream == '<':
                    self.shape = self.shape << 1
                    self.shadow = self.shadow << 1
                elif stream == '>':
                    self.shape = self.shape >> 1
                    self.shadow = self.shadow >> 1

            # if you're not stopping, fall 1
            if not self.__detect_stop__():
                self.level -= 1
            # if you are stopping
            else:
                # go through every element in the shape
                for i in range(len(self.shape)):
                    # calculate its absolute level
                    index:int = self.level + i
                    
                    # if something else in the level
                    if index < len(self.occupied):
                        # modify the level to account for this rock
                        self.occupied[index] = self.occupied[index] | self.shape[i]
                    
                    # if only this rock at the level
                    else:
                        # append yourself to the list
                        self.occupied.append(self.shape[i])
                
                # return you are no longer moving
                return False

            return True

        def __str__(self) -> str:
            """
            Returns the shape of the falling object and its level.
            """
            temp:list = list(self.shape)[::-1]
            string:str = ""
            for elem in temp:
                string += str(bin(elem)) + '\n'
            string += f"Level: {self.level}"
            return string

    rocks:int = 1000000000000
    stream_pos:int = 0
    rock:int = 0

    # tracks what level a block lands at relative to its position in the stream upon landing
    placement:dict = dict()
    for shape_num in range(len(shapes)):
        placement[shape_num] = {
            "stream_pos": [], # stream_pos % len(steam)
            "level": [], # level at which this was registered
            "rock": [] # which rock you were
        }

    # whether or not we've detected a repetition
    repetitive:bool = False
    # keeps running until we are out of rocks or detect a pattern
    while rock < rocks and not repetitive:
        # rock shape
        shape:int = rock % len(shapes)
        # print(i, np.array(shapes[i % len(shapes)], ndmin=1))
        falling:Rock = Rock(
            np.array(shapes[shape], ndmin=1), 
            levels,
            len(levels) + 3
        )
        while falling.move(stream[stream_pos % len(stream)]):
            stream_pos += 1
            # print(falling)
    
        # one more stream call after it stops moving
        stream_pos += 1
        
        # logs relative stream position
        placement[shape]["stream_pos"].append(stream_pos % len(stream))
        # logs level of rock stoppage
        placement[shape]["level"].append(falling.level)
        # logs rock number
        placement[shape]["rock"].append(rock)

        # if we've detected at least 3 repetitive stoppages for this shape
        if placement[shape]["stream_pos"].count(stream_pos % len(stream)) >= 3:
            # create cartesian product of all the data
            data:list = list(zip(placement[shape]["stream_pos"], placement[shape]["level"], placement[shape]["rock"]))

            # gets rid of data we dont care about
            data = [item for item in data if (item[0] == stream_pos % len(stream) and item[2] % len(shapes) == shape)]
            
            # takes the data, and calculates the distance and rock distance between them
            distances:list = list()
            for i in range(len(data) - 1):
                distances.append((data[i + 1][1] - data[i][1], data[i + 1][2] - data[i][2]))

            # count the number of times an interval separation occurs
            interval_count:collections.Counter = collections.Counter(distances)

            # makes sure every repetition is periodic (meaning it's happened at least twice, so we have had 2 repeats)
            periodic:bool = True
            for count in interval_count.values():
                if count % 2 == 1:
                    periodic = False
                    break
            
            # if every repetition is periodic
            if periodic:
                # calculate the period height
                period_height:int = sum([distance * (occurances // 2) for (distance, rock_distance), occurances in interval_count.items()])
            
                # then, check to see if two periods have occured for repetition
                period_1:list = levels[falling.level - period_height:falling.level]
                period_2:list = levels[falling.level - (2 * period_height):falling.level - period_height]
                repetitive = period_1 == period_2

                # if it is repetitive, calculate the rock distance
                if repetitive:
                    rock_distance:int = sum([rock_distance * (occurances // 2) for (distance, rock_distance), occurances in interval_count.items()])

        # finished a rock
        rock += 1

    # if we detected a repetition
    height:int = 0
    if repetitive:
        # calculates height over remaining periods
        height = period_height * ((rocks - rock) // rock_distance)
        # goes to proper rock
        rock += rock_distance * ((rocks - rock) // rock_distance)

        # as it's repetitive, we can simply run the remainder of the simulation like nothing happened and then append to the height covered by the remaining periods
        for i in range(rock, rocks):
            # print(i, np.array(shapes[i % len(shapes)], ndmin=1))
            falling:Rock = Rock(
                np.array(shapes[i % len(shapes)], ndmin=1), 
                levels,
                len(levels) + 3
            )

            while falling.move(stream[stream_pos % len(stream)]):
                stream_pos += 1
                # print(falling)
            
            # one more stream call after it stops moving
            stream_pos += 1

    height += len(levels) - 1
    print(height)
    copy_ans(height)

soln_2()