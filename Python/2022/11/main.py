import sys
sys.path.append("../../")
from advent_io import *

# type hinting
from typing import Union
from numbers import Number
# imports iterable type
from collections.abc import Iterable
# imports a stack-like object
from collections import deque
# import pandas and StringIO to feed data into pandas
from io import StringIO
from time import sleep
import numpy as np
import pandas as pd
import regex as re
# imports add for map
from operator import add

fetch_input(11, 2022)

def soln_1():
    # parses input
    with open("input.txt", 'r') as file:
        # raw file
        raw:str = file.read().rstrip()
        # isolates each monkey
        raw = raw.replace('\n\n', '\n')
        monkeys_text = [line.rstrip() for line in raw.split("\n")]
    
    # class for each monkey
    class Monkey():
        def __init__(self, name:str, starting_items:list, operation:str, test:str, test_results:tuple):
            # name of the monkey
            self.name:str = name
            # items the monkey currently possesses
            self.items:list = starting_items
            # operation the monkey performs
            self.operation:str = operation
            # test the monkey does to determine its actions
            self.test:str = test
            # what the monkey does after it does its test
            self.test_results:tuple = test_results
        
        def __str__(self):
            return f"""
{self.name}:
    Starting items: {self.items}
    Operation: {self.operation}
    Test: {self.test}
        Results: {self.test_results}
            """

    def count_indents(string:str) -> int:
        """
        Counts the leading spaces in a string
        string:str
            string you're analyzing
        """
        return len(string) - len(string.strip())

    def build_monkeys_dict(string_list:list, current_level:dict, index:int=0, indentation_level:int=0) -> int:
        """
        Builds a dictionary of monkeys depending on its indentation level
        index:int
            the index of the current line we're on
        string_list:list
            a split list of all the things defining the monkey
        current_level:
            the current attribute dictionary corresponding to an indentation level we're appending to
        indentation_level:
            the current indentation level
        
        return:int
            the index of the line in the string_list we got to
        """
        while (index < len(string_list)):
            # the parts of the line split up
            line:tuple = tuple([part.rstrip().strip() for part in string_list[index].split(':')])
            # the indentation level of the line
            indentation:int = count_indents(string_list[index])
            
            # if we're exiting the indentation block, exit this layer
            if indentation < indentation_level:
                return index
            
            # if a line's only attribute is itself and an indented descriptor, make a dict corresponding the two
            elif len(line) == 1:
                # creates indentation block dictionary
                current_level[line[0]] = dict()
                # fills out indentation block dictionary, sets index to where the last operation left off
                index = build_monkeys_dict(string_list, current_level[line[0]], index=index + 1, indentation_level=indentation)
            elif indentation > indentation_level:
                # previous line was actually a nested descriptor
                prev_line:str = string_list[index - 1]
                prev_line:tuple = tuple([part.rstrip().strip() for part in prev_line.split(':')])
                sub_desc = dict()
                current_level[prev_line[0]] = {
                    'desc': prev_line[1],
                    'sub_desc': sub_desc
                }
                # builds sub_desc
                index = build_monkeys_dict(string_list, sub_desc, index=index, indentation_level=indentation)
            else:
                current_level[line[0]] = line[1]
                index += 1
        
        return index

    # dictionary of all monkeys by name
    monkeys:dict = dict()
    
    # makes the monkeys into dictionarys
    build_monkeys_dict(monkeys_text, monkeys)
    print(monkeys)

    # objectify monkeys
    monkey_list:list = list()
    for name, attribute in monkeys.items():
        attribute = attribute['sub_desc']
        monkey_list.append(Monkey(name, [int(item) for item in attribute['Starting items'].split(", ")], attribute['Operation'], attribute['Test']['desc'], tuple(attribute['Test']['sub_desc'].values())))
    
    for monkey in monkey_list:
        print(monkey)

soln_1()