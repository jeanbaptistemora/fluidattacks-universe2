from db_model.groups.types import (
    Group,
)
from db_model.vulnerabilities.types import (
    VulnerabilitiesConnection,
)
from dynamodb.types import (
    PageInfo,
)
from graphql import (
    GraphQLResolveInfo,
)
from typing import (
    Any,
)


async def resolve(
    _parent: Group,
    _info: GraphQLResolveInfo,
    **_kwargs: Any,
) -> VulnerabilitiesConnection:
    return VulnerabilitiesConnection(
        edges=tuple(),
        page_info=PageInfo(has_next_page=False, end_cursor=""),
    )
