# Standard
from datetime import datetime
from typing import cast, Dict

# Third party
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend.decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_drills_white
)
from backend.domain import bill as bill_domain
from backend.typing import Historic, Project as Group
from backend.utils import (
    datetime as datetime_utils,
)


@concurrent_decorators(
    enforce_group_level_auth_async,
    require_drills_white,
)
async def resolve(
    parent: Group,
    _info: GraphQLResolveInfo,
    **kwargs: datetime
) -> Dict[str, Historic]:
    group_name: str = cast(str, parent['name'])
    date: datetime = kwargs.get('date', datetime_utils.get_now())

    return {
        'developers': await bill_domain.get_authors_data(
            date=date,
            group=group_name,
        ),
    }
