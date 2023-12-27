import sys
from enum import Enum
import attrs
from collections import Counter
from operator import attrgetter, methodcaller


@attrs.frozen
class Hand:
    
    cards: str

    bid: int

    def card_values(self, jokers: bool = False) -> tuple[int, int, int, int, int]:
        specials = {'A': 14, 'K': 13, 'Q': 12, 'J': 1 if jokers else 11, 'T': 10}
        values = []
        for card in self.cards:
            try:
                values.append(specials[card])
            except KeyError:
                values.append(int(card))
        return tuple(values)

    def hand_type(self, jokers: bool = False) -> int:

        if jokers:
            raise NotImplementedError

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

    with open(filename, 'r') as fp:
        
        for line in fp.readlines():
            cards, bid_txt = line.strip().split()
            hands.append(Hand(cards, int(bid_txt)))
    
    return hands


def sort_hands(values: list[Hand], jokers: bool = False) -> list[Hand]:
    """worst to best
    See https://docs.python.org/3/howto/sorting.html#sort-stability-and-complex-sorts
    """
    return sorted(
        sorted(values, key=methodcaller('card_values', jokers)),
        key=methodcaller('hand_type', jokers)
    )


def get_winnings(filename: str, jokers: bool):

    hands = parse_hands(filename)
    sorted_hands = sort_hands(hands, jokers) 
    
    winnings = 0
    for rank, hand in enumerate(sorted_hands, start=1):
        winnings += rank * hand.bid

    print(f'{winnings=}')
        


def part_ii(filename: str):
    raise NotImplementedError


if __name__ == '__main__':

    input_filename, part_number = sys.argv[1:]

    if part_number == '1':
        get_winnings(input_filename, jokers=False)

    elif part_number == '2':
        get_winnings(input_filename, jokers=True)

    else:
        raise ValueError(f'Invalid part number: {part_number}')


        
