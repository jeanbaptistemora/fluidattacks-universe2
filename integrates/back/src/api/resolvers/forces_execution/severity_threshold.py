from .schema import (
    FORCES_EXECUTION,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from typing import (
    Any,
)


@FORCES_EXECUTION.field("severityThreshold")
def resolve(
    parent: dict[str, Any],
    _info: GraphQLResolveInfo,
    **_kwargs: None,
) -> float:
    return (
        float(str(parent["severity_threshold"]))
        if parent.get("severity_threshold")
        else float(0.0)
    )
