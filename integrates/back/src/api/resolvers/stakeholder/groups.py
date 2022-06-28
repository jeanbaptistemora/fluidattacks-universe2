from aioextensions import (
    collect,
)
from dataloaders import (
    Dataloaders,
)
from db_model.groups.types import (
    Group,
)
from db_model.stakeholders.types import (
    Stakeholder,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from groups import (
    domain as groups_domain,
)
from newutils import (
    groups as groups_utils,
)
from typing import (
    List,
    Tuple,
)


async def resolve(
    parent: Stakeholder,
    info: GraphQLResolveInfo,
    **_kwargs: None,
) -> Tuple[Group, ...]:
    loaders: Dataloaders = info.context.loaders
    email = parent.email
    active, inactive = await collect(
        [
            groups_domain.get_groups_by_user(loaders, email),
            groups_domain.get_groups_by_user(loaders, email, active=False),
        ]
    )
    user_groups: List[str] = active + inactive

    groups: Tuple[Group, ...] = await loaders.group.load_many(user_groups)
    return groups_utils.filter_active_groups(groups)
