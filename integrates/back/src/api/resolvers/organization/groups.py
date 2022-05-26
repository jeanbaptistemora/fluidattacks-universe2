from dataloaders import (
    Dataloaders,
)
from db_model.groups.types import (
    Group,
)
from db_model.organizations.types import (
    Organization,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from groups import (
    domain as groups_domain,
)
from newutils import (
    groups as groups_utils,
    token as token_utils,
)
from typing import (
    Any,
    Union,
)


async def resolve(
    parent: Union[Organization, dict[str, Any]],
    info: GraphQLResolveInfo,
    **_kwargs: None,
) -> tuple[Group, ...]:
    loaders: Dataloaders = info.context.loaders
    user_info: dict[str, str] = await token_utils.get_jwt_content(info.context)
    user_email: str = user_info["user_email"]
    if isinstance(parent, dict):
        organization_id: str = parent["id"]
    else:
        organization_id = parent.id
    user_group_names: list[str] = await groups_domain.get_groups_by_user(
        user_email, organization_id=organization_id
    )
    user_groups: tuple[Group, ...] = await loaders.group.load_many(
        user_group_names
    )

    return groups_utils.filter_active_groups(user_groups)
