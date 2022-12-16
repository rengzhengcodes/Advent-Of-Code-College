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

# imports caching function for recursion
from functools import cache, lru_cache

# imports deepcopy function
from copy import deepcopy

fetch_input(16, 2022)

def soln_1():
    # parses input
    with open("example.txt", 'r') as file:
        # raw file
        raw:str = file.read().rstrip()
        # singlizes so it works with parser
        raw = raw.replace("valves", "valve")
        # splits among newlines
        raw = raw.split('\n')
        
        # breaks up into valves and leads
        valves_raw:list = [line.split("; ") for line in raw]
        del raw
        # breaks valves into leads and tuples
        valves_unmasked:dict = dict()

        # creates objects of valves
        for valve, leads in valves_raw:
            leads = tuple(leads.split("valve ")[1].split(", "))
            flow_rate = int(valve.split('=')[1])
            valve = valve.split(" has")[0].split("Valve ")[1]
            valves_unmasked[valve] = {
                'flow': flow_rate,
                'leads': leads
            }
        
        del valves_raw
        # we have 56 valves
        # 14 of them have nonzero flow
        # we can represent those 14 with LSB 0
        # we can represent the rest with LSB 1
        curr_nonzero_rep:np.uint16 = 2
        curr_zero_rep:np.uint16 = 1

        # all valves
        all_valves = [valve for valve, item in valves_unmasked.items()]

        # the translation book
        translation:dict = dict()
        for valve in all_valves:
            if valves_unmasked[valve]['flow'] == 0:
                translation[valve] = curr_zero_rep
                curr_zero_rep += 2
            else:
                translation[valve] = curr_nonzero_rep
                curr_nonzero_rep = curr_nonzero_rep << 1
        
        del all_valves
        del curr_nonzero_rep
        del curr_zero_rep

        # actual valves
        valves:dict = dict()
        # translate to bitmask
        for valve, item in valves_unmasked.items():
            valves[translation[valve]] = {
                'flow': item['flow'],
                'leads': tuple([translation[lead] for lead in item['leads']])
            }
         
        del valves_unmasked

    @cache
    def calc_flow_possible(
                        you:np.uint16, opened:np.uint16, time_left:np.uint8 = 30
        ) -> int:
        """
        Calculates all the flow possible given a starting point     
        you:np.uint16
            The position of you
        
        elephant:np.uint16
            The position of the elephant

        opened:np.uint16
            The opened valves, as bitmask
        
        time_left: int
            Amount of time left
        
        Returns:
            Maximum possible flow from state
        """
        # if time's up, return 0, no gain
        if time_left == 0:
            del you, opened, time_left
            return 0
        
        ### branching options ###
        
        # max gain branch so far
        max:int = 0
        
        # if you can open, open
        if not (you & opened) and you % 2 == 0:
            new_opened = opened | you
        
            branch_val:int = (
                valves[you]['flow'] * (time_left - 1) +
                calc_flow_possible(
                    you, new_opened, time_left - 1
                )
            )

            if branch_val > max:
                max = branch_val

            del new_opened
            del branch_val

        # you move
        for you_move in valves[you]['leads']:
            branch_val:int = (
                calc_flow_possible(
                    you_move, opened, time_left - 1
                )
            )

            if branch_val > max:
                max = branch_val
        
        return max
    
    # just to generate DP
    maximum_flow = calc_flow_possible(translation['AA'], 0, 26)
    print(maximum_flow)
    copy_ans(maximum_flow)

soln_1()

def soln_2():
    # parses input
    with open("example.txt", 'r') as file:
        # raw file
        raw:str = file.read().rstrip()
        # singlizes so it works with parser
        raw = raw.replace("valves", "valve")
        # splits among newlines
        raw = raw.split('\n')
        
        # breaks up into valves and leads
        valves_raw:list = [line.split("; ") for line in raw]
        del raw
        # breaks valves into leads and tuples
        valves_unmasked:dict = dict()

        # creates objects of valves
        for valve, leads in valves_raw:
            leads = tuple(leads.split("valve ")[1].split(", "))
            flow_rate = int(valve.split('=')[1])
            valve = valve.split(" has")[0].split("Valve ")[1]
            valves_unmasked[valve] = {
                'flow': flow_rate,
                'leads': leads
            }
        
        del valves_raw
        # we have 56 valves
        # 14 of them have nonzero flow
        # we can represent those 14 with LSB 0
        # we can represent the rest with LSB 1
        curr_nonzero_rep:np.uint16 = 2
        curr_zero_rep:np.uint16 = 1

        # all valves
        all_valves = [valve for valve, item in valves_unmasked.items()]

        # the translation book
        translation:dict = dict()
        for valve in all_valves:
            if valves_unmasked[valve]['flow'] == 0:
                translation[valve] = curr_zero_rep
                curr_zero_rep += 2
            else:
                translation[valve] = curr_nonzero_rep
                curr_nonzero_rep = curr_nonzero_rep << 1
        
        del all_valves
        del curr_nonzero_rep
        del curr_zero_rep

        # actual valves
        valves:dict = dict()
        # translate to bitmask
        for valve, item in valves_unmasked.items():
            valves[translation[valve]] = {
                'flow': item['flow'],
                'leads': tuple([translation[lead] for lead in item['leads']])
            }
         
        del valves_unmasked

    # our own dp implementation
    dp:dict = dict()
    def calc_flow_possible(
                        you:np.uint16, opened:np.uint16, time_left:np.uint8 = 30
        ) -> int:
        """
        Calculates all the flow possible given a starting point     
        you:np.uint16
            The position of you
        
        elephant:np.uint16
            The position of the elephant

        opened:np.uint16
            The opened valves, as bitmask
        
        time_left: int
            Amount of time left
        
        Returns:
            Maximum possible flow from state
        """
        # if time's up, return 0, no gain
        if time_left == 0:
            del you, opened, time_left
            return 0
        elif (you, opened, time_left) in dp:
            return dp[((you, opened, time_left))]
        
        ### branching options ###
        
        # max gain branch so far
        max:int = 0
        
        # if you can open, open
        if not (you & opened) and you % 2 == 0:
            new_opened = opened | you
        
            branch_val:int = (
                valves[you]['flow'] * (time_left - 1) +
                calc_flow_possible(
                    you, new_opened, time_left - 1
                )
            )

            if branch_val > max:
                max = branch_val

            del new_opened
            del branch_val

        # you move
        for you_move in valves[you]['leads']:
            branch_val:int = (
                calc_flow_possible(
                    you_move, opened, time_left - 1
                )
            )

            if branch_val > max:
                max = branch_val
        
        dp[(you, opened, time_left)] = max
        return max
    
    # just to generate DP
    calc_flow_possible(translation['AA'], 0, 26)

    valid_paths = [(max, opened) for (you, opened, time_left), max in dp.items()  if time_left == 25]

    print(valid_paths)

soln_2()