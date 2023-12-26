from __future__ import annotations
import sys

import re
import attrs
from typing import Optional, Union


# TODO: too many interfaces. I think we just want a Range and a Transformer class.
# The intermediate Transform is not so helpful.


@attrs.frozen
class Range:
    """Range of integers, including endpoint values"""

    start: int
    end: int

    def contains(self, value: int): 
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
class Transform:

    src: Range
    dest: Range

    @classmethod
    def from_txt(cls, txt: str):
        dest_start, src_start, length = (int(x) for x in txt.strip().split())
        return cls(
            Range(src_start, src_start + length -1),
            Range(dest_start, dest_start + length -1),
        )

    def scalar(self, value: int) -> Optional[int]:
        """Return transformed value, or None if the transform does not apply"""
        if self.src.contains(value):
            delta = value - self.src.start
            return self.dest.start + delta
        return None

    def range(self, value: Range) -> tuple[Optional[Range], tuple[Range, ...]]:
        """Apply transform to the input range, returning...
        + Transformed portion of the input range, or None if the transform does not apply
        + Untransformed portion(s) of the input range
        """
        intersection = self.src.intersection(value)
        
        if intersection is not None:
            transformed = Range(self.scalar(intersection.start), self.scalar(intersection.end)),
            return transformed, self.src.difference(value)
        
        else:
            return None, (value,)
       

@attrs.frozen
class TransformSet:
    
    transforms: tuple[Transform, ...]

    @classmethod
    def from_txt(cls, txt: str):
        return cls(
            tuple(Transform.from_txt(x) for x in txt.strip().splitlines())
        )

    def scalar(self, value: int) -> int:
        for transform in self.transforms:
            new_value = transform.scalar(value)
            if new_value is not None:
                return new_value 
        # no transformers apply, return value unchanged
        return value

    def range(self, value: Range) -> tuple[Range, ...]:
        """Apply all transforms to the input range"""

        unmapped = [value]
        mapped = []
 
        for transform in self.transforms:
            
            next_unmapped = []

            for this in unmapped:
                result = transform.range(this)
                if result[0] is not None:
                    mapped.append(result[0])
                next_unmapped.extend(result[1])
            
            unmapped = next_unmapped

        return tuple(mapped + unmapped)
            
                    
         


def parse_input(
    filename: str, seeds_as_ranges: bool = False
) -> tuple[Union[tuple[Range, ...], tuple[int, ...]], tuple[TransformSet, ...]]:

    with open(filename, 'r') as fp:
        chunks = re.findall(r'[\w-].*:([ \d\n]*)', fp.read())

    seeds_raw = [int(x) for x in chunks[0].split()]
    
    if seeds_as_ranges:
        seeds = []
        while seeds_raw:
            range_start = seeds_raw.pop(0)
            range_end = range_start + seeds_raw.pop(0) -1
            seeds.append(Range(range_start, range_end))

    else:
        seeds = seeds_raw
        

    trans = []
    for chunk in chunks[1:]:
        trans.append(TransformSet.from_txt(chunk))
    
    return seeds, tuple(trans)


def part_i(filename: str):
    seeds, transform_sets = parse_input(filename)

    locations = []
    for value in seeds:
        for transform_set in transform_sets:
            value = transform_set.scalar(value)
        locations.append(value)

    print(f'{min(locations)=}')
    

def part_ii(filename: str):
    pass
    

            

if __name__ == '__main__':

    input_path, part_number = sys.argv[1:]

    if part_number == '1':
        part_i(input_path)
    else:
        # part_ii(input_path)
        pass

        
    seed_ranges, transform_sets = parse_input(input_path, seeds_as_ranges=True)

    location_ranges = []


