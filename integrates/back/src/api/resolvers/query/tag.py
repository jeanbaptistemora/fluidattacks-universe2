from aioextensions import (
    collect,
)
from custom_exceptions import (
    TagNotFound,
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
from db_model.portfolios.types import (
    Portfolio,
)
from decorators import (
    require_login,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from groups import (
    domain as groups_domain,
)
from newutils import (
    token as token_utils,
)
from organizations import (
    domain as orgs_domain,
)
from tags import (
    domain as tags_domain,
)


@require_login
async def resolve(
    _parent: None, info: GraphQLResolveInfo, **kwargs: str
) -> Portfolio:
    loaders: Dataloaders = info.context.loaders
    tag_name: str = kwargs["tag"].lower()
    user_data: dict[str, str] = await token_utils.get_jwt_content(info.context)
    user_email: str = user_data["user_email"]
    user_group_names: list[str] = await groups_domain.get_groups_by_user(
        loaders, user_email
    )
    are_valid_groups = await collect(
        tuple(
            groups_domain.is_valid(loaders, group_name)
            for group_name in user_group_names
        )
    )
    user_group_names_filtered = [
        group_name
        for group_name, is_valid in zip(user_group_names, are_valid_groups)
        if is_valid
    ]

    if not user_group_names_filtered:
        raise TagNotFound()

    group: Group = await loaders.group.load(user_group_names_filtered[0])
    organization: Organization = await loaders.organization.load(
        group.organization_id
    )
    org_group_names_filtered = [
        group_name
        for group_name in user_group_names_filtered
        if group_name
        in await orgs_domain.get_group_names(loaders, organization.id)
    ]

    allowed_tags: list[str] = await tags_domain.filter_allowed_tags(
        loaders, organization.name, org_group_names_filtered
    )

    if tag_name not in allowed_tags:
        raise TagNotFound()

    portfolio: Portfolio = await loaders.portfolio.load(
        (organization.name, tag_name)
    )
    return portfolio
