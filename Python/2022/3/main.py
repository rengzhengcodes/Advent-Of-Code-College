# allows import of advent_io
import sys
sys.path.append("../../")
from advent_io import *

fetch_input(3, 2022)

def soln_1():
    with open("input.txt", 'r') as file:
        sacks = file.read().rstrip()
        sacks = sacks.split('\n')
        # splits between the two components
        sacks = [(sack[0 : len(sack) // 2], sack[len(sack) // 2:]) for sack in sacks]
    
    priorities = 0
    for sack in sacks:
        common_char = list(set(sack[0]) & set(sack[1]))[0]
        if common_char.isupper():
            # converts to ascii, decrements to get position of letter
            priorities += ord(common_char) - 64
            # 26 mor epoints b/c upper
            priorities += 26
        else:
            # converts to ascii, decrements to get position of letter
            priorities += ord(common_char) - 96

    print(priorities)
    copy_ans(priorities) 

# soln_1()

def soln_2():
    with open("input.txt", 'r') as file:
        sacks = file.read().rstrip()
        sacks = sacks.split('\n')
        groups = [(sacks[i], sacks[i + 1], sacks[i + 2]) for i in range(0, len(sacks), 3)]
    
    priorities = 0
    for group in groups:
        common_char = list(set(group[0]) & set(group[1]) & set(group[2]))[0]
        if common_char.isupper():
            # converts to ascii, decrements to get position of letter
            priorities += ord(common_char) - 64
            # 26 mor epoints b/c upper
            priorities += 26
        else:
            # converts to ascii, decrements to get position of letter
            priorities += ord(common_char) - 96

    print(priorities)
    copy_ans(priorities) 

soln_2()