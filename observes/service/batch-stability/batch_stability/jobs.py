# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from batch_stability import (
    report,
)
from batch_stability.client import (
    JobsClient,
)
import boto3
from enum import (
    Enum,
)
from fa_purity import (
    Cmd,
    Stream,
)
from fa_purity.pure_iter.factory import (
    from_flist,
)
from fa_purity.stream.transform import (
    consume,
)
from mypy_boto3_batch.type_defs import (
    JobSummaryTypeDef,
)

QUEUES = frozenset(
    [
        "small",
        "medium",
        "large",
        "clone",
    ]
)


class Product(Enum):
    OBSERVES = "observes"


def observes_jobs(queue: str, last_hours: int) -> Stream[JobSummaryTypeDef]:
    client = JobsClient(boto3.client("batch", region_name="us-east-1"), queue)
    return (
        client.list_jobs("FAILED")
        .transform(lambda s: report.observes_filter(s))
        .transform(lambda s: report.time_filter(s, last_hours))
    )


def observes_cancelled(
    queue: str, last_hours: int, dry_run: bool
) -> Cmd[None]:
    jobs = observes_jobs(queue, last_hours)
    cmds = report.cancelled_jobs(jobs).map(lambda i: report.report(i, dry_run))
    cmds_2 = report.unstarted_jobs(jobs).map(
        lambda i: report.report(i, dry_run)
    )
    return consume(cmds) + consume(cmds_2)


def observes_failures(queue: str, last_hours: int, dry_run: bool) -> Cmd[None]:
    jobs = observes_jobs(queue, last_hours)
    cmds = report.failed_jobs(jobs).map(lambda i: report.report(i, dry_run))
    return consume(cmds)


def report_cancelled(
    product: Product, last_hours: int, dry_run: bool
) -> Cmd[None]:
    if product is Product.OBSERVES:
        return (
            from_flist(tuple(QUEUES))
            .map(lambda q: observes_cancelled(q, last_hours, dry_run))
            .reduce(Cmd.__add__, Cmd.from_cmd(lambda: None))
        )
    raise Exception("Invalid product")


def report_failures(
    product: Product, last_hours: int, dry_run: bool
) -> Cmd[None]:
    if product is Product.OBSERVES:
        return (
            from_flist(tuple(QUEUES))
            .map(lambda q: observes_failures(q, last_hours, dry_run))
            .reduce(Cmd.__add__, Cmd.from_cmd(lambda: None))
        )
    raise Exception("Invalid product")
