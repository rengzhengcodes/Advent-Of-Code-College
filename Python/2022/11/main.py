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

soln_1()