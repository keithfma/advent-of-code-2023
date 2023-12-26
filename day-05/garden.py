from __future__ import annotations
import sys

import re
import attrs
from typing import Optional, Union


@attrs.frozen(order=True)
class Range:
    """Range of integers, including endpoint values"""

    start: int
    end: int

    def contains(self, value: int): 
        """Return True if the range contains the input value"""
        return self.start <= value <= self.end

    def intersection(self, other: Range) -> Optional[Range]:
        """Return the part of self that intersects with other, if any"""
        start = max(self.start, other.start)
        end = min(self.end, other.end)
        if start <= end:
            return self.__class__(start, end)
        return None 

    def difference(self, other: Range) -> tuple[Range, ...]:
        """Return the parts of self that do not intersect with other"""
        parts = []
        
        if self.start < other.start:
            parts.append(Range(self.start, other.start - 1)) 

        if self.end > other.end:
            parts.append(Range(other.end + 1, self.end))

        return tuple(parts)


@attrs.frozen
class Transformer:
    """Piecewise transform defined by a set of "rules"

    Each rule defines a range and an integer offset. If a value is within a
    given range, it is transformed by adding the corresponding offset. If not,
    it is not transformed.
    """

    rules: tuple[tuple[Range, int], ...]

    def scalar(self, value: int) -> int:
        """Transform scalar integer
        """
        for rng, offset in self.rules:
            if rng.contains(value):
                return value + offset
        return value
    
    def range(self, value: Range) -> tuple[Range, ...]:
        """Transform range

        Returns a tuple of ranges, because the transformation rules may apply
        to only some parts of the input range, and transforming these parts "splits"
        the original range into multiple output ranges.
        """
        ranges = [value]
        complete = []
        
        for rule_range, rule_offset in self.rules:
            
            # create a place to store range(s) that were not transformed by this rule, to be checked
            #   against the next one
            next_ranges = []

            for this_range in ranges:
                
                if intersection := this_range.intersection(rule_range):
                    # the rule applies to at least part of the range

                    # transform the overlap, then these values are completed (at
                    #  most one rule applies to each value)
                    complete.append(
                        Range(
                            start=intersection.start + rule_offset,
                            end=intersection.end + rule_offset,
                        )
                    )

                    # set the non-overlapping portion(s) of the range aside to check against the 
                    #   rest of the rules 
                    next_ranges.extend(
                        this_range.difference(rule_range)
                    )
                
                else:
                    # rule does not apply to this input range, set it aside to check against the
                    #   rest of the rules
                    next_ranges.append(this_range)

            # try the next rule on all range(s) that have not yet matched a rule
            ranges = next_ranges

        # combine results, anything not transformed by any rule is returned unchanged
        return sorted(complete + next_ranges)


def _parse_chunks(filename: str) -> list[str]:
    """Break up input text file into 'chunks' that define seeds and transformers"""
    with open(filename, 'r') as fp:
        chunks = re.findall(r'[\w-].*:([ \d\n]*)', fp.read())
    return [x.strip() for x in chunks]


def _parse_seeds(txt: str) -> list[int]:
    """Parse seeds text chunk as a list of scalar seeds"""
    return [int(x) for x in txt.split()]
    

def _parse_seed_ranges(txt: str) -> list[Range]:
    """Parse seeds text chunk as a list of seed ranges"""

    values = [int(x) for x in txt.strip().split()]
    ranges = []

    while values:
        start = values.pop(0)
        end = start + values.pop(0) - 1
        ranges.append(Range(start, end))

    return ranges


def _parse_transformer(txt: str) -> Transformer:
    """Parse transformer text chunks"""

    rules = []

    for line in txt.splitlines():
        dest_start, src_start, length = (int(x) for x in line.strip().split())
        rule_range = Range(src_start, src_start + length -1)
        rule_offset = dest_start - src_start
        rules.append((rule_range, rule_offset))

    return Transformer(tuple(rules))




def part_i(filename: str):

    print('Part 1 -----')

    chunks = _parse_chunks(filename)
    seeds = _parse_seeds(chunks[0])
    transformers = [_parse_transformer(x) for x in chunks[1:]]

    locations = []
    for value in seeds:
        for transformer in transformers:
            value = transformer.scalar(value)
        locations.append(value)

    print(f'{min(locations)=}')
    

def part_ii(filename: str):

    print('Part 2 -----')

    chunks = _parse_chunks(filename)
    seed_ranges = _parse_seed_ranges(chunks[0])
    transformers = [_parse_transformer(x) for x in chunks[1:]]

    ranges = seed_ranges

    for transformer in transformers:

        next_ranges = []
        for this in ranges:
            next_ranges.extend(transformer.range(this))
             
        ranges = next_ranges

    minimum_location = min(x.start for x in ranges)
    print(f'{minimum_location=}')
            

if __name__ == '__main__':

    input_path, part_number = sys.argv[1:]

    if part_number == '1':
        part_i(input_path)
    else:
        part_ii(input_path)
        
