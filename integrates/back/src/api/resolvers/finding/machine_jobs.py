from batch.dal import (
    Job,
    JobStatus,
)
from decorators import (
    enforce_group_level_auth_async,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
import machine.jobs
from newutils.utils import (
    get_key_or_fallback,
)
from skims_sdk import (
    get_finding_code_from_title,
)
from typing import (
    Any,
    Dict,
    List,
    Optional,
)


@enforce_group_level_auth_async
async def resolve(
    parent: Dict[str, str],
    info: GraphQLResolveInfo,
    **_: None,
) -> List[Dict[str, Any]]:
    group_name: str = get_key_or_fallback(parent)
    finding = await info.context.loaders.finding.load(parent["id"])
    finding_title: str = finding["title"]
    finding_code: Optional[str] = get_finding_code_from_title(finding_title)

    if finding_code is None:
        jobs: List[Job] = []
    else:
        jobs = await machine.jobs.list_(
            finding_code=finding_code,
            group_name=group_name,
            include_non_urgent=True,
            include_urgent=True,
            statuses=list(JobStatus),
        )

    return [
        dict(
            **job._asdict(),
            root_nickname=machine.jobs.parse_name(job.name).root_nickname,
        )
        for job in jobs
    ]
