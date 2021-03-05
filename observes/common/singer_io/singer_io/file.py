# Standard libraries
import tempfile
from functools import (
    partial,
)
from typing import (
    Callable, IO,
    Iterator,
    NamedTuple,
)
# Third party libraries

# Local libraries


def _read(name: str) -> Iterator[str]:
    with open(name) as tmp:
        line = tmp.readline()
        while line:
            yield line
            line = tmp.readline()


def _print(name: str, data: str) -> None:
    with open(name) as tmp:
        print(data, file=tmp)


class DataFile(NamedTuple):
    name: str
    read: Callable[[], Iterator[str]]
    print: Callable[[str], None]

    @classmethod
    def new(cls) -> 'DataFile':
        name: str
        with tempfile.NamedTemporaryFile('w+', delete=False) as tmp:
            name = tmp.name

        return DataFile(
            name=name,
            read=partial(_read, name),
            print=partial(_print, name)
        )

    @classmethod
    def from_file(cls, file: IO[str]) -> 'DataFile':
        name: str
        with tempfile.NamedTemporaryFile('w+', delete=False) as tmp:
            tmp.write(file.read())
            name = tmp.name

        return DataFile(
            name=name,
            read=partial(_read, name),
            print=partial(_print, name)
        )
