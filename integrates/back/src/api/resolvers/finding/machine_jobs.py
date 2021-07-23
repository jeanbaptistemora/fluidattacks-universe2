from batch.dal import (
    Job,
    JobStatus,
    list_queues_jobs,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from skims_sdk import (
    get_finding_code_from_title,
    get_queue_for_finding,
)
from typing import (
    Any,
    Dict,
    List,
    Optional,
)


async def resolve(
    parent: Dict[str, str],
    info: GraphQLResolveInfo,
    **_: None,
) -> List[Dict[str, Any]]:
    finding = await info.context.loaders.finding.load(parent["id"])
    finding_title: str = finding["title"]
    finding_code: Optional[str] = get_finding_code_from_title(finding_title)

    if finding_code is None:
        jobs: List[Job] = []
    else:
        jobs = await list_queues_jobs(
            queues=[
                get_queue_for_finding(finding_code, urgent=True),
                get_queue_for_finding(finding_code, urgent=False),
            ],
            statuses=list(JobStatus),
        )

    return [job._asdict() for job in jobs]
