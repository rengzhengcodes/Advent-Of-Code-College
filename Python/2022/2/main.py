# allows import of advent_io
import sys
sys.path.append("../../")
from advent_io import *

fetch_input(2, 2022)

def soln_1():
    # the points per choice you make
    choice_score = {
        'X': 1,
        'Y': 2,
        'Z': 3
    }

    # given an input, which output wins
    win_table = {
        'A': 'Y',
        'B': 'Z',
        'C': 'X'
    }

    tie_table = {
        'A': 'X',
        'B': 'Y',
        'C': 'Z'
    }

    with open('input.txt', 'r') as file:
        # reads each line as a 2 long tuple of opponent choice, your choice
        choice_pairs = file.read()
        choice_pairs = choice_pairs.rstrip()
        choice_pairs = choice_pairs.split('\n')
        choice_pairs = [tuple(pair.split(' ')) for pair in choice_pairs]

    points = 0
    for (opponent, you) in choice_pairs:
        points += choice_score[you]

        if win_table[opponent] == you:
            points += 6
        elif tie_table[opponent] == you:
            points += 3
        else:
            points += 0

    print(points)
    copy_ans(points)

# soln_1()

def soln_2():
    # score from each choice
    choice_score = {
        'A': 1,
        'B': 2,
        'C': 3
    }
    # choices available
    choice_table = ['A', 'B', 'C']
    # choices from loss, draw, win
    win_loss_points = {
        'X': 0,
        'Y': 3,
        'Z': 6

    }

    with open('input.txt', 'r') as file:
        # reads each line as a 2 long tuple of opponent choice, your choice
        choice_pairs = file.read()
        choice_pairs = choice_pairs.rstrip()
        choice_pairs = choice_pairs.split('\n')
        choice_pairs = [tuple(pair.split(' ')) for pair in choice_pairs]
    
    points = 0
    for (opponent, win_loss) in choice_pairs:
        points += win_loss_points[win_loss]

        if win_loss == 'X':
            # loses if you choose an option 1 behind your opponent
            choice_delta = -1
        elif win_loss == 'Y':
            # tie if you chose the same option
            choice_delta = 0
        elif win_loss == 'Z':
            # win if you choose 1 ahead of your opponent
            choice_delta = 1
        
        # points from reverse-engineering what you choose
        points += choice_score[choice_table[(choice_table.index(opponent) + choice_delta) % 3]]

    print(points)
    copy_ans(points)

soln_2()