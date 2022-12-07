import sys
sys.path.append("../../")
from advent_io import *

# imports a stack-like object
from collections import deque
# import pandas and StringIO to feed data into pandas
from io import StringIO
from time import sleep
import numpy as np
import pandas as pd
import regex as re

fetch_input(7, 2022)
root = dict()
cursor = root
cursor_directory = list()
cursor_directory.append(root)
def soln_1():
    with open("input.txt", 'r') as file:
        raw = file.read().strip()
        lines = raw.split('\n')
    
    for line in lines:
        if line[0] == '$': # detects commands you run
            # removes the leading $ 
            line = line[2::].split(' ')
            
            # case matching the command
            match line[0]:
                case('cd'):
                    # moves cursor back to root
                    if line[1] == '/':
                        cursor = root
                    elif line[1] == '..':
                        # removes current directory
                        cursor_directory.pop()
                        # moves cursor up one directory
                        cursor = cursor_directory[-1]
                    else:
                        # creates directory if directory doesn't exist
                        if line[1] not in cursor.keys():
                            cursor[line[1]] = dict()

                        # adds the directory we're cding into into the cursor directory
                        cursor_directory.append(cursor[line[1]])
                        # moves cursor to the correct location
                        cursor = cursor_directory[-1]
                case('ls'):
                    pass
        else:
            # splits size and filename info
            size, filename = line.split(' ')
            # if it lists a dir, we make the dir and store it into the directory structure
            if size == 'dir':
                cursor[filename] = dict()
            # otherwise, note size of file
            else:
                cursor[filename] = int(size)            

    def dir_size(directory:dict) -> int:
        """
        Given a directory dictionary, calculates its size.

        directory:
            The directory dictionary
        """
        # returns the size of the directory if already calculated
        if ('size') in directory.keys():
            return directory[('size')]
        
        # total directory size
        total_size:int = 0
        # goes through all things in the dictionary
        for name, size in directory.items():
            # figures out subdirectory size, then adds it
            if isinstance(size, dict):
                total_size += dir_size(size)
            # adds filesize to size
            else:
                total_size += size
        # we store size with key tuple size in directory so it doesn't conflict with any names
        directory[('size')] = total_size
        return directory[('size')]
    
    dir_size(root)
    
    def solve(directory:dict = root) -> int:
        """
        sums all the directories with size <= 100_000
        directory:
            the working directory
        """
        subsolution = 0
        for key, value in directory.items():
            if key == ('size') and value <= 100000:
                subsolution += value
            elif isinstance(value, dict):
                subsolution += solve(value)
        
        return subsolution
    
    solution = solve(root)
    print(solution)
    copy_ans(solution)
                    
soln_1()

def soln_2():
    pass