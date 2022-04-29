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
) -> str:
    group_name: str = get_key_or_fallback(parent)
    execution_id = str(parent["execution_id"])

    return await forces_domain.get_log_execution(group_name, execution_id)
