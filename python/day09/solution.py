from __future__ import annotations
import enum
from typing import NamedTuple, Self
from functools import singledispatchmethod


class Direction(enum.IntEnum):
    Right = 1
    Up = 2
    Left = 3
    Down = 4

    @property
    def vector(self):
        return DIR_TO_VEC[self]


LETTER_TO_DIRECTION = {
    "U": Direction.Up,
    "D": Direction.Down,
    "L": Direction.Left,
    "R": Direction.Right,
}


class Move(NamedTuple):
    dir: Direction
    amount: int


class Point(NamedTuple):
    x: int
    y: int

    def __add__(self, other: Vector):
        return Point(self.x + other.dx, self.y + other.dy)

    def __sub__(self, other: Point):
        return Vector(self.x - other.x, self.y - other.y)


class Vector(NamedTuple):
    dx: int
    dy: int


@singledispatchmethod
def _Vector__add__(self, other: Point):
    return Point(self.dx + other.x, self.dy + other.y)


@_Vector__add__.register
def _(self, other: Vector):
    return Vector(self.dx + other.dx, self.dy + other.dy)


Vector.__add__ = _Vector__add__


DIR_TO_VEC = {
    Direction.Up: Vector(0, 1),
    Direction.Down: Vector(0, -1),
    Direction.Left: Vector(-1, 0),
    Direction.Right: Vector(1, 0),
}


def parse_input(s: str) -> list[Move]:
    for line in s.split("\n"):
        dir_letter, amount_str = line.split(" ")
        yield Move(dir=LETTER_TO_DIRECTION[dir_letter], amount=int(amount_str))


def sign(x):
    if x == 0:
        return 0
    return x / abs(x)


class MoveTracker:
    def __init__(self, moves: list[Move], node_count=2):
        self.moves = moves
        self.node_count = node_count
        self.nodes = {i: Point(0, 0) for i in range(node_count)}
        self.node_history = {i: {Point(0, 0)} for i in range(node_count)}

    def simulate(self):
        for move in self.moves:
            for _ in range(move.amount):
                head = self.nodes[0]
                vec = move.dir.vector
                head += vec
                self.nodes[0] = head
                self.node_history[0].add(head)
                for i in range(self.node_count - 1):
                    head = self.nodes[i]
                    tail = self.nodes[i + 1]
                    azi = head - tail
                    if max(map(abs, (azi.dx, azi.dy))) <= 1:
                        continue
                    shift = Vector(
                        sign(azi.dx) * min(abs(azi.dx), 1),
                        sign(azi.dy) * min(abs(azi.dy), 1),
                    )
                    tail += shift
                    self.node_history[i + 1].add(tail)
                    self.nodes[i + 1] = tail


def part1():
    text = open("input.txt").read()
    moves = list(parse_input(text))
    mt = MoveTracker(moves, 2)
    mt.simulate()
    print(len(mt.node_history[1]))


def part2():
    text = open("input.txt").read()
    moves = list(parse_input(text))
    mt = MoveTracker(moves, 10)
    mt.simulate()
    print(len(mt.node_history[9]))


def main():
    part1()
    part2()


if __name__ == "__main__":
    main()
