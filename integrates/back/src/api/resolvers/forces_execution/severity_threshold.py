from .schema import (
    FORCES_EXECUTION,
)
from db_model.forces.types import (
    ForcesExecution,
)
from decimal import (
    Decimal,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from typing import (
    Any,
)


@FORCES_EXECUTION.field("severityThreshold")
async def resolve(
    parent: dict[str, Any] | ForcesExecution,
    _info: GraphQLResolveInfo,
    **_kwargs: None,
) -> float | Decimal:
    if isinstance(parent, dict):
        if parent.get("severity_threshold"):
            return float(str(parent["severity_threshold"]))
        return 0.0
    return parent.severity_threshold if parent.severity_threshold else 0.0
