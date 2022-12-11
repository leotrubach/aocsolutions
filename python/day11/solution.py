import re
from collections import deque
from typing import Optional, Callable, Self

CONDITIONS = {"divisible by": lambda x, by: x % by == 0}

ACTION_RXP = re.compile(
    r"If (?P<condition_value>true|false): throw to monkey (?P<monkey_next>\d+)"
)


class Num:
    buckets = (19, 3, 11, 17, 5, 2, 13, 7)
    def __init__(self, vals):
        self.vals = vals

    @classmethod
    def fromint(cls, value):
        return cls(vals={
            b: value % b for b in cls.buckets
        })

    def __add__(self, other: int | Self):
        if isinstance(other, Num):
            return Num({
                b: (self.vals[b] + other.vals[b]) % b for b, v in self.buckets
            })
        elif isinstance(other, int):
            return Num({
                b: (self.vals[b] + other) % b for b in self.buckets
            })

    def __mul__(self, other: int | Self):
        if isinstance(other, Num):
            return Num({
                b: (self.vals[b] * other.vals[b]) % b for b in self.buckets
            })
        elif isinstance(other, int):
            return Num({
                b: (self.vals[b] * other) % b for b in self.buckets
            })

    def __mod__(self, other):
        return self.vals[other]

class Operation:
    def __init__(self, expression: str):
        self.expression = expression

    def perform(self, item):
        return eval(self.expression, {"old": item})


class Action:
    def __init__(self, condition_txt: str, actions: list[str]):
        condition, condition_arg_txt = (
            condition_txt.strip().removeprefix("Test: ").rsplit(" ", 1)
        )
        self.func = CONDITIONS[condition]
        self.arg = int(condition_arg_txt)
        self.actions = dict(self.parse_action(a) for a in actions)

    def parse_action(self, action_txt):
        mo = ACTION_RXP.search(action_txt)
        gd = mo.groupdict()
        return gd["condition_value"] == "true", int(gd["monkey_next"])

    def decide_monkey(self, value):
        return self.actions[self.func(value, self.arg)]


def parse_monkey(monkey_txt: str):
    parts: list[str] = monkey_txt.split("\n")
    assert len(parts) == 6
    mn_txt, items_txt, operation_txt, test_txt, action1_txt, action2_txt = parts
    mn = int(mn_txt.removeprefix("Monkey ").removesuffix(":"))
    items = list(
        map(Num.fromint, map(int, items_txt.strip().removeprefix("Starting items: ").split(", ")))
    )
    expression = operation_txt.strip().removeprefix("Operation: ").split("=")[1].strip()
    operation = Operation(expression)
    action = Action(test_txt, [action1_txt, action2_txt])
    return Monkey(mn, items, operation, action)


class Monkey:
    def __init__(self, number, items: list[Num], operation: Operation, action: Action):
        self.number = number
        self.playground: Optional[Playground] = None
        self.items = deque(items)
        self.operation = operation
        self.action = action
        self.inspections = 0

    def accept_item(self, level):
        self.items.append(level)

    def play_item(self, item: int):
        level = self.operation.perform(item)
        level = self.playground.reducer(level)
        monkey = self.action.decide_monkey(level)
        self.playground.monkeys[monkey].accept_item(level)
        self.inspections += 1

    def play(self):
        while self.items:
            item = self.items.popleft()
            self.play_item(item)


class Playground:
    def __init__(self, monkeys: list[Monkey], reducer: Callable):
        self.monkeys = monkeys
        for m in self.monkeys:
            m.playground = self
        self.reducer = reducer
        self.rounds = 0

    def play(self, rounds):
        for _ in range(rounds):
            for m in self.monkeys:
                m.play()
        self.rounds += rounds

    def print(self):
        print(f"== After round {self.rounds} ==")
        for m in self.monkeys:
            print(f"Monkey {m.number} inpected items {m.inspections}")
            print(m.items)
        print()


def part1():
    text = open("input.txt").read()
    monkey_txts = text.split("\n\n")
    monkeys = [parse_monkey(monkey_txt) for monkey_txt in monkey_txts]
    p = Playground(monkeys, reducer=lambda x: x // 3)
    p.play(20)
    m1, m2 = list(sorted(p.monkeys, key=lambda m: m.inspections, reverse=True))[:2]
    print(m1.inspections * m2.inspections)


def part2():
    text = open("input.txt").read()
    monkey_txts = text.split("\n\n")
    monkeys = [parse_monkey(monkey_txt) for monkey_txt in monkey_txts]
    p = Playground(monkeys, reducer=lambda x: x)
    for n in [1, 19, 980, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000][:]:
        p.play(n)
        p.print()
    m1, m2 = list(sorted(p.monkeys, key=lambda m: m.inspections, reverse=True))[:2]
    print(m1.inspections * m2.inspections)


def main():
    # part1()
    part2()


if __name__ == "__main__":
    main()
