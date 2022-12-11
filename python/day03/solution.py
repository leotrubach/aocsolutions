letters = 'abcdefghijklmnopqrstuvwxyz'
upperletters = letters.upper()

priorities = {letter: i for i, letter in enumerate(f'{letters}{upperletters}', 1)}

def divide(s):
    l = len(s)
    assert len(s) % 2 == 0
    hl = l // 2
    return s[:hl], s[hl:]


def chunks(L, n):
    """ Yield successive n-sized chunks from L.
    """
    for i in range(0, len(L), n):
        yield L[i:i+n]


def part1():
    text = open('input.txt').read()
    prio_sum = 0
    for line in text.split('\n'):
        l, r = divide(line)
        common = set(l) & set(r)
        assert len(common) == 1
        for c in common:
            prio_sum += priorities[c]
    print(prio_sum)



def part2():
    text = open('input.txt').read()
    prio_sum = 0
    for a, b, c in chunks(text.split('\n'), 3):
        common = set(a) & set(b) & set(c)
        assert len(common) == 1
        for c in common:
            prio_sum += priorities[c]

    print(prio_sum)

def main():
    part1()
    part2()


if __name__ == '__main__':
    main()