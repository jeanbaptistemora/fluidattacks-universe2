from custom_types import (
    Finding,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils import (
    findings as findings_utils,
)
from typing import (
    cast,
    Dict,
)


async def resolve(
    parent: Dict[str, Finding], _info: GraphQLResolveInfo, **_kwargs: None
) -> str:
    release_date = findings_utils.get_approval_date(parent)
    return cast(str, release_date)
