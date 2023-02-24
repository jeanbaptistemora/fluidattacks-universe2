from .schema import (
    FORCES_EXECUTION,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from typing import (
    Any,
)


@FORCES_EXECUTION.field("gracePeriod")
def resolve(
    parent: dict[str, Any],
    _info: GraphQLResolveInfo,
    **_kwargs: None,
) -> int:
    return (
        int(str(parent["grace_period"])) if parent.get("grace_period") else 0
    )
