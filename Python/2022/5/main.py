# allows import of advent_io
import sys
sys.path.append("../")
from advent_io import *

# imports a stack-like object
from collections import deque
# import pandas and StringIO to feed data into pandas
from io import StringIO
from time import sleep
import numpy as np
import pandas as pd
import regex as re

fetch_input(5, 2022)

def soln_1():
    with open("input.txt", 'r') as file:
        raw = file.read().strip()
        image, instructions = raw.split('\n\n')
        # parses instructions to its equivalent in a pd.dataframe
        image = image.replace("] ", ',')
        image = image.replace("]", '')
        image = image.replace("[", "")
        image = image.replace("    ", ",")
        image = image.replace("  ", ",")
        image = pd.read_csv(StringIO(image.rstrip()), sep=",", header=None, dtype=str)
        
        # reverses image so the indices are correct/easier to work with
        image = image[::-1]
        
        columns = dict()
        # converts to deque structure
        for i in range(len(image)):
            columns[i + 1] = deque()
            for j in range(len(image[i]) - 1):
                if image[i][j] is not np.nan:
                    columns[i + 1].appendleft(image[i][j])
        
        # separates instructions
        instructions = instructions.split('\n')

        # isolates numerical important values per instruction
        instructions = [tuple(re.split('[\D]*\s', instruction)[1::]) for instruction in instructions]
        instructions = [(int(amount), int(start), int(end)) for (amount, start, end) in instructions]

    for amount, start, end in instructions:
        for i in range(amount):
            columns[end].append(columns[start].pop())

    result = ''
    for key, value in columns.items():
        result += value.pop()
    
    print(result)
    copy_ans(result)

# soln_1()

def soln_2():
    with open("input.txt", 'r') as file:
        raw = file.read().strip()
        image, instructions = raw.split('\n\n')
        # parses instructions to its equivalent in a pd.dataframe
        image = image.replace("] ", ',')
        image = image.replace("]", '')
        image = image.replace("[", "")
        image = image.replace("    ", ",")
        image = image.replace("  ", ",")
        image = pd.read_csv(StringIO(image.rstrip()), sep=",", header=None, dtype=str)
        
        # reverses image so the indices are correct/easier to work with
        image = image[::-1]
        
        columns = dict()
        # converts to list structure
        for i in range(len(image)):
            columns[i + 1] = list()
            for j in range(len(image[i]) - 1):
                if image[i][j] is not np.nan:
                    columns[i + 1].append(image[i][j])

        # separates instructions
        instructions = instructions.split('\n')

        # isolates numerical important values per instruction
        instructions = [tuple(re.split('[\D]*\s', instruction)[1::]) for instruction in instructions]
        instructions = [(int(amount), int(start), int(end)) for (amount, start, end) in instructions]

    for amount, start, end in instructions:
        columns[end] = columns[start][0:amount] + columns[end]
        del columns[start][0:amount]

    result = ''
    for key, value in columns.items():
        result += value[0]
        
    print(result)
    copy_ans(result)

soln_2()