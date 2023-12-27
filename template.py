import sys


def part_i(filename: str):
    raise NotImplementedError


def part_ii(filename: str):
    raise NotImplementedError


if __name__ == '__main__':

    _, input_filename, part_number = sys.argv[1:]

    if part_number == '1':
        part_i(input_filename)

    elif part_number == '2':
        part_ii(input_filename)

    else:
        raise ValueError(f'Invalid part number: {part_number}')
