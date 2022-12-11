import abc
from typing import TypedDict, NamedTuple, Iterable
import bisect


class VMState(NamedTuple):
    cycle: int = 1
    x: int = 1


def chunks(L, n):
    """ Yield successive n-sized chunks from L.
    """
    for i in range(0, len(L), n):
        yield L[i:i+n]

class Instruction(abc.ABC):
    def parse(self, rest: list[str]):
        ...

    @staticmethod
    def execute(vm):
        ...


class Noop(Instruction):
    cycles = 1

    def __init__(self, rest: list[str]):
        self.rest = self.parse(rest)

    def parse(self, rest):
        return []

    def execute(self, vm):
        return VMState(x=vm.state.x, cycle=vm.state.cycle + self.cycles)


class Addx(Instruction):
    cycles = 2

    def __init__(self, rest: list[str]):
        self.rest = self.parse(rest)

    def parse(self, rest):
        return list(map(int, rest))


    def execute(self, vm):
        v = self.rest[0]
        return VMState(cycle=vm.state.cycle + self.cycles, x=vm.state.x + v)


TXT_TO_INSTRUCTION = {"noop": Noop, "addx": Addx}


def parse_input(s: str):
    for line in s.split("\n"):
        cmd, *rest = line.split()
        yield TXT_TO_INSTRUCTION[cmd](rest)


class CRT:
    def __init__(self):
        self.state = ['.'] * 240
        self.cursor = 0

    def step(self, state: VMState):
        highlight = state.x - 1 <= self.cursor % 40 <= state.x + 1
        self.state[self.cursor] = "#" if highlight else ' '
        self.cursor += 1

    def print(self):
        for c in chunks(self.state, 40):
            print(''.join(c))


class VM:
    def __init__(self):
        self.state = VMState()
        self.state_history = [self.state]
        self.crt = CRT()


    def run(self, commands: Iterable[Instruction]):
        for inst in commands:
            for _ in range(inst.cycles):
                self.crt.step(self.state)
            new_state = inst.execute(self)
            self.state = new_state
            self.state_history.append(new_state)

    def get_state_at(self, cycle):
        i = bisect.bisect_right(self.state_history, cycle, key=lambda s: s.cycle)
        if i:
            return self.state_history[i-1]
        raise ValueError


def part1():
    text = open("input.txt").read()
    commands = parse_input(text)
    v = VM()
    v.run(commands)
    result = 0
    for i in [20,60,100,140,180,220]:
        state = v.get_state_at(i)
        result += i * state.x
    print(result)


def part2():
    text = open("input.txt").read()
    commands = parse_input(text)
    v = VM()
    v.run(commands)
    v.crt.print()


def main():
    part1()
    part2()


if __name__ == "__main__":
    main()
