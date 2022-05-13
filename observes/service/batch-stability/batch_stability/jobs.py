from batch_stability import (
    report,
)
from batch_stability.client import (
    JobsClient,
)
import boto3
from fa_purity import (
    Stream,
)
from mypy_boto3_batch.type_defs import (
    JobSummaryTypeDef,
)


def observes_jobs(queue: str, last_hours: int) -> Stream[JobSummaryTypeDef]:
    client = JobsClient(boto3.client("batch"), queue)
    return (
        client.list_jobs("FAILED")
        .transform(lambda s: report.observes_filter(s))
        .transform(lambda s: report.time_filter(s, last_hours))
    )
