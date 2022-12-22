import sys
sys.path.append("../")
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
        # nonzero flow valves
        good_valves:set = set()
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
                # adds to good valves
                good_valves.add(curr_nonzero_rep)
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
        
        def collect_nonzero_relation(start:np.uint16) -> None:
            """
            Returns distance from starting point to all other nonzero flow pipes
            start:np.uint16
                A valve with 0 flow
            """
            # BFS Queue
            queue:deque = deque()
            queue.append(start)
            # BFS Visited
            visited:set = set()
            # adds start to visited, no double back
            visited.add(start)
            # distance dictionary from start
            distances:dict = dict()
            # all valves we should keep in simplified
            good_valve_count:int = all_opened_rep.bit_count()
            # steps taken so far
            steps:int = 0
            while(len(distances) < good_valve_count - 1):
                # increment step counter
                steps += 1
                # next queue, to not mix with current step queue
                next_queue = deque()

                # empties current queue
                while(len(queue) > 0):
                    for lead in valves[queue.popleft()]['leads']:
                        # if we haven't been here before
                        if lead not in visited:
                            # mark that we've been here before
                            visited.add(lead)
                            # if this is a nonzero flow pipe, note the steps
                            if lead in good_valves:
                                distances[lead] = steps
                            # add lead to queue
                            next_queue.append(lead)

                # next iteration gets next_queue
                queue = next_queue

            return distances
                    
                    

        # simplified map of only valves with nonzero flow
        simplified:dict = dict()
        # notes 'AA', the starting point
        simplified[translation['AA']] = dict()
        simplified[translation['AA']]['leads'] = collect_nonzero_relation(translation['AA'])
        simplified[translation['AA']]['flow'] = 0
        # removes all empty valves as we can't open them
        for valve in good_valves:
            simplified[valve] = dict()
            simplified[valve]['leads'] = collect_nonzero_relation(valve)
            simplified[valve]['flow'] = valves[valve]['flow']
        del valves
        del good_valves

    @cache
    def calc_all_possible_outcomes(
                        you:np.uint16, opened:np.uint16, time_left:np.uint8 = 30
        ) -> set:
        """
        Calculates all the flow possible given a starting point     
        you:np.uint16
            The position of you

        opened:np.uint16
            The opened valves, as bitmask
        
        time_left: int
            Amount of time left
        
        Returns:
            Maximum possible flow from state
        """
        # set of all outcomes
        max:int = 0
        # you move and open
        for you_move, distance in simplified[you]['leads'].items():
            # ors all the possibilities into the outcomes
            if not (you_move & opened) and (distance + 1) < time_left:
                best_subbranch:int = (
                    calc_all_possible_outcomes(
                        you_move, opened | you_move, time_left - (distance + 1)
                    )
                )

                if best_subbranch > max:
                    max = best_subbranch
        
        # enron accounting for added EV to return from opening current valve
        return max + simplified[you]['flow'] * time_left

    # max flow solve
    maximum_flow = calc_all_possible_outcomes(translation['AA'], 0, 30)
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
        # nonzero flow valves
        good_valves:set = set()
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
                # adds to good valves
                good_valves.add(curr_nonzero_rep)
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
        
        def collect_nonzero_relation(start:np.uint16) -> None:
            """
            Returns distance from starting point to all other nonzero flow pipes
            start:np.uint16
                A valve with 0 flow
            """
            # BFS Queue
            queue:deque = deque()
            queue.append(start)
            # BFS Visited
            visited:set = set()
            # adds start to visited, no double back
            visited.add(start)
            # distance dictionary from start
            distances:dict = dict()
            # all valves we should keep in simplified
            good_valve_count:int = all_opened_rep.bit_count()
            # steps taken so far
            steps:int = 0
            while(len(distances) < good_valve_count - 1):
                # increment step counter
                steps += 1
                # next queue, to not mix with current step queue
                next_queue = deque()

                # empties current queue
                while(len(queue) > 0):
                    for lead in valves[queue.popleft()]['leads']:
                        # if we haven't been here before
                        if lead not in visited:
                            # mark that we've been here before
                            visited.add(lead)
                            # if this is a nonzero flow pipe, note the steps
                            if lead in good_valves:
                                distances[lead] = steps
                            # add lead to queue
                            next_queue.append(lead)

                # next iteration gets next_queue
                queue = next_queue

            return distances
                    
                    

        # simplified map of only valves with nonzero flow
        simplified:dict = dict()
        # notes 'AA', the starting point
        simplified[translation['AA']] = dict()
        simplified[translation['AA']]['leads'] = collect_nonzero_relation(translation['AA'])
        simplified[translation['AA']]['flow'] = 0
        # removes all empty valves as we can't open them
        for valve in good_valves:
            simplified[valve] = dict()
            simplified[valve]['leads'] = collect_nonzero_relation(valve)
            simplified[valve]['flow'] = valves[valve]['flow']
        del valves
        del good_valves

    @cache
    def calc_all_possible_outcomes(
                        you:np.uint16, opened:np.uint16, time_left:np.uint8 = 30
        ) -> set:
        """
        Calculates all the flow possible given a starting point     
        you:np.uint16
            The position of you

        opened:np.uint16
            The opened valves, as bitmask
        
        time_left: int
            Amount of time left
        
        Returns:
            Maximum possible flow from state
        """
        # set of all outcomes
        outcomes = set()
        # stay put
        outcomes.add((0, opened))
        # you move and open
        for you_move, distance in simplified[you]['leads'].items():
            # ors all the possibilities into the outcomes
            if not (you_move & opened) and (distance + 1) < time_left:
                outcomes |= (
                    calc_all_possible_outcomes(
                        you_move, opened | you_move, time_left - (distance + 1)
                    )
                )
        
        # enron accounting for added EV to return from opening current valve
        return {(value + simplified[you]['flow'] * time_left, opened_valves) for value, opened_valves in outcomes}

    # just to generate all outcomes
    outcomes = calc_all_possible_outcomes(translation['AA'], 0, 26)
    del simplified

    # identifies best max value for all combinations of opened and outcome
    best_per_opened:dict = dict()
    for outcome in outcomes:
        # if no current best, now you're the current best
        if outcome[1] not in best_per_opened:
            best_per_opened[outcome[1]] = outcome[0]
        # if current best, and you best it, you're the current best
        elif outcome[0] > best_per_opened[outcome[1]]:
            best_per_opened[outcome[1]] = outcome[0]
    
    # test it works for part 1 1 agent
    # print(max(best_per_opened.values()))

    # delete this, redundant we just need the best
    del outcomes

    # flow is maximized for all outcomes if the two entities DONT open the same valves (to prevent valve conflict and thus wasted turn) and have maximium total product compared to others
    best_outcome = 0

    # works for NC2, but should scale to NCN if you chain the &s and the outcome parsing
    for outcome0, outcome1 in it.combinations(best_per_opened.items(), 2):
        # no common valve
        if not (outcome0[0] & outcome1[0]):
            total = outcome0[1] + outcome1[1]
            if total > best_outcome:
                best_outcome = total

    print(best_outcome)
    copy_ans(best_outcome)

soln_2()