"""Advent of Code 2023 Day 1"""

from pathlib import Path
import re


INPUT_PATH = Path('input.txt')

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


def ensure_digit(x: str) -> str:
    try:
        return WORD_TO_DIGIT[x]
    except KeyError:
        return x


pattern = re.compile(r'\d|one|two|three|four|five|six|seven|eight|nine')



def part_i(txt):
        
    total = 0
    
    for line in txt.splitlines():
        
        first_digit = None
        last_digit = None

        for x in line:
            if x in DIGITS:
                if first_digit is None:
                    first_digit = x
                else:
                    last_digit = x
        
        if not last_digit:
            last_digit = first_digit

        this = int(first_digit + last_digit)
        print(this)
        total += this

    print(f'{total=}')


# TODO: problem! need to do a match that does not permit overlaps...
# FAIL: 53254 is too high


def part_ii(txt: str):

    total = 0
    for line in txt.splitlines():
        matches = pattern.findall(line)
        this = int(ensure_digit(matches[0]) + ensure_digit(matches[-1]))
        total += this
        print(f"{line=}, {matches=}, {this=}, {total=}")
    print(f'{total=}')


def part_iib(txt: str):

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

    with open(INPUT_PATH, 'r') as fp:
        input_txt = fp.read()

    part_iib(input_txt)
