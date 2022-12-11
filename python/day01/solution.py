def part1():
    text = open('input.txt').read()
    calories = text.split("\n\n")
    cals = [
        sum(map(int, s.split('\n'))) for s in calories
    ]
    print(max(cals))


def part2():
    text = open('input.txt').read()
    calories = text.split("\n\n")
    cals = [
        sum(map(int, s.split('\n'))) for s in calories
    ]
    cals.sort(reverse=True)

    print(sum(cals[:3]))


def main():
    part1()
    part2()


if __name__ == '__main__':
    main()