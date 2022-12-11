import dataclasses
from collections import deque
from typing import NamedTuple


@dataclasses.dataclass
class File:
    name: str
    size: int


@dataclasses.dataclass
class Dir:
    name: str
    dirs: dict[str, 'Dir']
    files: dict[str, File]
    _size: int = None

    def add(self, dirs: list['Dir'], files: list[File]):
        for d in dirs:
            self.dirs[d.name] = d
        for f in files:
            self.files[f.name] = f

    @property
    def size(self):
        if self._size is None:
            self._size = (
                    sum(f.size for f in self.files.values()) +
                    sum(d.size for d in self.dirs.values())
            )
        return self._size


class Command:
    pass


def isint(v):
    try:
        int(v)
    except ValueError:
        return False
    return True


class List(Command):
    @classmethod
    def parse(cls, parts: list[str]):
        return List()

    def parse_output(self, parts: list[str]):
        if not parts:
            return
        if parts[0] == 'dir':
            return Dir(parts[1], {}, {})
        if isint(parts[0]):
            return File(size=int(parts[0]), name=parts[1])

    def process(self, parser: 'Parser'):
        while parser.input:
            line = parser.input.popleft()
            if line.startswith('$'):
                parser.input.appendleft(line)
                break
            item = self.parse_output(line.split())
            if isinstance(item, File):
                if item.name not in parser.current_dir.files:
                    parser.current_dir.files[item.name] = item
            elif isinstance(item, Dir):
                if item.name not in parser.current_dir.dirs:
                    parser.current_dir.dirs[item.name] = item


@dataclasses.dataclass
class Chdir(Command):
    path: str

    @classmethod
    def parse(cls, parts: list[str]):
        return Chdir(path=parts[0])

    def process(self, parser: 'Parser'):
        path_parts = self.path.split('/')
        if path_parts[0] == '':
            directory = parser.root
            path = []
            path_parts = path_parts[1:]
        else:
            directory = parser.current_dir
            path = parser.current_path[:]

        for part in path_parts:
            if part == '..':
                path = path[:-1]
                directory = parser.root
                for path_part in path:
                    directory = directory.dirs[path_part]

            elif part:
                directory = directory.dirs[part]
                path = [*path, part]

        parser.current_dir = directory
        parser.current_path = path


class Parser:
    command_classes = {
        "ls": List,
        "cd": Chdir
    }

    def __init__(self, lines: list[str]):
        self.root = Dir('', {}, {})
        self.current_dir = self.root
        self.current_path: list[str] = []
        self.input = deque(lines)

    def parse_line(self, line: str):
        parts = line.split()
        if parts[0] == '$':
            return self.parse_command(parts[1:])

    def parse_command(self, parts: list[str]):
        cmd_cls = self.command_classes[parts[0]]
        command = cmd_cls.parse(parts[1:])
        command.process(self)

    def process(self):
        while self.input:
            line = self.input.popleft()
            self.parse_line(line)


def get_dir_sizes(directory: Dir):
    result = []
    result.append(directory.size)
    dirs = [item for d in directory.dirs.values() for item in get_dir_sizes(d)]
    result.extend(dirs)
    return result


def get_dirs_below(directory: Dir, size):
    result = []
    if directory.size < size:
        result.append(directory)
    dirs = [item for d in directory.dirs.values() for item in get_dirs_below(d, size)]
    result.extend(dirs)
    return result


def part1():
    text = open('input.txt').read()
    p = Parser(text.split('\n'))
    p.process()
    db = get_dirs_below(p.root, 100000)
    print(sum(d.size for d in db))


def part2():
    text = open('input.txt').read()
    p = Parser(text.split('\n'))
    p.process()

    total_space = 70000000
    unused_needed = 30000000
    total_used = p.root.size
    to_free = total_used - (total_space - unused_needed)
    sizes = get_dir_sizes(p.root)
    good = [s for s in sizes if s > to_free]
    print(min(good))


def main():
    part1()
    part2()


if __name__ == '__main__':
    main()
