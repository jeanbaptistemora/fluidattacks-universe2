# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from ._centralize import (
    centralize,
)
import click
from dynamo_etl_conf.jobs import (
    default_executor,
    Jobs,
    run_job,
)
import logging
from typing import (
    NoReturn,
)

LOG = logging.getLogger(__name__)


@click.command()  # type: ignore[misc]
@click.argument(  # type: ignore[misc]
    "job", type=click.Choice([i.name for i in Jobs], case_sensitive=False)
)
def run(job: str) -> NoReturn:
    exe = default_executor()
    run_job(exe, Jobs(job)).compute()


@click.group()  # type: ignore[misc]
def main() -> None:
    # cli group entrypoint
    pass


main.add_command(run)
main.add_command(centralize)
