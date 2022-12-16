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
from functools import cache

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
            ) -> list:
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

soln_1()