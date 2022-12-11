import enum
import itertools


class Result(enum.IntEnum):
    Win = 6
    Draw = 3
    Lose = 0


class Move(enum.IntEnum):
    Rock = 1
    Paper = 2
    Scissors = 3

    def play(self, other: 'Move') -> Result:
        if self == other:
            return Result.Draw
        if self == Move.Paper:
            return Result.Win if other == Move.Rock else Result.Lose
        if self == Move.Scissors:
            return Result.Win if other == Move.Paper else Result.Lose
        if self == Move.Rock:
            return Result.Win if other == Move.Scissors else Result.Lose


    def deduce_move(self, others_result: Result):
        if others_result == Result.Draw:
            return self
        if others_result == Result.Win:
            if self == Move.Rock:
                return Move.Paper
            if self == Move.Paper:
                return Move.Scissors
            return Move.Rock
        # Lose
        if self == Move.Rock:
            return Move. Scissors
        if self == Move.Scissors:
            return Move.Paper
        return Move.Rock

Strategy = dict[str, Move]

first_strategy = {
    'A': Move.Rock,
    'B': Move.Paper,
    'C': Move.Scissors
}

second_strategy = {
    'X': Move.Rock,
    'Y': Move.Paper,
    'Z': Move.Scissors
}

Strategy2 = dict[str, Result]

second_strategy2 = {
    'X': Result.Lose,
    'Y': Result.Draw,
    'Z': Result.Win
}


def decode_moves(moves):
    for fm, sm in moves:
        yield first_strategy[fm], second_strategy[sm]


def decode_moves2(moves):
    for fm, sm in moves:
        yield first_strategy[fm], second_strategy2[sm]


def play_moves(moves: list[tuple[Move, Move]]) -> tuple[int, int]:
    fs, ss = 0, 0
    for fm, sm in moves:
        fs += fm.play(sm) + fm.value
        ss += sm.play(fm) + sm.value
    return fs, ss


def iter_strategies():
    for letters in itertools.permutations("XYZ"):
        R, P, S = letters
        yield {
            R: Move.Rock,
            P: Move.Paper,
            S: Move.Scissors
        }

def part1():
    text = open('input.txt').read()
    moves_str = [s.split(' ') for s in text.split('\n')]
    moves = list(decode_moves(moves_str))
    fs, ss = play_moves(moves)
    print(ss)


def part2():
    text = open('input.txt').read()
    moves_str = [s.split(' ') for s in text.split('\n')]
    moves = list(decode_moves2(moves_str))
    second_moves = [fm.deduce_move(result) for fm, result in moves]
    first_moves = [fm for fm, _ in moves]
    moves = [(fm, sm) for fm, sm in zip(first_moves, second_moves)]
    fs, ss = play_moves(moves)
    print(ss)


def main():
    part1()
    part2()


if __name__ == '__main__':
    main()