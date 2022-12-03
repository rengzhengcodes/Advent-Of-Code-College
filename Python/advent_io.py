import requests

response = requests.request('GET', "https://adventofcode.com/2022/day/1/input")
open("session_cookie.secret")