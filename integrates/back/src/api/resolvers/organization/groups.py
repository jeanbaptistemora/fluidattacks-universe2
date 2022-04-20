from custom_types import (
    Organization,
)
from dataloaders import (
    Dataloaders,
)
from db_model.groups.types import (
    Group,
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
from organizations import (
    domain as orgs_domain,
)
from typing import (
    Tuple,
)


async def resolve(
    parent: Organization, info: GraphQLResolveInfo, **_kwargs: None
) -> Tuple[Group, ...]:
    user_info: dict[str, str] = await token_utils.get_jwt_content(info.context)
    user_email: str = user_info["user_email"]
    org_id: str = parent["id"]
    user_groups: list[str] = await groups_domain.get_groups_by_user(
        user_email, organization_id=org_id
    )

    loaders: Dataloaders = info.context.loaders
    org_name: str = await orgs_domain.get_name_by_id(org_id)
    groups: tuple[Group, ...] = await loaders.group_typed.load_many(
        tuple((group, org_name) for group in user_groups)
    )
    return groups_utils.filter_active_groups(groups)
