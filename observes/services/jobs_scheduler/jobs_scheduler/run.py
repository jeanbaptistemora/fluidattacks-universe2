from enum import (
    Enum,
)
from fa_purity.cmd import (
    Cmd,
)
from fa_purity.maybe import (
    Maybe,
)
import logging
import subprocess
from typing import (
    List,
)

LOG = logging.getLogger(__name__)


class CmdFailed(Exception):
    pass


def _run_command_action(cmd: List[str], dry_run: bool) -> None:
    if not dry_run:
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
            print(line, end="")
        if proc.returncode:
            error = CmdFailed(cmd)
            LOG.error("%s: %s", cmd, error)
        return None
    LOG.info("`%s` will be executed", " ".join(cmd))


def run_job(job: Enum, dry_run: bool) -> Cmd[None]:
    return Cmd.from_cmd(
        lambda: _run_command_action(
            job.value.replace(".", "-").split(), dry_run
        )
    )
