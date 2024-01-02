import sys
import numpy as np


def parse_input(filename: str) -> list[np.ndarray]:

    with open(filename, 'r') as fp:
        data = []
        for line in fp.readlines():
            data.append(
                np.array([int(x) for x in line.strip().split(' ')], dtype=int)
            )
    return data


def part_i(filename: str):

    def next_value(series: np.ndarray) -> int:
        if len(np.unique(series)) == 1:
            return series[-1]
        delta = next_value(np.diff(series))
        return series[-1] + delta

    series_list = parse_input(filename)
    next_values = [next_value(x) for x in series_list]
    print(f'Sum of extrapolated values is {sum(next_values)}')


def part_ii(filename: str):
    raise NotImplementedError


if __name__ == '__main__':

    input_filename, part_number = sys.argv[1:]

    if part_number == '1':
        part_i(input_filename)

    # elif part_number == '2':
    #    part_ii(input_filename)

    # else:
    #     raise ValueError(f'Invalid part number: {part_number}')







    



