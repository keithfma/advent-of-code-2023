import sys
import attrs


@attrs.frozen
class Card:

    win: set[int]
    have: tuple[int]

    def score(self) -> int:
        matches = sum(1 if num in self.win else 0 for num in self.have)
        if matches: 
            return 2**(matches - 1)
        return 0


def part_i(filename: str):

    with open(filename, 'r') as fp:
        lines = fp.readlines()
    
    total_value = 0
    for line in lines: 
        win_txt, have_txt = line.strip().split(':')[1].split('|')
        card = Card(
            win={int(x) for x in win_txt.strip().split(' ') if x},
            have=tuple(int(x) for x in have_txt.strip().split(' ') if x),
        )
        total_value += card.score()

    print(f'{total_value=}')

if __name__ == '__main__':

    _, input_path, part = sys.argv
    
    if part == '1': 
        part_i(input_path)
    else:
        raise ValueError(f'Bad part number: {part}')
