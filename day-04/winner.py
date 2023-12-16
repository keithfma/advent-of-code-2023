import sys
import attrs


@attrs.define
class Card:

    id: int
    win: set[int]
    have: tuple[int]
    copies: int = 1

    @classmethod
    def parse(cls, card_txt) -> 'Card':
        id_txt, card_txt = card_txt.strip().split(':')
        win_txt, have_txt = card_txt.split('|')
        return cls(
            id=int(id_txt.strip().split(' ')[-1]),
            win={int(x) for x in win_txt.strip().split(' ') if x},
            have=tuple(int(x) for x in have_txt.strip().split(' ') if x),
        )

    def num_matches(self) -> int:
        return sum(1 if num in self.win else 0 for num in self.have)

    def score(self) -> int:
        power = self.num_matches() - 1
        if power: 
            return 2**power
        return 0


def part_i(filename: str):

    with open(filename, 'r') as fp:
        lines = fp.readlines()
    
    total_value = 0
    for line in lines: 
        card = Card.parse(line)
        total_value += card.score()

    print(f'{total_value=}')

if __name__ == '__main__':

    _, input_path, part = sys.argv
    
    if part == '1': 
        part_i(input_path)
    elif part =='2':
        pass
    else:
        raise ValueError(f'Bad part number: {part}')

    # parse cards
    cards = [] 
    with open(input_path, 'r') as fp:
        for line in fp.readlines():
            cards.append(Card.parse(line))

    # resolve cards and their copies
    total_cards = 0
    for ii, card in enumerate(cards):

        while card.copies:
            
            # print(card)

            total_cards += 1
            card.copies -= 1
            # print(card)
            # print()

            for jj in range(ii + 1, ii + 1 + card.num_matches()):
                cards[jj].copies += 1 

    print(f'{total_cards=}')
    


