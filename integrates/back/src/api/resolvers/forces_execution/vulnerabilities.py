from db_model.forces.types import (
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
    Any,
    Union,
)


async def resolve(
    parent: Union[dict[str, Any], ForcesExecution],
    _info: GraphQLResolveInfo,
    **_kwargs: None,
) -> dict[str, Any]:
    if isinstance(parent, dict):
        group_name: str = get_key_or_fallback(parent)
        execution_id = str(parent["execution_id"])
        vulnerabilities = parent.get("vulnerabilities", {})
        return {
            **vulnerabilities,
            **await forces_domain.get_vulns_execution(
                group_name, execution_id
            ),
        }

    group_name = parent.group_name
    execution_id = parent.id
    vulnerabilities = parent.vulnerabilities
    return {
        **vulnerabilities._asdict,
        **await forces_domain.get_vulns_execution(group_name, execution_id),
    }
