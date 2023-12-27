import sys
from enum import Enum
import attrs


# class Card(Enum):
#     """Named camel card"""
#     A
#     K   
#     Q
#     J
#     T
#     9

@attrs.frozen
class Hand:
    
    cards: tuple[int, int, int, int, int]
    bid: int


def parse_hands(filename: str) -> list[Hand]:
        
    hands = []

    specials = {'A': 14, 'K': 13, 'Q': 12, 'J': 11, 'T': 10}

    with open(filename, 'r') as fp:
        
        for line in fp.readlines():
            cards_txt, bid_txt = line.strip().split()
            
            cards = []
            for card_txt in cards_txt.strip():
                try:
                    cards.append(int(card_txt))
                except ValueError:
                    cards.append(specials[card_txt])
            
            hands.append(Hand(tuple(cards), int(bid_txt)))
    
    return hands


def part_i(filename: str):
    raise NotImplementedError


def part_ii(filename: str):
    raise NotImplementedError


if __name__ == '__main__':

    input_filename, part_number = sys.argv[1:]

    # if part_number == '1':
    #     part_i(input_filename)

    # elif part_number == '2':
    #     part_ii(input_filename)

    # else:
    #     raise ValueError(f'Invalid part number: {part_number}')

    hands = parse_hands(input_filename) 

        
