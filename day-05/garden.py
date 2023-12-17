import sys
import re
import attrs


@attrs.frozen
class MappedRange:

    src: int
    dest: int
    length: int

    @classmethod
    def from_txt(cls, txt: str):
        dest, src, length = (int(x) for x in txt.strip().split())
        return cls(src, dest, length)


@attrs.frozen
class Transformer:
    
    mapped_ranges: tuple[MappedRange, ...]

    @classmethod
    def from_txt(cls, txt: str):
        return cls(
            tuple(MappedRange.from_txt(x) for x in txt.strip().splitlines())
        )

    def __getitem__(self, key: int) -> int:
        for rng in self.mapped_ranges:
            if key >= rng.src:
                delta = key - rng.src
                if delta <= rng.length:
                    # in this mapped range
                    return rng.dest + delta
        # not in any mapped range, return key unchanged
        return key


def parse_input(filename: str) -> tuple[tuple[int, ...], tuple[Transformer, ...]]:

    with open(filename, 'r') as fp:
        chunks = re.findall(r'[\w-].*:([ \d\n]*)', fp.read())

    seeds = tuple(int(x) for x in chunks[0].split())

    trans = []
    for chunk in chunks[1:]:
        trans.append(Transformer.from_txt(chunk))
    
    return seeds, tuple(trans)


def part_i(filename: str):
    seeds, transformers = parse_input(filename)

    locations = []
    for value in seeds:
        for transformer in transformers:
            value = transformer[value]
        locations.append(value)

    print(f'{min(locations)=}')
    
            

if __name__ == '__main__':

    input_path, part_number = sys.argv[1:]

    if part_number == '1':
        part_i(input_path)
    else:
        raise NotImplementedError(f'{part_number=}')

        

