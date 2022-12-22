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

fetch_input(6, 2022)

def soln_1():
    with open("input.txt", 'r') as file:
        raw = file.read().strip()
    
    for i in range(0, len(raw) - 4): # makes sure there's no index errors
        if len(set(raw[i:i+4])) == 4: # makes sure there's over 4 unique characters
            print(i + 4) # prompt asks for # of words processed
            copy_ans(i + 4)
            break
    
# soln_1()

def soln_2():
    with open("input.txt", 'r') as file:
        raw = file.read().strip()
    
    for i in range(0, len(raw) - 14): # makes sure that there's no EOL line
        if len(set(raw[i:i+14])) == 14: # makes sure there's over 14 unique characters
            print(i + 14) # # of characters processed
            copy_ans(i + 14)
            break

soln_2()