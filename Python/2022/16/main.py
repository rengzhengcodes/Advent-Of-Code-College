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
    maximum_flow = calc_flow_possible(translation['AA'], 0, 30)
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

    @cache
    def calc_flow_possible(
                        you_elephant:np.uint32, opened:np.uint16, time_left:np.uint8 = 30
        ) -> int:
        """
        Calculates all the flow possible given a starting point     
        you_elephant:np.uint32
            Position of you and the elephant
            You always is <= elephant when evaluated

        opened:np.uint16
            The opened valves, as bitmask
        
        time_left: int
            Amount of time left
        
        Returns:
            Maximum possible flow from state
        """
        # if time's up, return 0, no gain
        if time_left == 0:
            del you_elephant, opened, time_left
            return 0
        
        # gets you and elephant
        you = np.uint32(you_elephant & 0xFFFF0000) >> 16
        elephant = (you_elephant & 0x0000FFFF)

        ### branching options ###
        
        # max gain branch so far
        max:int = 0
        
        # if you and elephant can open, open
        if (
            you != elephant and 
            you & 0b1 == 0 and you & opened == 0 and
            elephant & 0b1 == 0 and elephant & opened == 0
        ):
            new_opened = opened | you | elephant
        
            branch_val:int = (
                valves[you]['flow'] * (time_left - 1) +
                valves[elephant]['flow'] * (time_left - 1) +
                calc_flow_possible(
                    you_elephant, new_opened, time_left - 1
                )
            )

            if branch_val > max:
                max = branch_val

            del new_opened
            del branch_val
        
        # if you can open, open
        if (
            you & 0b1 == 0 and you & opened == 0
        ):
            new_opened = opened | you

            # move elephant
            for elephant_move in valves[elephant]['leads']:
                you_temp = you
                if you > elephant_move:
                    elephant_move, you_temp = you_temp, elephant_move
                
                branch_val:int = (
                    valves[you]['flow'] * (time_left - 1) +
                    calc_flow_possible(
                        (you_temp << 16) | elephant_move, new_opened, time_left - 1
                    )
                )
        
            if branch_val > max:
                max = branch_val

            del new_opened
            del branch_val
        
        # if elephant can open, open
        if (
            elephant & 0b1 == 0 and elephant & opened == 0
        ):
            new_opened = opened | elephant

            # move you
            for you_move in valves[you]['leads']:
                elephant_temp = elephant
                if you_move > elephant:
                    elephant_temp, you_move = you_move, elephant_temp
                
                branch_val:int = (
                    valves[elephant]['flow'] * (time_left - 1) +
                    calc_flow_possible(
                        (you_move << 16) | elephant_temp, new_opened, time_left - 1
                    )
                )

            if branch_val > max:
                max = branch_val

            del new_opened
            del branch_val
        
        # both move
        for you_move in valves[you]['leads']:
            for elephant_move in valves[elephant]['leads']:
                if you_move > elephant_move:
                    elephant_move, you_move = you_move, elephant_move
                branch_val:int = (
                    calc_flow_possible(
                        (you_move << 16) | elephant_move, opened, time_left - 1
                    )
                )

                if branch_val > max:
                    max = branch_val
        
        return max
    
    # just to generate DP
    maximum_flow = calc_flow_possible((translation['AA'] << 16) | translation['AA'], 0, 26)
    print(maximum_flow)
    copy_ans(maximum_flow)

soln_2()