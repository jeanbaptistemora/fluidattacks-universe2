from __future__ import (
    annotations,
)

from dataclasses import (
    dataclass,
)
from enum import (
    Enum,
)
from fa_purity import (
    Cmd,
    FrozenList,
    Maybe,
)
from fa_purity.pure_iter import (
    factory as PIterFactory,
)
import logging
import subprocess
from subprocess import (
    Popen,
)
from typing import (
    Callable,
    Generic,
    IO,
    Optional,
    TypeVar,
)

LOG = logging.getLogger(__name__)
_A = TypeVar("_A", bytes, str)


class StdValues(Enum):
    PIPE = subprocess.PIPE
    DEVNULL = subprocess.DEVNULL


class Stdout(Enum):
    STDOUT = subprocess.STDOUT


@dataclass(frozen=True)
class Subprocess(Generic[_A]):
    cmd: FrozenList[str]
    stdin: StdValues | IO[_A] | None
    stdout: StdValues | IO[_A] | None
    stderr: StdValues | Stdout | IO[_A] | None


def _normalize(
    item: StdValues | Stdout | IO[_A] | None,
) -> int | IO[_A] | None:
    if isinstance(item, StdValues):
        return item.value
    if isinstance(item, Stdout):
        return item.value
    return item


@dataclass(frozen=True)
class RunningSubprocess(Generic[_A]):
    _process: Popen[_A]
    stdin: IO[_A] | None
    stdout: IO[_A] | None
    stderr: IO[_A] | None

    @staticmethod
    def run(item: Subprocess[bytes]) -> Cmd[RunningSubprocess[bytes]]:
        def _action() -> RunningSubprocess[bytes]:
            process = Popen(
                item.cmd,
                stdin=_normalize(item.stdin),
                stdout=_normalize(item.stdout),
                stderr=_normalize(item.stderr),
            )
            return RunningSubprocess(
                process, process.stdin, process.stdout, process.stderr
            )

        return Cmd.from_cmd(_action)

    @staticmethod
    def run_universal_newlines(
        item: Subprocess[str],
    ) -> Cmd[RunningSubprocess[str]]:
        def _action() -> RunningSubprocess[str]:
            process = Popen(
                item.cmd,
                stdin=_normalize(item.stdin),
                stdout=_normalize(item.stdout),
                stderr=_normalize(item.stderr),
                universal_newlines=True,
            )
            return RunningSubprocess(
                process, process.stdin, process.stdout, process.stderr
            )

        return Cmd.from_cmd(_action)

    def poll(self) -> Cmd[Optional[int]]:
        return Cmd.from_cmd(self._process.poll)

    def wait(self, timeout: Optional[float]) -> Cmd[int]:
        return Cmd.from_cmd(lambda: self._process.wait(timeout))


def chain(
    run: Callable[[Subprocess[_A]], Cmd[RunningSubprocess[_A]]],
    cmds: FrozenList[Subprocess[_A]],
) -> Maybe[Cmd[RunningSubprocess[_A]]]:
    def _chain(
        previous: Cmd[RunningSubprocess[_A]] | None, current: Subprocess[_A]
    ) -> Cmd[RunningSubprocess[_A]]:
        if previous is None:
            return run(
                Subprocess(
                    current.cmd, StdValues.PIPE, current.stdout, current.stderr
                )
            )
        return previous.map(
            lambda r: Subprocess(
                current.cmd, StdValues.PIPE, r.stdin, current.stderr
            )
        ).bind(run)

    result = PIterFactory.from_flist(cmds[::-1]).reduce(_chain, None)
    return Maybe.from_optional(result)
