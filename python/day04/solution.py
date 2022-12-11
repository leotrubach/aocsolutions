from typing import NamedTuple


class Segment(NamedTuple):
    start: int
    end: int

    def fully_contains(self, other: 'Segment'):
        return self.start <= other.start and self.end >= other.end

    def overlaps(self, other: 'Segment'):
        return not (self.start > other.end or self.end < other.start)


def parse_line(l) -> tuple[Segment, Segment]:
    c1, c2 = l.split(',')
    s1, s2 = [Segment(*map(int, c.split('-'))) for c in (c1, c2)]
    return s1, s2


def part1():
    text = open('input.txt').read()
    spairs = [parse_line(l) for l in text.split('\n')]
    total = 0
    for fs, ss in spairs:
        if fs.fully_contains(ss) or ss.fully_contains(fs):
            total += 1
    print(total)



def part2():
    text = open('input.txt').read()
    spairs = [parse_line(l) for l in text.split('\n')]
    total = 0
    for fs, ss in spairs:
        if fs.overlaps(ss) or ss.overlaps(fs):
            total += 1
    print(total)


def main():
    part1()
    part2()


if __name__ == '__main__':
    main()