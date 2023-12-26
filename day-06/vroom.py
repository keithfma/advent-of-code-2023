import sys
import attrs
from math import sqrt, ceil, floor, prod


@attrs.frozen
class Race:

    # total race time
    t: int

    # distance-to-beat
    d: int



def parse_races(filename: str) -> tuple[Race, ...]:

    with open(filename, 'r') as fp:
        
        _, times_txt = fp.readline().split(':')
        times = [int(x) for x in times_txt.strip().split(' ') if x]

        _, distances_txt = fp.readline().split(':')
        distances = [int(x) for x in distances_txt.strip().split(' ') if x]
    
    return tuple(Race(t, d) for t, d in zip(times, distances))


def next_larger_int(num: float) -> int:
    if (larger := ceil(num)) > num:
        return larger
    return int(num + 1)


def next_smaller_int(num: float) -> int:
    if (smaller := floor(num)) < num:
        return smaller
    return int(num - 1)


def part_i(filename: str):

    races = parse_races(filename)
    
    num_paths_to_victory = []

    for race in races:
        # find two zeros of the quadratic equation 0 = charge_time**2 - charge_time*race_time + distance_to_beat 
        # use the quadratic equation to solve for charge_time, with a=1, b=-race_time and c=distance_to_beat
        # these zeros are the minimum and maximum charge time that will beat the target distance
        left_term = race.t / 2
        right_term = sqrt(race.t*race.t - 4*race.d) / 2
        min_charge_time = next_larger_int(left_term - right_term)
        max_charge_time = next_smaller_int(left_term + right_term)
        num_paths_to_victory.append(max_charge_time - min_charge_time + 1)

    print(f'Ways to win: {prod(num_paths_to_victory)}')


if __name__ == '__main__':

    input_file, part_number = sys.argv[1:]
    
    if part_number == '1': 
        part_i(input_file) 

    else:
        raise NotImplementedError(f'Unknown part number: {part_number}')

    
