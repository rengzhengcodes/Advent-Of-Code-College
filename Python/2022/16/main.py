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
    with open("input.txt", 'r') as file:
        # raw file
        raw:str = file.read().rstrip()
        # singlizes so it works with parser
        raw = raw.replace("valves", "valve")
        # splits among newlines
        raw = raw.split('\n')
        
        # breaks up into valves and leads
        valves_raw:list = [line.split("; ") for line in raw]
        # breaks valves into leads and tuples
        valves:dict = dict()

        # creates objects of valves
        for valve, leads in valves_raw:
            leads = tuple(leads.split("valve ")[1].split(", "))
            flow_rate = int(valve.split('=')[1])
            valve = valve.split(" has")[0].split("Valve ")[1]
            valves[valve] = {
                'flow': flow_rate,
                'leads': leads
            }
        
        @cache
        def calc_flow_possible(
                            start:str, opened:tuple, 
                            time_left:int = 30, valves:dict=valves
            ) -> int:
            """
            Calculates all the flow possible given a starting point
            start: str
                Current valve
            
            path:tuple
                path taken to get here
            
            time_left: int
                Amount of time left
            
            valves:dict
                valve dictionary
            
            Returns:
                Maximum possible flow from state
            """
            # print(start, time_left, current_opened)
            
            # time out scenario
            if time_left == 0: 
                return 0
            
            # all the path results
            possible_additional_flow:list = list()

            # goes to another tunnel
            for lead in valves[start]['leads']:
                possible_additional_flow.append(
                    # max flow given this current place
                    calc_flow_possible(
                        lead, 
                        opened = opened,
                        time_left = (time_left - 1)
                    )
                )
                
            # opens the current valve if unopened
            if start not in opened:
                # appends current valve to opened
                opened = tuple(list(opened) + [start])
                
                # adds best possible path now that we've
                possible_additional_flow.append(
                    # adds this as flow is pressure/minute, so gets net flow
                    valves[start]['flow'] * (time_left - 1) +
                    # adds further max possible net flow
                    calc_flow_possible(
                        start, 
                        opened = opened,
                        time_left = (time_left - 1)    
                    )
                )
            
            # returns max flow possible
            return max(possible_additional_flow)
        
        # all the ones with flow 0 you should not open
        opened:list = list()
        for valve, info in valves.items():
            flow, leads = info.values()
            if flow == 0:
                opened.append(valve)
        
        print(opened)
        maximum_flow = calc_flow_possible('AA', time_left = 30, opened=tuple(opened))
        print(maximum_flow)
        copy_ans(maximum_flow)

# soln_1()

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

    @lru_cache(maxsize=None)
    def calc_flow_possible(
                        you:np.uint16, elephant:np.uint16, opened:np.uint16, time_left:np.uint8 = 30
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
            del you, elephant, opened, time_left
            return 0
        
        ### branching options ###
        
        # max gain branch so far
        max:int = 0
        
        # if you and elephant can open, both open, if not on same valve
        if (
            you != elephant and (not (you & opened) and you % 2 == 0) and (not (elephant & opened) and elephant % 2 == 0)
        ):
            new_opened = opened | you | elephant

            branch_val:int = (
                valves[you]['flow'] * (time_left - 1) +
                valves[elephant]['flow'] * (time_left - 1) +
                calc_flow_possible(
                    you, elephant, new_opened, time_left - 1
                )
            )

            if branch_val > max:
                max = branch_val
            
            del branch_val
            del new_opened
        
        # if you can open, open, and elephant moves
        if not (you & opened) and you % 2 == 0:
            new_opened = opened | you
            
            for elephant_move in valves[elephant]['leads']:
                branch_val:int = (
                    valves[you]['flow'] * (time_left - 1) +
                    calc_flow_possible(
                        you, elephant_move, new_opened, time_left - 1
                    )
                )

                if branch_val > max:
                    max = branch_val

            del new_opened
            del branch_val

        # if elephant can open, open, and you move
        if not (elephant & opened) and elephant % 2 == 0:
            new_opened = opened | elephant

            for you_move in valves[you]['leads']:
                branch_val:int = (
                    valves[elephant]['flow'] * (time_left - 1) +
                    calc_flow_possible(
                        you_move, elephant, new_opened, time_left - 1
                    )
                )

                if branch_val > max:
                    max = branch_val
            
            del branch_val
            del new_opened
        
        # both move
        for you_move in valves[you]['leads']:
            for elephant_move in valves[elephant]['leads']:
                branch_val:int = (
                    calc_flow_possible(
                        you_move, elephant_move, opened, time_left - 1
                    )
                )

                if branch_val > max:
                    max = branch_val
                
                del branch_val
    
        del you, elephant, opened, time_left
        return max

    # all the ones with flow 0 you should not open
    opened:set = set()
    for valve, info in valves.items():
        flow, leads = info.values()
        if flow == 0:
            opened.add(valve)
    
    print(opened)
    maximum_flow = calc_flow_possible(translation['AA'], translation['AA'], time_left = 26, opened=0)
    print(maximum_flow)
    copy_ans(maximum_flow)

soln_2()