from custom_types import (
    Group,
)
from decorators import (
    require_asm,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
import simplejson as json  # type: ignore


@require_asm
async def resolve(
    parent: Group, _info: GraphQLResolveInfo, **_kwargs: None
) -> object:
    total_treatment: str = parent.get("total_treatment", {})
    return json.dumps(total_treatment, use_decimal=True)
