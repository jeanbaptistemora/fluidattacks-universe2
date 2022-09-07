# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from fa_purity.cmd import (
    Cmd,
)
from fa_purity.frozen import (
    FrozenList,
)
from fa_purity.maybe import (
    Maybe,
)
import logging
import subprocess
from typing import (
    cast,
    TypeVar,
)

LOG = logging.getLogger(__name__)
_T = TypeVar("_T")


class CmdFailed(Exception):
    pass


def _assert_int(item: _T) -> int:
    if isinstance(item, int):
        return item
    raise Exception(f"Expected int type got {type(item)}")


def _action(cmd: FrozenList[str], enable_print: bool) -> None:
    LOG.info("Executing: %s", " ".join(cmd))
    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        shell=False,
        universal_newlines=True,
    )
    stdout = Maybe.from_optional(proc.stdout).unwrap()
    for line in iter(stdout.readline, b""):
        if proc.poll() is not None:
            break
        if enable_print:
            print(line, end="")
    if _assert_int(cast(int, proc.returncode)):
        error = CmdFailed(cmd)
        LOG.error("%s: %s", cmd, error)
    return None


def external_run(cmd: FrozenList[str]) -> Cmd[None]:
    return Cmd.from_cmd(lambda: _action(cmd, True))
