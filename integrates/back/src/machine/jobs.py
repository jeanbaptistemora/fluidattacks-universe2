from batch.dal import (
    Job,
    JobStatus,
    list_queues_jobs,
)
from skims_sdk import (
    get_queue_for_finding,
)
from typing import (
    List,
    NamedTuple,
)


class JobArguments(NamedTuple):
    # pylint: disable=inherit-non-class, too-few-public-methods
    group_name: str
    finding_code: str
    root_nickname: str


def parse_name(name: str) -> JobArguments:
    tokens = name.split("-", maxsplit=3)
    return JobArguments(
        finding_code=tokens[2],
        group_name=tokens[1],
        root_nickname=tokens[3],
    )


async def list_(
    *,
    finding_code: str,
    group_name: str,
    include_non_urgent: bool = False,
    include_urgent: bool = False,
    statuses: List[JobStatus],
) -> List[Job]:
    queues: List[str] = []
    if include_non_urgent:
        queues.append(get_queue_for_finding(finding_code, urgent=False))
    if include_urgent:
        queues.append(get_queue_for_finding(finding_code, urgent=True))

    jobs = await list_queues_jobs(
        filters=(
            lambda job: parse_name(job.name).finding_code == finding_code,
            lambda job: parse_name(job.name).group_name == group_name,
        ),
        queues=queues,
        statuses=statuses,
    )

    return sorted(
        jobs,
        key=lambda job: job.created_at or 0,
        reverse=True,
    )
