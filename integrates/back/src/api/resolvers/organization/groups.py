from .schema import (
    ORGANIZATION,
)
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


@ORGANIZATION.field("groups")
async def resolve(
    parent: Organization,
    info: GraphQLResolveInfo,
    **_kwargs: None,
) -> list[Group]:
    loaders: Dataloaders = info.context.loaders
    session_info = await sessions_domain.get_jwt_content(info.context)
    email: str = session_info["user_email"]
    stakeholder_group_names = await groups_domain.get_groups_by_stakeholder(
        loaders, email, organization_id=parent.id
    )
    stakeholder_groups = await loaders.group.load_many(stakeholder_group_names)

    return groups_utils.filter_active_groups(stakeholder_groups)
