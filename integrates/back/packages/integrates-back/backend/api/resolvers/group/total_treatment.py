# Standard
from typing import cast

# Third party
import simplejson as json
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend.decorators import require_integrates
from backend.typing import Project as Group


@require_integrates
async def resolve(
    parent: Group,
    _info: GraphQLResolveInfo,
    **_kwargs: None
) -> object:
    total_treatment: str = cast(str, parent.get('total_treatment', {}))

    return json.dumps(total_treatment, use_decimal=True)
