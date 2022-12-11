import collections
import itertools


def sliding_window(iterable, n):
    it = iter(iterable)
    window = collections.deque(itertools.islice(it, n), maxlen=n)
    if len(window) == n:
        yield tuple(window)
    for x in it:
        window.append(x)
        yield tuple(window)


def part1():
    text = open('input.txt').read()
    for i, chunk in enumerate(sliding_window(text, 4)):
        if len(set(chunk)) == len(chunk):
            print(i + len(chunk))
            return


def part2():
    text = open('input.txt').read()
    for i, chunk in enumerate(sliding_window(text, 14)):
        if len(set(chunk)) == len(chunk):
            print(i + len(chunk))
            return



def main():
    part1()
    part2()


if __name__ == '__main__':
    main()