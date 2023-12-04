"""Advent of Code 2023 - Day 3"""

import sys
from attrs import frozen
from pprint import pprint


DIGITS = '0123456789'
NULL = '.'


@frozen
class Loc:
    row: int
    col: int


def part_i(filename: str):

    with open(filename, 'r') as fp:
        txt = fp.read().strip()
        
    # find locations adjacent to symbols
    include: set[Loc] = set()
    for ii, row in enumerate(txt.splitlines()):
        for jj, elem in enumerate(row):
            if elem not in NULL + DIGITS:
                # a symbol! store this location and all neighbors. It does not matter if the
                #   neighbor locations are in-bounds or not
                for delta_i in [-1, 0, 1]:
                    for delta_j in [-1, 0, 1]:
                        include.add(Loc(ii + delta_i, jj + delta_j))
            else:
                # not a symbol, do nothing
                pass
    
    num_rows = ii + 1
    num_cols = jj + 1
        
    # find part numbers and sum if they are to be included
    total = 0
    for ii, row in enumerate(txt.splitlines()):

        nums = []
        locs = set()

        for jj, elem in enumerate(row):
            if elem in DIGITS:
                # a digit in a number! append it
                nums.append(elem)
                locs.add(Loc(ii, jj))
                
            if nums and (elem not in DIGITS or jj == num_cols - 1):
                # we have a part number in progress and have either reached its end or reached the end of the row!
                # complete the part number, and sum if it should be included
                value = int(''.join(nums)) 
                if include.intersection(locs):
                    total += value
                else:
                    pass

                # reset for next part number
                nums = []
                locs = set()
                
               
    print(f'{total=}')

if __name__ == '__main__':

    _, input_path, part = sys.argv
    
    if part == '1':
       part_i(input_path)
    else:
        raise ValueError(f'No such {part=}')



            
