import boto3
import bugsnag
from datetime import (
    datetime,
)
from itertools import (
    chain,
)
from typing import (
    Any,
    Dict,
    Iterator,
    List,
    Type,
)

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


class BatchCancelledJob(Exception):
    pass


class BatchUnstartedJob(Exception):
    pass


def _report_status(
    exception: Type[Exception],
    container: str,
    identifier: str,
    name: str,
    reason: str,
) -> None:
    arguments = dict(
        exception=exception(name),
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


def _report_job(
    job_summary: Dict[str, Any], exception: Type[Exception]
) -> None:
    _report_status(
        container=str(job_summary.get("container")),
        identifier=job_summary["jobId"],
        name=job_summary["jobName"],
        reason=job_summary["statusReason"],
        exception=exception,
    )


def _get_jobs(paginator: Any, queues: List[str]) -> Iterator[Any]:
    return chain.from_iterable(
        [
            paginator.paginate(
                jobQueue=queue,
                jobStatus="FAILED",
            )
            for queue in queues
        ]
    )


def _get_jobs_summaries(paginator: Any, queues: List[str]) -> Iterator[Any]:
    jobs = _get_jobs(paginator, queues)
    for job in jobs:
        for job_summary in job["jobSummaryList"]:
            if job_summary["status"] != "SUCCEEDED":
                yield job_summary


def _is_cancelled(job_summary: Dict[str, Any], last_hours: int) -> bool:
    # Timestamps from aws come in miliseconds
    created_at: float = job_summary["createdAt"] / 1000
    if created_at > NOW - last_hours * HOUR:
        return not job_summary.get("startedAt") and not job_summary.get(
            "stoppedAt"
        )
    return False


def _is_fail(job_summary: Dict[str, Any], last_hours: int) -> bool:
    if job_summary.get("startedAt") and job_summary.get("stoppedAt"):
        stopped_at: float = job_summary["stoppedAt"] / 1000
        if stopped_at > NOW - last_hours * HOUR:
            return True
    return False


def _is_unstarted(job_summary: Dict[str, Any], last_hours: int) -> bool:
    if not job_summary.get("startedAt") and job_summary.get("stoppedAt"):
        stopped_at: float = job_summary["stoppedAt"] / 1000
        if stopped_at > NOW - last_hours * HOUR:
            return True
    return False


def report_cancelled(queues: List[str], last_hours: int) -> None:
    client = boto3.client("batch")
    paginator = client.get_paginator("list_jobs")
    jobs = _get_jobs_summaries(paginator, queues)
    for job_summary in jobs:
        if _is_cancelled(job_summary, last_hours):
            _report_job(job_summary, BatchCancelledJob)


def report_failures(queues: List[str], last_hours: int) -> None:
    client = boto3.client("batch")
    paginator = client.get_paginator("list_jobs")
    jobs = _get_jobs_summaries(paginator, queues)
    for job_summary in jobs:
        if _is_fail(job_summary, last_hours):
            _report_job(job_summary, BatchFailedJob)
        elif _is_unstarted(job_summary, last_hours):
            _report_job(job_summary, BatchUnstartedJob)


def default_queues(base_name: str) -> List[str]:
    suffixes = ["_soon", "_later"]
    return [f"{base_name}{suffix}" for suffix in suffixes]
