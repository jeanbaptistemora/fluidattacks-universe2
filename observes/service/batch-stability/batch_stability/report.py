from batch_stability.errors import (
    BatchCancelledJob,
    BatchFailedJob,
    BatchUnstartedJob,
)
from dataclasses import (
    dataclass,
)
from fa_purity import (
    Stream,
)
from mypy_boto3_batch.type_defs import (
    JobSummaryTypeDef,
)


@dataclass(frozen=True)
class FailReport:
    container: str
    identifier: str
    name: str
    reason: str
    exception: Exception


def _to_report(raw: JobSummaryTypeDef, exception: Exception) -> FailReport:
    return FailReport(
        str(raw.get("container")),
        raw["jobId"],
        raw["jobName"],
        raw["statusReason"],
        exception,
    )


def cancelled_jobs(jobs: Stream[JobSummaryTypeDef]) -> Stream[FailReport]:
    return jobs.filter(
        lambda j: bool(not j.get("startedAt") and not j.get("stoppedAt"))
    ).map(lambda j: _to_report(j, BatchCancelledJob(j["jobName"])))


def unstarted_jobs(jobs: Stream[JobSummaryTypeDef]) -> Stream[FailReport]:
    return jobs.filter(
        lambda j: bool(not j.get("startedAt") and j.get("stoppedAt"))
    ).map(lambda j: _to_report(j, BatchUnstartedJob(j["jobName"])))


def failed_jobs(jobs: Stream[JobSummaryTypeDef]) -> Stream[FailReport]:
    return jobs.filter(
        lambda j: bool(j.get("startedAt") and j.get("stoppedAt"))
    ).map(lambda j: _to_report(j, BatchFailedJob(j["jobName"])))
