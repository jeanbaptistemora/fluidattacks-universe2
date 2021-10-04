from batch.dal import (
    Job,
    JobStatus,
)
from db_model.findings.types import (
    Finding,
)
from decorators import (
    enforce_group_level_auth_async,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
import machine.jobs
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
    parent: Finding,
    _info: GraphQLResolveInfo,
    **_: None,
) -> List[Dict[str, Any]]:
    # pylint: disable=unsubscriptable-object
    finding_code: Optional[str] = get_finding_code_from_title(parent.title)
    if finding_code is None:
        jobs: List[Job] = []
    else:
        jobs = await machine.jobs.list_(
            finding_code=finding_code,
            group_name=parent.group_name,
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
