import sys
import attrs


@attrs.frozen
class Cubes:

    red: int = 0
    green: int = 0
    blue: int = 0

    @classmethod
    def from_string(cls, txt: str):
        kwargs = {}
        for num_and_color in txt.split(','):
            num, color = num_and_color.strip().split()
            if color in kwargs:
                raise ValueError(f'{color=} appears more than once in string "{txt}"')
            kwargs[color] = int(num)
        return cls(**kwargs)


@attrs.frozen(order=True)
class Game:
    
    game_id: int
    draws: tuple[Cubes, ...]
    
    @classmethod
    def from_string(cls, txt: str):
        game_txt, draws_txt = txt.split(':')
        return cls(
            game_id=int(game_txt.split()[1]),
            draws=tuple(Cubes.from_string(x) for x in draws_txt.split(';')),
        )

    @property
    def red(self) -> int:
        return max(x.red for x in self.draws)

    @property
    def green(self) -> int:
        return max(x.green for x in self.draws)

    @property
    def blue(self) -> int:
        return max(x.blue for x in self.draws)

    def possible(self, c: Cubes) -> bool:
        """True if the game would be possible if the number of cubes in the bag is 'c'"""
        return self.red <= c.red and self.green <= c.green and self.blue <= c.blue


def parse_games(filename: str) -> tuple[Game, ...]:
    """Return all games defined in the input file"""
    with open(filename, 'r') as fp:
        games = []
        for line in fp.read().splitlines():
            games.append(Game.from_string(line))
    return tuple(games)


BAG = Cubes(red=12, green=13, blue=14)


def part_i(filename: str) -> int:
    total = 0
    for game in parse_games(input_path):
        if game.possible(BAG):
            total += game.game_id
    print(f'{total=}')



if __name__ == '__main__':

    _, input_path, part = sys.argv
    
    if part == '1':
        part_i(input_path)
    else:
        raise ValueError(f'No such {part=}')



            

            
    
