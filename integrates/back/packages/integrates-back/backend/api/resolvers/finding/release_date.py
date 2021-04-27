# Standard
from typing import cast, Dict

# Third party
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend.typing import Finding
from newutils import findings as findings_utils


async def resolve(
    parent: Dict[str, Finding],
    _info: GraphQLResolveInfo,
    **_kwargs: None
) -> str:
    release_date = findings_utils.get_approval_date(parent)

    return cast(str, release_date)
