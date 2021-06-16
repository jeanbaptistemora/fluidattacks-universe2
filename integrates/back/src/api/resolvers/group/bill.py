from bill import (
    domain as bill_domain,
)
from custom_types import (
    Group,
    Historic,
)
from datetime import (
    datetime,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_drills_white,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils import (
    datetime as datetime_utils,
)
from typing import (
    cast,
    Dict,
)


@concurrent_decorators(
    enforce_group_level_auth_async,
    require_drills_white,
)
async def resolve(
    parent: Group, _info: GraphQLResolveInfo, **kwargs: datetime
) -> Dict[str, Historic]:
    group_name: str = cast(str, parent["name"])
    date: datetime = kwargs.get("date", datetime_utils.get_now())
    return {
        "developers": await bill_domain.get_authors_data(
            date=date,
            group=group_name,
        ),
    }
