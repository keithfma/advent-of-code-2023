import sys


def part_i(filename: str):

    with open(filename, 'r') as fp:
        lines = fp.readlines()
    
    total_value = 0
    for line in lines: 
        win_txt, have_txt = line.strip().split(':')[1].split('|')
        win = {int(x) for x in win_txt.strip().split(' ') if x}
        have = tuple(int(x) for x in have_txt.strip().split(' ') if x)

        value = 0
        for num in have:
            if num in win:
                value = max(1, value*2)

        total_value += value

    print(f'{total_value=}')

if __name__ == '__main__':

    _, input_path, part = sys.argv
    
    if part == '1': 
        part_i(input_path)
    else:
        raise ValueError(f'Bad part number: {part}')
