import sys
import attrs
from math import sqrt, ceil, floor, prod


def next_larger_int(num: float) -> int:
    if (larger := ceil(num)) > num:
        return larger
    return int(num + 1)


def next_smaller_int(num: float) -> int:
    if (smaller := floor(num)) < num:
        return smaller
    return int(num - 1)


@attrs.frozen
class Race:

    # total race time
    t: int

    # distance-to-beat
    d: int

    def ways_to_win(self) -> int:
        """Return number of ways to win this race"""
        # solves quadratic equation for the charge time needed to match the distance-to-beat
        #   then finds the min/max winning charge times asthe next higher/lower integers 
        left_term = self.t / 2
        right_term = sqrt(self.t*self.t - 4*self.d) / 2
        min_charge_time = next_larger_int(left_term - right_term)
        max_charge_time = next_smaller_int(left_term + right_term)
        return max_charge_time - min_charge_time + 1


def part_i(filename: str):

    with open(filename, 'r') as fp:
        
        _, times_txt = fp.readline().split(':')
        times = [int(x) for x in times_txt.strip().split(' ') if x]

        _, distances_txt = fp.readline().split(':')
        distances = [int(x) for x in distances_txt.strip().split(' ') if x]
    
    races = tuple(Race(t, d) for t, d in zip(times, distances))

    ways_to_win = [r.ways_to_win() for r in races]

    print(f'Ways to win: {prod(ways_to_win)}')


def part_ii(filename: str):

    with open(filename, 'r') as fp:
        
        _, time_txt = fp.readline().split(':')
        time = int(''.join(x for x in time_txt.strip().split(' ') if x))

        _, distance_txt = fp.readline().split(':')
        distance = int(''.join(x for x in distance_txt.strip().split(' ') if x))
    
    race = Race(time, distance)

    print(f'Ways to win: {race.ways_to_win()}')


if __name__ == '__main__':

    input_file, part_number = sys.argv[1:]
    
    if part_number == '1': 
        part_i(input_file) 

    elif part_number == '2': 
        part_ii(input_file) 

    else:
        raise NotImplementedError(f'Unknown part number: {part_number}')

    
