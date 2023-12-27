import sys
from enum import Enum
import attrs
from collections import Counter
from operator import attrgetter


@attrs.frozen
class Hand:
    
    cards: tuple[int, int, int, int, int]
    bid: int
    type: int = attrs.field(init=False)

    @type.default
    def _set_type(self) -> int:

        counts = tuple(sorted(Counter(self.cards).values(), reverse=True))

        if counts == (5,):
            return 7  # 5 of a kind
        if counts == (4, 1):
            return 6  # 4 of a kind
        if counts == (3, 2):
            return 5  # full house
        if counts == (3, 1, 1):
            return 4  # 3 of a kind
        if counts == (2, 2, 1):
            return 3  # 2 pair
        if counts == (2, 1, 1, 1):
            return 2  # one pair
        if counts == (1, 1, 1, 1, 1):
            return 1  # high card
        raise ValueError(f'Unknown hand type: {self.cards}')
    


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


def sort_hands(values: list[Hand]) -> None:
    """worst to best"""
    values.sort(key=attrgetter('cards'))
    values.sort(key=attrgetter('type'))


def part_i(filename: str):

    hands = parse_hands(filename)
    sort_hands(hands)  # in-place sort
    
    winnings = 0
    for rank, hand in enumerate(hands, start=1):
        winnings += rank * hand.bid

    print(f'{winnings=}')
        


def part_ii(filename: str):
    raise NotImplementedError


if __name__ == '__main__':

    input_filename, part_number = sys.argv[1:]

    if part_number == '1':
        part_i(input_filename)

    # elif part_number == '2':
    #     part_ii(input_filename)

    # else:
    #     raise ValueError(f'Invalid part number: {part_number}')


        
