from aocutils.utils import loader
import os

from math import remainder
from pprint import pprint

data = loader('input.txt')

current = 50

stops = []

for line in data:
    dir = line[:1]
    amount = int(line[1:])

    if dir == "L":
        change = -amount
    else:
        change = amount
    
    current = (current + change) %  100
    stops.append(current)

pprint(stops)
print(stops.count(0))