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
)
from sessions import (
    domain as sessions_domain,
)


async def resolve(
    parent: Organization,
    info: GraphQLResolveInfo,
    **_kwargs: None,
) -> tuple[Group, ...]:
    loaders: Dataloaders = info.context.loaders
    user_info: dict[str, str] = await sessions_domain.get_jwt_content(
        info.context
    )
    user_email: str = user_info["user_email"]
    user_group_names: list[
        str
    ] = await groups_domain.get_groups_by_stakeholder(
        loaders, user_email, organization_id=parent.id
    )
    user_groups: tuple[Group, ...] = await loaders.group.load_many(
        user_group_names
    )

    return groups_utils.filter_active_groups(user_groups)
