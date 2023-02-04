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
from db_model import (
    portfolios as portfolios_model,
)
from db_model.groups.types import (
    Group,
)
from db_model.portfolios.types import (
    Portfolio,
    PortfolioRequest,
)
from organizations import (
    domain as orgs_domain,
    utils as orgs_utils,
)
from typing import (
    Optional,
)


async def remove(organization_name: str, portfolio_id: str) -> None:
    await portfolios_model.remove(
        organization_name=organization_name, portfolio_id=portfolio_id
    )


async def filter_allowed_tags(
    loaders: Dataloaders,
    organization_name: str,
    user_group_names: list[str],
) -> list[str]:
    groups = await loaders.group.load_many(user_group_names)
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
        org_id, portfolio = subject.split("PORTFOLIO#")
        organization = await orgs_utils.get_organization(loaders, org_id)
        organization_name = organization.name
        portfolio_info: Optional[Portfolio] = await loaders.portfolio.load(
            PortfolioRequest(
                organization_name=organization_name, portfolio_id=portfolio
            )
        )
        if portfolio_info:
            portfolio_groups: list[str] = list(portfolio_info.groups)
            org_access, group_access = await collect(
                (
                    orgs_domain.has_access(
                        loaders=loaders, email=email, organization_id=org_id
                    ),
                    authz.get_group_level_roles(
                        loaders=loaders,
                        email=email,
                        groups=portfolio_groups,
                    ),
                )
            )
            return org_access and any(group_access.values())  # type: ignore
    raise PortfolioNotFound()


async def is_tag_allowed(
    loaders: Dataloaders,
    user_groups: tuple[Group, ...],
    organization_name: str,
    tag: str,
) -> bool:
    org_tag: Optional[Portfolio] = await loaders.portfolio.load(
        PortfolioRequest(organization_name=organization_name, portfolio_id=tag)
    )
    if org_tag:
        all_groups_tag = org_tag.groups
        user_groups_tag = [
            group.name
            for group in user_groups
            if group.state.tags
            and tag in [p_tag.lower() for p_tag in group.state.tags]
        ]
        return any(group in user_groups_tag for group in all_groups_tag)
    return False


async def update(
    portfolio: Portfolio,
) -> None:
    await portfolios_model.update(portfolio=portfolio)
