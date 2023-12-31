import sys
from attrs import define, frozen
from operator import attrgetter
from copy import copy


def parse_input(filename: str) -> tuple[str, dict[str, tuple[str, str]]]:
    """Parse input file to return...
    + string containing instructions (e.g., LRR)
    + dictionary mapping node name to the (left, right) childrens node names
    """
    graph: dict[str, tuple[str, str]] = {}

    with open(filename, 'r') as fp:
        instructions = fp.readline().strip()
        fp.readline()  # skip one
        for line in fp.readlines():
            name, children = line.strip().split('=')
            left, right = children.strip()[1:-1].split(',')
            graph[name.strip()] = (left.strip(), right.strip())
    
    return instructions, graph


def part_i(filename: str):


    instructions, graph = parse_input(filename)

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


@define
class Traveler:
    node: str
    steps: int
    
    @property
    def done(self) -> int:
        return self.node[-1] == 'Z'


@frozen
class Location:
    node: str
    instruction_index: int


@frozen
class Destination:
    node: str
    num_steps: int



def part_ii(filename: str):
    # NOTE: run time is too long! It turns out that the travelers are traversing simple loops of len(instructions) steps
    #   To get the answer, we need the least common multiple of all these loop lengths, which is 21_003_205_388_413. My 
    #   program takes a looooong time to get to 21 trillion.
    #   
    # I found this out by inspecting the "cheat_sheet" variable. Not sure how I would solve this entirely programatically though!

    instructions, graph = parse_input(input_filename)

    cheat_sheet: dict[Location, Destination] = {}

    travelers = [Traveler(name, 0)  for name in graph.keys() if name.endswith('A')]
    min_traveler = travelers[0]  # arbitrary
    max_traveler = travelers[-1]  # arbitrary

    while True: 
        
        # check for completion, and find the next node to update while we are at it
        all_done = True
        for traveler in travelers:

            all_done = all_done and traveler.done

            if traveler.steps < min_traveler.steps:
                min_traveler = traveler
            elif traveler.steps > max_traveler.steps:
                max_traveler = traveler

        if all_done and min_traveler.steps == max_traveler.steps:
            break
        else:
            print(f'{min_traveler.steps:_}')

        # not done! update the traveler with the fewest steps
        instruction_index = min_traveler.steps % len(instructions)
        instruction = instructions[instruction_index]

        current_location = Location(min_traveler.node, instruction_index)

        if current_location in cheat_sheet:
            # skip ahead to the next possible end node
            destination = cheat_sheet[current_location]
            min_traveler.node = destination.node
            min_traveler.steps += destination.num_steps

        else:
            # follow instructions to the next possible endpoint
            init_steps = min_traveler.steps
            while True:
            
                # move to child as instructed
                min_traveler.steps += 1
                
                left, right = graph[min_traveler.node]
                if instruction == 'L':
                    min_traveler.node = left
                elif instruction == 'R':
                    min_traveler.node = right
                else:
                    raise ValueError(f'Unknown instruction: {instruction}')

                # prepare next instruction 
                instruction_index = min_traveler.steps % len(instructions)
                instruction = instructions[instruction_index]

                # stop if this is a possible endpoint
                if min_traveler.done:
                    cheat_sheet[current_location] = Destination(min_traveler.node, min_traveler.steps - init_steps)
                    break

    print(f'Complete in {min_traveler.steps} steps')


if __name__ == '__main__':

    input_filename, part_number = sys.argv[1:]

    if part_number == '1':
        part_i(input_filename)

    elif part_number == '2':
        part_ii(input_filename)

    else:
        raise ValueError(f'Invalid part number: {part_number}')



        
