import enum
import operator
from collections import deque
from functools import cached_property, reduce


class Direction(enum.Enum):
    left = 1
    right = 2
    top = 3
    bottom = 4


def transpose(m):
    return [list(c) for c in zip(*m)]

class Grid:
    def __init__(self, values: list[list[int]]):
        self.cells = values

    def max_from_left(self, row: list[int]):
        result = [-1]
        for item in row[:-1]:
            result.append(max(result[-1], item))
        return result

    def max_from_right(self, row: list[int]):
        return self.max_from_left(row[::-1])[::-1]

    def view_range(self, row: list[int]):
        result = []
        for i, v in enumerate(row):
            visible_to_right = 0
            for j in range(i+1, len(row)):
                visible_to_right += 1
                if row[j] >= v:
                    break
            result.append(visible_to_right)
        return result


    @cached_property
    def maxes(self):
        transposed = transpose(self.cells)
        return {
            Direction.left: [self.max_from_left(r) for r in self.cells],
            Direction.right: [self.max_from_right(r) for r in self.cells],
            Direction.top: transpose([self.max_from_left(r) for r in transposed]),
            Direction.bottom: transpose([self.max_from_right(r) for r in transposed])
        }

    @cached_property
    def vrange(self):
        transposed = transpose(self.cells)
        return {
            Direction.left: [self.view_range(r) for r in self.cells],
            Direction.right: [self.view_range(r[::-1])[::-1] for r in self.cells],
            Direction.top: transpose([self.view_range(r) for r in transposed]),
            Direction.bottom: transpose([self.view_range(r[::-1])[::-1] for r in transposed])
        }

    def scenic_score(self, r, c):
        vrs = [self.vrange[direction][r][c] for direction in Direction]
        return reduce(
            operator.mul,
            vrs,
            1
        )

    @cached_property
    def sscores(self):
        return [self.scenic_score(r, c) for r, v in enumerate(self.cells) for c, _ in enumerate(v)]

    def visible(self, row, column):
        value = self.cells[row][column]
        return any(self.maxes[direction][row][column] < value for direction in Direction)

    @cached_property
    def visibility(self):
        return [self.visible(r, c) for r, v in enumerate(self.cells) for c, _ in enumerate(v)]

def part1():
    text = open('input.txt').read()
    grid = Grid([[int(c) for c in line] for line in text.split()])
    print(sum(grid.visibility))



def part2():
    text = open('input.txt').read()
    grid = Grid([[int(c) for c in line] for line in text.split()])
    for row in grid.vrange[Direction.top]:
        print(' '.join([f'{c-1:02d}' for c in row]))
    print(max(grid.sscores))


def main():
    part1()
    part2()


if __name__ == '__main__':
    main()