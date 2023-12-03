"""Advent of Code 2023 - Day 3"""

import sys
from pprint import pprint
import numpy as np


def parse_arrays(filename: str) -> tuple[np.ndarray, np.ndarray]:
    """Return parsed input file as integer array of part numbers, and boolean array of symbol locations
    """
    with open(filename, 'r') as fp:
        
        numbers = []
        symbols = []
        for line in fp.readlines():
            numbers_row = []
            symbols_row = []
            for elem in line.strip().replace('.', '0'):
                try:
                    # if the element is an integer, store that value and not that it is not a symbol
                    numbers_row.append(int(elem))
                    symbols_row.append(False)
                except ValueError:   
                    # if the element is a symbol, treat its value as 0 and note that it *is* a symbol
                    numbers_row.append(0)
                    symbols_row.append(True)
            numbers.append(numbers_row)
            symbols.append(symbols_row)
    return np.array(numbers, dtype=int), np.array(symbols, dtype=bool)


if __name__ == '__main__':

    _, input_path, part = sys.argv
    
    if part == '1':
       pass 
    else:
        raise ValueError(f'No such {part=}')

    num, sym = parse_arrays(input_path)

    mask = sym.copy()
    mask[1:, :] = np.maximum(mask[1:, :], sym[:-1, :])  # down
    mask[:-1, :] = np.maximum(mask[:-1, :], sym[1:, :])  # up
    mask[:, :-1] = np.maximum(mask[:, :-1], sym[:, 1:])  # left
    mask[:, 1:] = np.maximum(mask[:, 1:], sym[:, :-1])  # left
