from __future__ import (
    annotations,
)

from dataclasses import (
    dataclass,
)
from fa_purity import (
    Cmd,
    PureIter,
    Stream,
)
from fa_purity.cmd.core import (
    CmdUnwrapper,
)
from fa_purity.pure_iter.factory import (
    unsafe_from_cmd,
)
from fa_purity.stream.factory import (
    unsafe_from_cmd as unsafe_build_stream,
)
from pathlib import (
    Path,
)
from tempfile import (
    NamedTemporaryFile,
)
from typing import (
    Callable,
    IO,
    Iterable,
)


@dataclass(frozen=True)
class TempFile:
    path: Path

    @staticmethod
    def new() -> Cmd[TempFile]:
        def _action() -> TempFile:
            file_object = NamedTemporaryFile("w", delete=False)
            file_object.close()
            return TempFile(Path(file_object.name))

        return Cmd.from_cmd(_action)

    def write_hook(self, hook: Callable[[IO[str]], Cmd[None]]) -> Cmd[None]:
        def _action(unwrapper: CmdUnwrapper) -> None:
            with open(self.path, "w", encoding="UTF-8") as file:
                unwrapper.act(hook(file))

        return Cmd.new_cmd(_action)

    def read_lines(self) -> Stream[str]:
        def _new_iter() -> Iterable[str]:
            with open(self.path, "r", encoding="UTF-8") as file:
                line = file.readline()
                while line:
                    yield line
                    line = file.readline()

        return unsafe_build_stream(Cmd.from_cmd(_new_iter))

    def write_lines(self, lines: PureIter[str]) -> Cmd[None]:
        return self.write_hook(
            lambda f: Cmd.from_cmd(lambda: f.writelines(lines))
        )


@dataclass(frozen=True)
class _TempReadOnlyFile:
    file: TempFile


@dataclass(frozen=True)
class TempReadOnlyFile:
    """
    Wraps a `TempFile` ensuring read only access.
    File path is private and should not be exposed.
    """

    _inner: _TempReadOnlyFile

    def read_lines(self) -> PureIter[str]:
        # safe since the file is supposed to be read only
        return unsafe_from_cmd(self._inner.file.read_lines().unsafe_to_iter())

    def extract(self) -> Cmd[TempFile]:
        """
        Useful when file path is required a new `TempFile` object
        will provide it without exposing the inner path
        """
        return TempFile.new().bind(
            lambda f: f.write_lines(self.read_lines()).map(lambda _: f)
        )

    @staticmethod
    def new(content: PureIter[str]) -> Cmd[TempReadOnlyFile]:
        return TempFile.new().bind(
            lambda f: f.write_lines(content).map(
                lambda _: TempReadOnlyFile(_TempReadOnlyFile(f))
            )
        )
