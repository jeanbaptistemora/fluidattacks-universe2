# Standard
from typing import cast, Dict

# Third party
import simplejson as json
from ariadne.utils import convert_kwargs_to_snake_case
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend.typing import Project as Group


@convert_kwargs_to_snake_case
async def resolve(
    parent: Group,
    _info: GraphQLResolveInfo,
    **_kwargs: str
) -> str:
    total_treatment: Dict[str, int] = cast(
        Dict[str, int],
        parent['total_treatment']
    )

    return json.dumps(total_treatment, use_decimal=True)
