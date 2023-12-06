import sys


if __name__ == '__main__':

    input_path, part = sys.argv
    
    if part == '1': 
        pass
    else:
        raise ValueError(f'Bad part number: {part}')
