from dataclasses import (
    dataclass,
)
import os
from tempfile import (
    NamedTemporaryFile,
)
from typing import (
    Callable,
    IO as IO_FILE,
    TypeVar,
)

_T = TypeVar("_T")
OpenStrFile = IO_FILE[str]


@dataclass(frozen=True)
class _TempFile:
    name: str
    encoding: str


class TempFile(_TempFile):
    def __init__(self, encoding: str) -> None:
        with NamedTemporaryFile("w+", encoding=encoding, delete=False) as file:
            super().__init__(file.name, encoding)

    def map(
        self,
        function: Callable[[OpenStrFile], _T],
        mode: str,
    ) -> _T:
        with open(self.name, mode, encoding=self.encoding) as file:
            return function(file)

    def __del__(self) -> None:
        os.remove(self.name)
