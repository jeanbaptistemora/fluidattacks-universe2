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
from fa_purity.cmd import (
    unsafe_unwrap,
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
from tempfile import (
    NamedTemporaryFile,
)
from typing import (
    Callable,
    IO,
    Iterable,
    TypeVar,
)

LOG = logging.getLogger(__name__)


@dataclass(frozen=True)
class _TempReadOnlyFile:
    file_path: str


_T = TypeVar("_T")


@dataclass(frozen=True)
class TempReadOnlyFile:
    _inner: _TempReadOnlyFile

    def over_binary(self, transform: Callable[[IO[bytes]], _T]) -> _T:
        def _action() -> _T:
            with open(self._inner.file_path, "rb") as file:
                return transform(file)

        # even if opening a file is a Cmd
        # unsafe_unwrap is safe to use since
        # the file is supposed to be immutable
        # and therefore return the same output
        return unsafe_unwrap(Cmd.from_cmd(_action))

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
            file_object = NamedTemporaryFile("w", delete=False)
            file_object.writelines(content)
            file_object.close()
            return TempReadOnlyFile(_TempReadOnlyFile(file_object.name))

        return Cmd.from_cmd(_action)

    @staticmethod
    def from_cmd(
        write_cmd: Callable[[IO[str]], Cmd[None]]
    ) -> Cmd[TempReadOnlyFile]:
        """
        `write_cmd` initializes the file content. It has write-only access to file
        """

        def _action(act: CmdUnwrapper) -> TempReadOnlyFile:
            file_object = NamedTemporaryFile("w", delete=False)
            act.unwrap(write_cmd(file_object))
            file_object.close()
            return TempReadOnlyFile(_TempReadOnlyFile(file_object.name))

        return new_cmd(_action)

    @staticmethod
    def save(content: Stream[str]) -> Cmd[TempReadOnlyFile]:
        def _action(act: CmdUnwrapper) -> TempReadOnlyFile:
            file_object = NamedTemporaryFile("w", delete=False)
            LOG.debug("Saving stream into %s", file_object.name)
            file_object.writelines(act.unwrap(content.unsafe_to_iter()))
            file_object.close()
            return TempReadOnlyFile(_TempReadOnlyFile(file_object.name))

        return new_cmd(_action)

    @classmethod
    def freeze(cls, file_path: str) -> Cmd[TempReadOnlyFile]:
        def _action() -> Iterable[str]:
            with open(file_path, "r") as file:
                file.seek(0)
                line = file.readline()
                while line:
                    yield line
                    line = file.readline()

        start = Cmd.from_cmd(lambda: LOG.debug("Freezing file"))
        end = Cmd.from_cmd(lambda: LOG.debug("Freezing completed!"))
        stream = unsafe_build_stream(Cmd.from_cmd(_action))
        return start + cls.save(stream).bind(lambda f: end.map(lambda _: f))
