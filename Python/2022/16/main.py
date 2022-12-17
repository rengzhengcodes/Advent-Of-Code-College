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

# imports itertools
import itertools as it

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
        Calculates max flow possible given a starting point     
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
            # gets the value of the best from this possibility tree
            branch_val:int = (
                # adds EV of opening via enron accounting
                valves[you]['flow'] * (time_left - 1) +
                calc_flow_possible(
                    you, opened | you, time_left - 1
                )
            )

            # if EV calculated > current max EV, replace
            if branch_val > max:
                max = branch_val

            del branch_val

        # you move
        for you_move in valves[you]['leads']:
            # gets the value of the best from this possibility tree
            branch_val:int = (
                calc_flow_possible(
                    you_move, opened, time_left - 1
                )
            )

            # if EV greater than current max EV, replace current max EV
            if branch_val > max:
                max = branch_val
        
        return max
    
    # just to generate DP
    maximum_flow = calc_flow_possible(translation['AA'], 0, 30)
    print(maximum_flow)
    copy_ans(maximum_flow)

# soln_1()

def soln_2():
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
        # we have 55 valves
        # 15 of them have nonzero flow
        # we can represent those 15 with LSB 0
        # we can represent the rest with LSB 1
        curr_nonzero_rep:np.uint16 = 0b10
        curr_zero_rep:np.uint16 = 1
        # int where all the valves are opened
        all_opened_rep:np.uint16 = 0

        # all valves
        all_valves = [valve for valve, item in valves_unmasked.items()]

        # the translation book
        translation:dict = dict()
        # translates all valves
        for valve in all_valves:
            # if there is no flow
            if valves_unmasked[valve]['flow'] == 0:
                # assign it a zero bit representation
                translation[valve] = curr_zero_rep
                # increment the representation by two to keep LSB = 0
                curr_zero_rep += 2
            # if there is flow
            else:
                # assign a nonzero flow bitrep (acts as bitmask for this rep)
                translation[valve] = curr_nonzero_rep
                # mask the all_opened_rep so we can keep track of what the all opened state looks like
                all_opened_rep |= curr_nonzero_rep
                # bitshift the mask for the next one, to be nice
                curr_nonzero_rep = curr_nonzero_rep << 1
        
        # delete unecessary values so we don't have runaway valves
        del all_valves
        del curr_nonzero_rep
        del curr_zero_rep

        # actual valves, bit representation
        valves:dict = dict()
        
        # translates all data to the bit representation
        for valve, item in valves_unmasked.items():
            valves[translation[valve]] = {
                'flow': item['flow'],
                'leads': tuple([translation[lead] for lead in item['leads']])
            }
        
        # deletes the unmasked version as we're done with it
        del valves_unmasked

    @cache
    def calc_all_possible_outcomes(
                        you:np.uint16, opened:np.uint16, time_left:np.uint8 = 30
        ) -> set:
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
            return {(0, opened)}
        
        ### branching options ###
        
        # set of all outcomes
        outcomes = set()
        
        # if you can open, open
        if not (you & opened) and you & 0b1 == 0:
            # increments all the values by enron accounting, then ors into possibility space
            outcomes |= {
                (valves[you]['flow'] * (time_left - 1) + value, opened)
                for value, opened in calc_all_possible_outcomes(
                    you, opened | you, time_left - 1
                )
            }

        # you move
        for you_move in valves[you]['leads']:
            # ors all the possibilities into the outcomes
            outcomes |= (
                calc_all_possible_outcomes(
                    you_move, opened, time_left - 1
                )
            )
        
        return outcomes

    # just to generate all outcomes
    outcomes = calc_all_possible_outcomes(translation['AA'], 0, 26)

    # identifies best max value for all combinations of opened and outcome
    best_per_opened:dict = dict()
    for outcome in outcomes:
        # if no current best, now you're the current best
        if outcome[1] not in best_per_opened:
            best_per_opened[outcome[1]] = outcome[0]
        # if current best, and you best it, you're the current best
        elif outcome[0] > best_per_opened[outcome[1]]:
            best_per_opened[outcome[1]] = outcome[0]
    
    # delete this, redundant we just need the best
    del outcomes

    # flow is maximized for all outcomes if the two entities DONT open the same valves (to prevent valve conflict and thus wasted turn) and have maximium total product compared to others
    best_outcome = 0
    # now data is flipped, in (opened, value) format
    best_outcomes = set(best_per_opened.items())

    # works for NC2, but should scale to NCN if you chain the &s and the outcome parsing
    for outcome0, outcome1 in it.combinations(best_outcomes, 2):
        # no common valve
        if outcome0[0] & outcome1[0] == 0:
            total = outcome0[1] + outcome1[1]
            if total > best_outcome:
                best_outcome = total

    print(best_outcome)
    copy_ans(best_outcome)

soln_2()