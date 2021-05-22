from typing import cast

import simplejson as json
from graphql.type.definition import GraphQLResolveInfo

from custom_types import Project as Group
from decorators import require_integrates


@require_integrates
async def resolve(
    parent: Group, _info: GraphQLResolveInfo, **_kwargs: None
) -> object:
    total_treatment: str = cast(str, parent.get("total_treatment", {}))
    return json.dumps(total_treatment, use_decimal=True)
