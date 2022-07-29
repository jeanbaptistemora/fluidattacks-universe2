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
    new_cmd,
)
from fa_purity.pure_iter.factory import (
    unsafe_from_cmd,
)
from tempfile import (
    NamedTemporaryFile,
)
from typing import (
    Callable,
    IO,
    Iterable,
    TypeVar,
)


@dataclass(frozen=True)
class _TempReadOnlyFile:
    file_path: str


_T = TypeVar("_T")


@dataclass(frozen=True)
class TempReadOnlyFile:
    _inner: _TempReadOnlyFile

    def over_binary(self, cmd_fx: Callable[[IO[bytes]], Cmd[_T]]) -> Cmd[_T]:
        def _action(act: CmdUnwrapper) -> _T:
            with open(self._inner.file_path, "rb") as file:
                return act.unwrap(cmd_fx(file))

        return new_cmd(_action)

    def read(self) -> PureIter[str]:
        def _new_iter() -> Iterable[str]:
            with open(self._inner.file_path, "r") as file:
                line = file.readline()
                while line:
                    yield line
                    line = file.readline()

        return unsafe_from_cmd(Cmd.from_cmd(_new_iter))

    @staticmethod
    def new(content: PureIter[str]) -> Cmd[TempReadOnlyFile]:
        def _action() -> TempReadOnlyFile:
            file = NamedTemporaryFile("w", delete=False)
            file.writelines(content)
            file.close()
            return TempReadOnlyFile(_TempReadOnlyFile(file.name))

        return Cmd.from_cmd(_action)

    @staticmethod
    def from_cmd(
        write_cmd: Callable[[IO[str]], Cmd[None]]
    ) -> Cmd[TempReadOnlyFile]:
        """
        `write_cmd` initializes the file content. It has write-only access to file
        """

        def _action(act: CmdUnwrapper) -> TempReadOnlyFile:
            file = NamedTemporaryFile("w", delete=False)
            act.unwrap(write_cmd(file))
            file.close()
            return TempReadOnlyFile(_TempReadOnlyFile(file.name))

        return new_cmd(_action)

    @staticmethod
    def save(content: Stream[str]) -> Cmd[TempReadOnlyFile]:
        def _action(act: CmdUnwrapper) -> TempReadOnlyFile:
            file = NamedTemporaryFile("w", delete=False)
            file.writelines(act.unwrap(content.unsafe_to_iter()))
            file.close()
            return TempReadOnlyFile(_TempReadOnlyFile(file.name))

        return new_cmd(_action)
