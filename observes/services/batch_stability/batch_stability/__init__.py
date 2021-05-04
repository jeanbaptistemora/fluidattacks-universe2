# Standard library
from datetime import (
    datetime,
)
from itertools import (
    chain,
)
from typing import (
    Any,
    Iterator,
    List,
)

# Third party libraries
import boto3
import bugsnag

# Constants
HOUR: float = 3600.0
NOW: float = datetime.utcnow().timestamp()

# Side effects
bugsnag.configure(
    api_key="13748c4b5f6807a89f327c0f54fe6c7a",
    asynchronous=False,
    send_code=False,
)


class BatchSucceededJob(Exception):
    pass


class BatchFailedJob(Exception):
    pass


def report_msg(
    container: str,
    identifier: str,
    name: str,
    reason: str,
    success: bool,
) -> None:
    arguments = dict(
        exception=(BatchSucceededJob if success else BatchFailedJob)(name),
        extra=dict(
            container=container,
            identifier=identifier,
            reason=reason,
        ),
        grouping_hash=name,
    )

    print(arguments)
    bugsnag.start_session()
    bugsnag.notify(**arguments)


def get_jobs(paginator: Any, queues: List[str]) -> Iterator[Any]:
    return chain.from_iterable(
        [
            paginator.paginate(
                jobQueue=queue,
                jobStatus="FAILED",
            )
            for queue in queues
        ]
    )


def report_queues(queues: List[str], last_hours: int) -> None:
    client = boto3.client("batch")
    paginator = client.get_paginator("list_jobs")
    jobs = get_jobs(paginator, queues)
    for job in jobs:
        for job_summary in job["jobSummaryList"]:
            # Timestamps from aws come in miliseconds
            stopped_at: float = job_summary["stoppedAt"] / 1000
            if stopped_at > NOW - last_hours * HOUR:
                report_msg(
                    container=str(job_summary.get("container")),
                    identifier=job_summary["jobId"],
                    name=job_summary["jobName"],
                    reason=job_summary["statusReason"],
                    success=job_summary["status"] == "SUCCEEDED",
                )


def report_default_queues(base_name: str, last_hours: int) -> None:
    suffixes = ["_now", "_soon", "_later"]
    report_queues([f"{base_name}{suffix}" for suffix in suffixes], last_hours)
