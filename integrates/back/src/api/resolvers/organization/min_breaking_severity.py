from db_model.organization.types import (
    Organization,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from typing import (
    Any,
    Dict,
    Union,
)


async def resolve(
    parent: Union[Organization, dict[str, Any]],
    _info: GraphQLResolveInfo,
    **_kwargs: Dict[str, str],
) -> float:
    if isinstance(parent, dict):
        if "min_breaking_severity" in parent:
            return parent["min_breaking_severity"]
    else:
        if parent.min_breaking_severity:
            return parent.min_breaking_severity
    return 0.0
