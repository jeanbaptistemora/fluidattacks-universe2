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
    get_key_or_fallback,
)
from typing import (
    cast,
)


async def resolve(
    parent: ForcesExecution, _info: GraphQLResolveInfo, **_kwargs: None
) -> ExecutionVulnerabilities:
    group_name: str = get_key_or_fallback(parent)
    execution_id: str = parent["execution_id"]
    vulnerabilities: ExecutionVulnerabilities = cast(
        ExecutionVulnerabilities, parent.get("vulnerabilities", {})
    )

    return {
        **vulnerabilities,
        **await forces_domain.get_vulns_execution(group_name, execution_id),
    }
