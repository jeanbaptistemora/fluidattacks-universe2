import boto3
import bugsnag
from datetime import (
    datetime,
)
from itertools import (
    chain,
)
from mypy_boto3_batch import (
    BatchClient,
    ListJobsPaginator,
)
from mypy_boto3_batch.type_defs import (
    JobSummaryTypeDef,
    ListJobsResponseTypeDef,
)
from os import (
    environ,
)
from typing import (
    Iterator,
    List,
    Type,
)

# Constants
__version__ = "1.0.0"
HOUR: float = 3600.0
NOW: float = datetime.utcnow().timestamp()
NOTIFIER_KEY = environ.get("bugsnag_notifier_key", "")

# Side effects
bugsnag.configure(  # type: ignore[no-untyped-call]
    api_key=NOTIFIER_KEY,
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
        extra=dict(
            container=container,
            identifier=identifier,
            reason=reason,
        ),
        grouping_hash=name,
    )

    print(arguments)
    bugsnag.start_session()  # type: ignore[no-untyped-call]
    bugsnag.notify(exception(name), **arguments)


def _report_job(
    job_summary: JobSummaryTypeDef, exception: Type[Exception]
) -> None:
    _report_status(
        container=str(job_summary.get("container")),
        identifier=job_summary["jobId"],
        name=job_summary["jobName"],
        reason=job_summary["statusReason"],
        exception=exception,
    )


def _get_jobs(
    paginator: ListJobsPaginator, queues: List[str]
) -> Iterator[ListJobsResponseTypeDef]:
    return chain.from_iterable(
        [
            paginator.paginate(
                jobQueue=queue,
                jobStatus="FAILED",
            )
            for queue in queues
        ]
    )


def _get_jobs_summaries(
    paginator: ListJobsPaginator, queues: List[str]
) -> Iterator[JobSummaryTypeDef]:
    jobs = _get_jobs(paginator, queues)
    for job in jobs:
        for job_summary in job["jobSummaryList"]:
            if job_summary["status"] != "SUCCEEDED":
                yield job_summary


def _is_cancelled(job_summary: JobSummaryTypeDef, last_hours: int) -> bool:
    # Timestamps from aws come in miliseconds
    created_at: float = job_summary["createdAt"] / 1000
    if created_at > NOW - last_hours * HOUR:
        return not job_summary.get("startedAt") and not job_summary.get(
            "stoppedAt"
        )
    return False


def _is_fail(job_summary: JobSummaryTypeDef, last_hours: int) -> bool:
    if job_summary.get("startedAt") and job_summary.get("stoppedAt"):
        stopped_at: float = job_summary["stoppedAt"] / 1000
        if stopped_at > NOW - last_hours * HOUR:
            return True
    return False


def _is_unstarted(job_summary: JobSummaryTypeDef, last_hours: int) -> bool:
    if not job_summary.get("startedAt") and job_summary.get("stoppedAt"):
        stopped_at: float = job_summary["stoppedAt"] / 1000
        if stopped_at > NOW - last_hours * HOUR:
            return True
    return False


def report_cancelled(queues: List[str], last_hours: int) -> None:
    client: BatchClient = boto3.client("batch")
    paginator = client.get_paginator("list_jobs")
    jobs = _get_jobs_summaries(paginator, queues)
    for job_summary in jobs:
        if _is_cancelled(job_summary, last_hours):
            _report_job(job_summary, BatchCancelledJob)


def report_failures(queues: List[str], last_hours: int) -> None:
    client: BatchClient = boto3.client("batch")
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
