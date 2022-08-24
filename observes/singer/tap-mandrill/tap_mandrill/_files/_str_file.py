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
from fa_purity.stream.factory import (
    unsafe_from_cmd as unsafe_build_stream,
)
import logging
from pathlib import (
    Path,
)
from tempfile import (
    NamedTemporaryFile,
)
from typing import (
    Iterable,
)

LOG = logging.getLogger(__name__)


@dataclass(frozen=True)
class _StrFile:
    file_path: str


@dataclass(frozen=True)
class StrFile:
    _inner: _StrFile

    def read(self) -> PureIter[str]:
        def _new_iter() -> Iterable[str]:
            with open(self._inner.file_path, "r") as file:
                line = file.readline()
                while line:
                    yield line
                    line = file.readline()

        return unsafe_from_cmd(Cmd.from_cmd(_new_iter))

    @staticmethod
    def new(content: PureIter[str]) -> Cmd[StrFile]:
        def _action() -> StrFile:
            file = NamedTemporaryFile("w", delete=False)
            file.writelines(content)
            file.close()
            return StrFile(_StrFile(file.name))

        return Cmd.from_cmd(_action)

    @staticmethod
    def save(content: Stream[str]) -> Cmd[StrFile]:
        def _action(act: CmdUnwrapper) -> StrFile:
            file = NamedTemporaryFile("w", delete=False)
            LOG.debug("Saving stream into %s", file.name)
            file.writelines(act.unwrap(content.unsafe_to_iter()))
            file.close()
            return StrFile(_StrFile(file.name))

        return new_cmd(_action)

    @classmethod
    def freeze(cls, file_path: Path) -> Cmd[StrFile]:
        def _action() -> Iterable[str]:
            with open(file_path.as_posix(), "r") as file:
                file.seek(0)
                line = file.readline()
                while line:
                    yield line
                    line = file.readline()

        start = Cmd.from_cmd(lambda: LOG.debug("Freezing file"))
        end = Cmd.from_cmd(lambda: LOG.debug("Freezing completed!"))
        stream = unsafe_build_stream(Cmd.from_cmd(_action))
        return start + cls.save(stream).bind(lambda f: end.map(lambda _: f))
