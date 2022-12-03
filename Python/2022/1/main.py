# allows import of advent_io
import sys
sys.path.append("../../")
from advent_io import *

fetch_input(1, 2022)

def soln_1():
    # preprocessing on file to isolate elfs
    with open("input.txt") as file:
        raw = file.read() # all the data
        elf_isolation = raw.split("\n\n") # double lines split elfs
        elf_isolation = [string.split('\n') for string in elf_isolation] # splits the calories into separate strings
        
        # converts all strings into ints
        for elf in range(len(elf_isolation)):
            elf_isolation[elf] = (int(string) for string in elf)
        
        # totals all calories per elf
        total_cals = [sum(elf) for elf in elf_isolation]
    
    print(max(total_cals))