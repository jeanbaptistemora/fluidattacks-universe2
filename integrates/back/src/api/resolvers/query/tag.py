from .schema import (
    QUERY,
)
from aioextensions import (
    collect,
)
from custom_exceptions import (
    PortfolioNotFound,
    TagNotFound,
)
from dataloaders import (
    Dataloaders,
)
from db_model.portfolios.types import (
    Portfolio,
    PortfolioRequest,
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
from organizations import (
    domain as orgs_domain,
    utils as orgs_utils,
)
from sessions import (
    domain as sessions_domain,
)
from tags import (
    domain as tags_domain,
)


@QUERY.field("tag")
@require_login
async def resolve(
    _parent: None, info: GraphQLResolveInfo, **kwargs: str
) -> Portfolio:
    loaders: Dataloaders = info.context.loaders
    user_data = await sessions_domain.get_jwt_content(info.context)
    user_email = user_data["user_email"]
    user_group_names = await groups_domain.get_groups_by_stakeholder(
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

    group = await loaders.group.load(user_group_names_filtered[0])
    organization_id = kwargs.get("organizationId") or group.organization_id
    organization = await orgs_utils.get_organization(loaders, organization_id)
    org_group_names_filtered = [
        group_name
        for group_name in user_group_names_filtered
        if group_name
        in await orgs_domain.get_group_names(loaders, organization.id)
    ]
    allowed_tags = await tags_domain.filter_allowed_tags(
        loaders, organization.name, org_group_names_filtered
    )
    if (tag_name := kwargs["tag"].lower()) not in allowed_tags:
        raise TagNotFound()

    if portfolio := await loaders.portfolio.load(
        PortfolioRequest(
            organization_name=organization.name, portfolio_id=tag_name
        )
    ):
        return portfolio

    raise PortfolioNotFound()
