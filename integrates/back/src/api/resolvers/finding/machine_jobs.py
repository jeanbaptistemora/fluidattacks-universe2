from batch.types import (
    Job,
)
from db_model.findings.types import (
    Finding,
)
from db_model.roots.types import (
    GitRootItem,
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
    Dict,
    List,
    Optional,
)


@enforce_group_level_auth_async
async def resolve(
    parent: Finding,
    info: GraphQLResolveInfo,
    **_: None,
) -> List[Job]:
    finding_code: Optional[str] = get_finding_code_from_title(parent.title)
    root_nicknames: Dict[str, str] = {
        root.id: root.state.nickname
        for root in await info.context.loaders.group_roots.load(
            parent.group_name
        )
        if isinstance(root, GitRootItem)
    }
    if finding_code is None:
        jobs: List[Job] = []
    else:
        jobs = await machine.jobs.list_(
            finding_code=finding_code,
            group_roots=root_nicknames,
        )

    return jobs
