from __future__ import (
    annotations,
)

from dataclasses import (
    dataclass,
)
from fa_purity import (
    Cmd,
    Result,
    Stream,
)
from fa_purity.cmd.core import (
    CmdUnwrapper,
    new_cmd,
)
from fa_purity.stream import (
    factory as StreamFactory,
)
import logging
import requests
from requests.exceptions import (
    HTTPError,
    StreamConsumedError,
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

LOG = logging.getLogger(__name__)
_T = TypeVar("_T")


@dataclass(frozen=True)
class _BinFile:
    file_path: str


@dataclass(frozen=True)
class BinFile:
    _inner: _BinFile

    def unsafe_transform(self, function: Callable[[IO[bytes]], _T]) -> Cmd[_T]:
        """
        This method can be unsafe.
        - Do not extract file name from the IO file obj. IO file name is private.
        - Ensure it will be reopened in read mode only.
        """

        def _action() -> _T:
            with open(self._inner.file_path, "rb") as file:
                return function(file)

        return Cmd.from_cmd(_action)

    @staticmethod
    def save(content: Stream[bytes]) -> Cmd[BinFile]:
        def _action(act: CmdUnwrapper) -> BinFile:
            file = NamedTemporaryFile("wb", delete=False)
            LOG.debug("Saving bin file into %s", file.name)
            file.writelines(act.unwrap(content.unsafe_to_iter()))
            file.close()
            return BinFile(_BinFile(file.name))

        return new_cmd(_action)

    @classmethod
    def from_url(cls, url: str) -> Cmd[Result[BinFile, HTTPError]]:
        def _action(act: CmdUnwrapper) -> Result[BinFile, HTTPError]:
            LOG.debug("Getting %s", url)
            with requests.get(url, stream=True) as response:
                try:
                    response.raise_for_status()

                    def _data_iter() -> Iterable[bytes]:
                        try:
                            return (bytes(i) for i in response.iter_content(chunk_size=8192))  # type: ignore[misc]
                        except StreamConsumedError:  # type: ignore[misc]
                            return iter([])

                    stream = StreamFactory.unsafe_from_cmd(
                        Cmd.from_cmd(_data_iter)
                    )
                    return Result.success(act.unwrap(cls.save(stream)))
                except HTTPError as err:  # type: ignore[misc]
                    return Result.failure(err)

        return new_cmd(_action)
