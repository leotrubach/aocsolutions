import itertools
import re
from typing import NamedTuple

COMMAND_RXP = re.compile(r"move (?P<amount>\d+) from (?P<source>\d+) to (?P<destination>\d+)")

class Command(NamedTuple):
    amount: int
    source: int
    destination: int

Crates = dict[int, list[str]]

def chunks(L, n):
    """ Yield successive n-sized chunks from L.
    """
    for i in range(0, len(L), n):
        yield L[i:i+n]


def cleanup_content(s):
    return s.strip().replace(']', '').replace('[', '')


def parse_crates(crates_txt) -> Crates:
    crates_lines = crates_txt.split('\n')
    max_len = max(len(s) for s in crates_lines)
    assert max_len % 4 == 3
    filled_lines = [f"{s:<{max_len + 1}}" for s in crates_lines]
    parts = [list(chunks(s, 4)) for s in reversed(filled_lines)]
    indexes = list(map(lambda x: int(x.strip()) if x.strip() else None, parts[0]))
    content = [list(filter(None, (cleanup_content(cc) for cc in c))) for c in itertools.zip_longest(*parts[1:])]
    return dict(zip(indexes, content))

def parse_commands(commands_txt) -> list[Command]:
    result = []
    for command_line in commands_txt.split('\n'):
        mo = COMMAND_RXP.match(command_line)
        assert mo
        params = {k: int(v) for k, v in mo.groupdict().items()}
        result.append(Command(**params))
    return result

def run_commands(commands: list[Command], crates: Crates):
    for command in commands:
        for _ in range(command.amount):
            crates[command.destination].append(crates[command.source].pop())

def run_commands2(commands: list[Command], crates: Crates):
    for command in commands:
        to_move = crates[command.source][-command.amount:]
        crates[command.source][-command.amount:] = []
        crates[command.destination].extend(to_move)

def part1():
    text = open('input.txt').read()
    crates_txt, commands_txt = text.split('\n\n')
    crates = parse_crates(crates_txt)
    commands = parse_commands(commands_txt)
    run_commands(commands, crates)
    print(''.join(v[-1] for k, v in crates.items()))


def part2():
    text = open('input.txt').read()
    crates_txt, commands_txt = text.split('\n\n')
    crates = parse_crates(crates_txt)
    commands = parse_commands(commands_txt)
    run_commands2(commands, crates)
    print(''.join(v[-1] for k, v in crates.items()))



def main():
    part1()
    part2()


if __name__ == '__main__':
    main()