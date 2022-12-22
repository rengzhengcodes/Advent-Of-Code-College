# allows import of advent_io
import sys
sys.path.append("../")
from advent_io import *

fetch_input(4, 2022)

def soln_1():
    with open("input.txt", 'r') as file:
        raw = file.read().rstrip()
        pairs = raw.split('\n')
        # gets each pair as a string
        pairs = [tuple(pair.split(',')) for pair in pairs]
        # gets pair of pairs
        pairs = [(tuple(first.split('-')), tuple(second.split('-'))) for first, second in pairs]
        # ints everything
        pairs = [((int(one), int(two)), (int(three), int(four))) for ((one, two), (three, four)) in pairs]
    
    overlaps = 0
    for ((one, two), (three, four)) in pairs:
        schedule1 = set(range(one, two + 1))
        schedule2 = set(range(three, four + 1))
        overlap = schedule1 & schedule2

        if overlap == schedule1 or overlap == schedule2:
            overlaps += 1
    
    print(overlaps)
    copy_ans(overlaps)

# soln_1()

def soln_2():
    with open("input.txt", 'r') as file:
        raw = file.read().rstrip()
        pairs = raw.split('\n')
        # gets each pair as a string
        pairs = [tuple(pair.split(',')) for pair in pairs]
        # gets pair of pairs
        pairs = [(tuple(first.split('-')), tuple(second.split('-'))) for first, second in pairs]
        # ints everything
        pairs = [((int(one), int(two)), (int(three), int(four))) for ((one, two), (three, four)) in pairs]
    
    overlaps = 0
    for ((one, two), (three, four)) in pairs:
        schedule1 = set(range(one, two + 1))
        schedule2 = set(range(three, four + 1))
        overlap = schedule1 & schedule2

        if len(overlap) > 0:
            overlaps += 1
    
    print(overlaps)
    copy_ans(overlaps)

soln_2()