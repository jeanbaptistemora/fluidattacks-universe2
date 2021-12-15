# pylint: skip-file
from __future__ import (
    annotations,
)

from datetime import (
    datetime,
)
from jobs_scheduler.conf import (
    SCHEDULE,
)
from jobs_scheduler.cron import (
    match_cron,
)
from jobs_scheduler.cron_2 import (
    match,
)
import pytz  # type: ignore
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
import utils_logger

utils_logger.configure(
    app_type="tap",
    asynchronous=False,
)
LOG = utils_logger.main_log(__name__)
tz = pytz.timezone("America/Bogota")
NOW = datetime.now(tz)


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


@impure
def main() -> None:
    LOG.info("Now: %s", NOW)
    for cron, jobs in SCHEDULE.items():
        LOG.debug("Evaluating %s.", cron)
        if match.match_cron(cron, NOW):
            for job in jobs:
                run_command(job.replace(".", "-").split())
