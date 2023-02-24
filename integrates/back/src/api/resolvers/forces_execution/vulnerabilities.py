from .schema import (
    FORCES_EXECUTION,
)
from forces import (
    domain as forces_domain,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from typing import (
    Any,
)


@FORCES_EXECUTION.field("vulnerabilities")
async def resolve(
    parent: dict[str, Any],
    _info: GraphQLResolveInfo,
    **_kwargs: None,
) -> dict[str, Any]:
    group_name = str(parent["group_name"])
    execution_id = str(parent["execution_id"])
    vulnerabilities = parent.get("vulnerabilities", {})

    return {
        **vulnerabilities,
        **await forces_domain.get_vulns_execution(group_name, execution_id),
    }
