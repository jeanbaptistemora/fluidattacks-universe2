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


@FORCES_EXECUTION.field("log")
async def resolve(
    parent: dict[str, Any],
    _info: GraphQLResolveInfo,
    **_kwargs: None,
) -> str:
    group_name = str(parent["group_name"])
    execution_id = str(parent["execution_id"])

    return await forces_domain.get_log_execution(group_name, execution_id)
