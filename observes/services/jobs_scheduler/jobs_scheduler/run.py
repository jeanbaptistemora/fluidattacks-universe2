# pylint: skip-file
import logging
from returns.io import (
    impure,
)
from returns.maybe import (
    Maybe,
)
import subprocess
from typing import (
    List,
)

LOG = logging.getLogger(__name__)


class CmdFailed(Exception):
    pass


@impure
def run_command(cmd: List[str]) -> None:
    LOG.info("Executing: %s", cmd)
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
        print(line, end="")
    if proc.returncode:
        error = CmdFailed(cmd)
        LOG.error("%s: %s", cmd, error)
