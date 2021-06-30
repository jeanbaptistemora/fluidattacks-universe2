from custom_types import (
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
) -> str:
    group_name: str = cast(str, resolve_kwargs(parent))
    execution_id: str = cast(str, parent["execution_id"])

    return cast(
        str, await forces_domain.get_log_execution(group_name, execution_id)
    )
