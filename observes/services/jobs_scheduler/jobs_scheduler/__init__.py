# pylint: skip-file
# Standard libraries
from __future__ import annotations
import subprocess
from datetime import datetime

# Third party libraries
from returns.io import impure
from returns.maybe import Maybe

# Local libraries
from jobs_scheduler.conf import SCHEDULE
from jobs_scheduler.cron import match_cron
import utils_logger


utils_logger.configure(
    app_type="tap",
    asynchronous=False,
)
LOG = utils_logger.main_log(__name__)
NOW = datetime.now()


class CmdFailed(Exception):
    pass


@impure
def run_command(cmd: str) -> None:
    proc = subprocess.Popen(
        [cmd],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=False,
        universal_newlines=True,
    )
    stdout = Maybe.from_optional(proc.stdout).unwrap()
    stderr = Maybe.from_optional(proc.stderr).unwrap()
    while True:
        line = stdout.readline()
        line2 = stderr.readline()
        if not line and not line2:
            break
        if line:
            print(line, end="")
        if line2:
            print(line2, end="")
    if proc.returncode:
        error = CmdFailed(cmd)
        LOG.error("%s: %s", error, stderr)
        raise error


@impure
def main() -> None:
    for cron, jobs in SCHEDULE.items():
        LOG.debug("Evaluating %s.", cron)
        if match_cron(cron, NOW):
            for job in jobs:
                LOG.info("Executing: %s", job)
                run_command(job.replace(".", "-"))
