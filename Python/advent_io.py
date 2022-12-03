from os import path
import requests

def fetch_input(day:int, year:int) -> None:
    """
    fetches the day's advent of code input and puts it into input.txt

    day:
        the day's data we're requesting
    """
    # exits if there's already an input
    if path.exists("input.txt"): 
        return
    
    # creates cookie with session ID to fetch unique input
    with open("../../session_cookie.secret", 'r') as file:
        cookie = {
            'session': file.read()
        }
    
    # gets the input from the server
    response = requests.get(f"https://adventofcode.com/{year}/day/{day}/input",
                            cookies=cookie)
    # writes the input to the correct area
    with open("input.txt", 'w') as file: 
        file.write(response.text)

import pyperclip
def copy_ans(ans:str) -> None:
    """
    Copies the inputted string, hopefully the answer, to the clipboard

    ans:
        string to be copied
    """
    pyperclip.copy(ans)