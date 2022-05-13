from batch_stability.errors import (
    BatchCancelledJob,
    BatchFailedJob,
    BatchUnknownExitCode,
    BatchUnstartedJob,
)
import bugsnag
from dataclasses import (
    dataclass,
)
from datetime import (
    datetime,
)
from fa_purity import (
    Cmd,
    Maybe,
    Stream,
)
from mypy_boto3_batch.type_defs import (
    JobSummaryTypeDef,
)

HOUR: float = 3600.0
NOW: float = datetime.utcnow().timestamp()


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


def _failed_job_exception(job: JobSummaryTypeDef) -> Exception:
    name = job["jobName"]
    exit_code = Maybe.from_optional(job.get("container")).bind_optional(
        lambda c: c.get("exitCode")
    )
    return exit_code.map(lambda _: BatchFailedJob(name)).value_or(
        BatchUnknownExitCode(name)
    )


def failed_jobs(jobs: Stream[JobSummaryTypeDef]) -> Stream[FailReport]:
    return jobs.filter(
        lambda j: bool(j.get("startedAt") and j.get("stoppedAt"))
    ).map(lambda j: _to_report(j, _failed_job_exception(j)))


def time_filter(
    jobs: Stream[JobSummaryTypeDef], last_hours: int
) -> Stream[JobSummaryTypeDef]:
    def _filter(job: JobSummaryTypeDef) -> bool:
        # Timestamps from aws come in miliseconds
        job_date = (
            Maybe.from_optional(job.get("stoppedAt")).value_or(
                job["createdAt"]
            )
            / 1000
        )  # unit: seconds
        return job_date > NOW - last_hours * HOUR

    return jobs.filter(_filter)


def observes_filter(
    jobs: Stream[JobSummaryTypeDef],
) -> Stream[JobSummaryTypeDef]:
    return jobs.filter(lambda j: "observes" in j["jobName"])


def report(item: FailReport, dry_run: bool) -> Cmd[None]:
    def _action() -> None:
        arguments = dict(
            extra=dict(
                container=item.container,
                identifier=item.identifier,
                reason=item.reason,
            ),
            grouping_hash=item.name,
        )
        if dry_run:
            print(type(item.exception))
            print(item.exception)
            print(arguments)
        else:
            bugsnag.start_session()  # type: ignore[no-untyped-call]
            bugsnag.notify(item.exception, **arguments)

    return Cmd.from_cmd(_action)
