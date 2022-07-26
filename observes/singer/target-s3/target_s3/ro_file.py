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
    Iterable,
)


@dataclass(frozen=True)
class _TempReadOnlyFile:
    file_path: str


@dataclass(frozen=True)
class TempReadOnlyFile:
    _inner: _TempReadOnlyFile

    def read(self) -> PureIter[str]:
        def _new_iter() -> Iterable[str]:
            with open(self._inner.file_path, "r") as file:
                line = file.readline()
                while line:
                    line = file.readline()
                    yield line

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
    def save(content: Stream[str]) -> Cmd[TempReadOnlyFile]:
        def _action(act: CmdUnwrapper) -> TempReadOnlyFile:
            file = NamedTemporaryFile("w", delete=False)
            file.writelines(act.unwrap(content.unsafe_to_iter()))
            file.close()
            return TempReadOnlyFile(_TempReadOnlyFile(file.name))

        return new_cmd(_action)
