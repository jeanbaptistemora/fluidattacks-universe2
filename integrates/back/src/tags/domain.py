from aioextensions import (
    collect,
)
import authz
from contextlib import (
    suppress,
)
from custom_exceptions import (
    PortfolioNotFound,
)
from dataloaders import (
    Dataloaders,
)
from db_model.groups.types import (
    Group,
)
from db_model.portfolios.types import (
    PortfolioRequest,
)
from organizations import (
    domain as orgs_domain,
    utils as orgs_utils,
)
from typing import (
    Iterable,
)


async def filter_allowed_tags(
    loaders: Dataloaders,
    organization_name: str,
    group_names: list[str],
) -> list[str]:
    groups = await loaders.group.load_many(group_names)
    all_tags = {
        str(tag).lower()
        for group in groups
        if group.state.tags
        for tag in group.state.tags
    }
    are_tags_allowed = await collect(
        is_tag_allowed(loaders, tuple(groups), organization_name, tag)
        for tag in all_tags
    )
    tags = [
        tag
        for tag, is_tag_allowed in zip(all_tags, are_tags_allowed)
        if is_tag_allowed
    ]
    return tags


async def has_access(loaders: Dataloaders, email: str, subject: str) -> bool:
    with suppress(ValueError):
        organization_id, portfolio_id = subject.split("PORTFOLIO#")
        organization = await orgs_utils.get_organization(
            loaders, organization_id
        )
        portfolio = await loaders.portfolio.load(
            PortfolioRequest(
                organization_name=organization.name, portfolio_id=portfolio_id
            )
        )
        if portfolio is None:
            raise PortfolioNotFound()

        organization_access = await orgs_domain.has_access(
            loaders=loaders, email=email, organization_id=organization_id
        )
        group_access = await authz.get_group_level_roles(
            loaders=loaders,
            email=email,
            groups=list(portfolio.groups),
        )

        return organization_access and any(group_access.values())

    return False


async def is_tag_allowed(
    loaders: Dataloaders,
    stakeholder_groups: Iterable[Group],
    organization_name: str,
    portfolio_id: str,
) -> bool:
    portfolio = await loaders.portfolio.load(
        PortfolioRequest(
            organization_name=organization_name, portfolio_id=portfolio_id
        )
    )
    if portfolio is None:
        return False

    stakeholder_portfolios_group_names = [
        group.name
        for group in stakeholder_groups
        if group.state.tags
        and portfolio_id in [p_tag.lower() for p_tag in group.state.tags]
    ]

    return any(
        group in stakeholder_portfolios_group_names
        for group in portfolio.groups
    )
