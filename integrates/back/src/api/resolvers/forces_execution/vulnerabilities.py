from custom_types import (
    ExecutionVulnerabilities,
    ForcesExecution,
)
from forces import (
    domain as forces_domain,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils.utils import (
    resolve_kwargs,
)
from typing import (
    cast,
)


async def resolve(
    parent: ForcesExecution, _info: GraphQLResolveInfo, **_kwargs: None
) -> ExecutionVulnerabilities:
    group_name: str = cast(str, resolve_kwargs(parent))
    execution_id: str = cast(str, parent["execution_id"])
    vulnerabilities: ExecutionVulnerabilities = cast(
        ExecutionVulnerabilities, parent.get("vulnerabilities", {})
    )

    return {
        **vulnerabilities,
        **await forces_domain.get_vulns_execution(group_name, execution_id),
    }
