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
    Dict,
)


async def resolve(
    parent: Dict[str, Any], _info: GraphQLResolveInfo, **_kwargs: None
) -> Dict[str, Any]:
    group_name: str = get_key_or_fallback(parent)
    execution_id = str(parent["execution_id"])
    vulnerabilities: Dict[str, Any] = parent.get("vulnerabilities", {})
    return {
        **vulnerabilities,
        **await forces_domain.get_vulns_execution(group_name, execution_id),
    }
