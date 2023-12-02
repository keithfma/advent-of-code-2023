"""Advent of Code 2023 Day 1"""

import sys
from pathlib import Path
import re
import click


WORD_TO_DIGIT = {
    'one': '1',
    'two': '2',
    'three':  '3',
    'four': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine': '9',
}

DIGITS = set(WORD_TO_DIGIT.values())

WORDS = set(WORD_TO_DIGIT.keys())


def part_i(txt: str):

    total = 0
    for line in txt.splitlines():
        
        digits = []
        
        for idx in range(len(line)):
            
            # check for character digits
            if line[idx] in DIGITS:
                digits.append(line[idx])

        this = int(digits[0] + digits[-1])
        total += this
        print(f"{line=}, {digits=}, {this=}, {total=}")
            
    print(f'{total=}')


def part_ii(txt: str):

    total = 0
    for line in txt.splitlines():
        
        digits = []
        
        for idx in range(len(line)):
            
            # check for character digits
            if line[idx] in DIGITS:
                digits.append(line[idx])

            # check for word digits
            else:
                for word in WORDS:
                    if line[idx:].startswith(word):
                        digits.append(WORD_TO_DIGIT[word])
                        break
        this = int(digits[0] + digits[-1])
        total += this
        print(f"{line=}, {digits=}, {this=}, {total=}")
            
    print(f'{total=}')
            

if __name__ == '__main__':

    _, input_path, part = sys.argv

    with open(input_path, 'r') as fp:
       input_txt = fp.read()

    if part == '1':
        part_i(input_txt)

    elif part == '2':
        part_ii(input_txt)

    else:
        raise ValueError('Invalid {part=}')
