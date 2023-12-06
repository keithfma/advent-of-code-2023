"""Advent of Code 2023 - Day 3"""

import sys
from attrs import frozen
from pprint import pprint
from math import prod


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
    
    nrows = ii + 1
    ncols = jj + 1
        
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
                
            if nums and (elem not in DIGITS or jj == ncols - 1):
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


def part_ii(filename):

    with open(filename, 'r') as fp:
        txt = fp.read().strip()
    
    # find symbol locations
    gear_candidates: set[Loc] = set()
    for ii, row in enumerate(txt.splitlines()):
        for jj, elem in enumerate(row):
            if elem == '*':
                # a possible gear! store this location
                gear_candidates.add(Loc(ii, jj))
            else:
                # not a gear, do nothing
                pass
    
    nrows = ii + 1
    ncols = jj + 1
        
    # find part numbers and locations adjacent to them
    numbers: list[tuple[int, set[Loc]]] = []
    for ii, row in enumerate(txt.splitlines()):

        num_chars = []
        num_locs = set()

        for jj, elem in enumerate(row):

            if elem in DIGITS:
                # a digit in a number! append it and store this location and all neighbors.
                # It does not matter if the neighbor locations are in-bounds or not
                num_chars.append(elem)
                for delta_i in [-1, 0, 1]:
                    for delta_j in [-1, 0, 1]:
                        num_locs.add(Loc(ii + delta_i, jj + delta_j))
                
            if num_chars and (elem not in DIGITS or jj == ncols - 1):
                # we have a part number in progress and have either reached its end or reached the end of the row!
                num = int(''.join(num_chars)) 
                numbers.append((num, num_locs))

                # reset for next part number
                num_chars = []
                num_locs = set()
                
    # identify gears and sum their values
    total = 0
    for candidate in gear_candidates:
        adjacent_numbers = []
        for num, locs in numbers:
            if candidate in locs:
                adjacent_numbers.append(num)
        if len(adjacent_numbers) == 2:
            # print(f'{candidate=}, {adjacent_numbers=}')
            total += prod(adjacent_numbers)

    print(f'{total=}')


if __name__ == '__main__':

    _, input_path, part = sys.argv
    
    if part == '1':
       part_i(input_path)
    elif part == '2':
       part_ii(input_path)
        pass
    else:
        raise ValueError(f'No such {part=}')



               
