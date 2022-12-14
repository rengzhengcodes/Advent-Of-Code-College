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

fetch_input(15, 2022)

def soln_1():
    # parses input
    with open("input.txt", 'r') as file:
        # raw file
        raw:str = file.read().rstrip()

soln_1()