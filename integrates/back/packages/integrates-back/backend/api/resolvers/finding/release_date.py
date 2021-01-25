# Standard
from typing import cast, Dict

# Third party
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend.filters import finding as finding_filters
from backend.typing import Finding


async def resolve(
    parent: Dict[str, Finding],
    _info: GraphQLResolveInfo,
    **_kwargs: None
) -> str:
    release_date = finding_filters.get_approval_date(parent)

    return cast(str, release_date)
