from .schema import (
    FINDING,
)
from batch.types import (
    Job,
)
from dataloaders import (
    Dataloaders,
)
from db_model.findings.types import (
    Finding,
)
from db_model.roots.types import (
    GitRoot,
)
from decorators import (
    enforce_group_level_auth_async,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
import machine.jobs
from machine.jobs import (
    get_finding_code_from_title,
)
from typing import (
    Optional,
)


@FINDING.field("machineJobs")
@enforce_group_level_auth_async
async def resolve(
    parent: Finding,
    info: GraphQLResolveInfo,
    **_: None,
) -> list[Job]:
    loaders: Dataloaders = info.context.loaders
    finding_code: Optional[str] = get_finding_code_from_title(parent.title)
    root_nicknames: dict[str, str] = {
        root.id: root.state.nickname
        for root in await loaders.group_roots.load(parent.group_name)
        if isinstance(root, GitRoot)
    }
    if finding_code is None:
        jobs: list[Job] = []
    else:
        jobs = await machine.jobs.list_(
            finding_code=finding_code,
            group_roots=root_nicknames,
        )

    return jobs
