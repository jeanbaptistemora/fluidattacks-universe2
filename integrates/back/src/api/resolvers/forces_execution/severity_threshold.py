from db_model.forces.types import (
    ForcesExecution,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from typing import (
    Any,
    Union,
)


async def resolve(
    parent: Union[dict[str, Any], ForcesExecution],
    _info: GraphQLResolveInfo,
    **_kwargs: None,
) -> float:
    if isinstance(parent, dict):
        if "severity_threshold" in parent:
            return float(str(parent["severity_threshold"]))
        return 0.0
    return parent.severity_threshold if parent.severity_threshold else 0.0
