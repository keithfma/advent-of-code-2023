import sys
# from attrs import frozen
# 
# 
# @frozen
# class Node:
#     name: str
#     left: Node 
#     right: Node
# 
#     def __str__(self):
#         return f'{self.__class__.__name__}({name}, ({left.name}, {right.name}))'


def part_i(filename: str):

    graph: dict[str, tuple[str, str]] = {}

    with open(filename, 'r') as fp:
        instructions = fp.readline().strip()
        fp.readline()  # skip one
        for line in fp.readlines():
            name, children = line.strip().split('=')
            left, right = children.strip()[1:-1].split(',')
            graph[name.strip()] = (left.strip(), right.strip())

    at = 'AAA'
    steps = 0

    while at != 'ZZZ':
        instruction = instructions[steps % len(instructions)]
        if instruction == 'L':
            at = graph[at][0]
        elif instruction == 'R':
            at = graph[at][1]
        else:
            raise ValueError('Unknown instruction: {instruction}')
        steps += 1
    
    print(f'At {at} in {steps} steps')


def part_ii(filename: str):
    raise NotImplementedError


if __name__ == '__main__':

    input_filename, part_number = sys.argv[1:]

    if part_number == '1':
        part_i(input_filename)

    elif part_number == '2':
        part_ii(input_filename)

    else:
        raise ValueError(f'Invalid part number: {part_number}')

        
        
