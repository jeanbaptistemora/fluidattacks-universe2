# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from billing import (
    domain as billing_domain,
)
from billing.types import (
    OrganizationAuthor,
    Price,
)
from dataloaders import (
    Dataloaders,
)
from datetime import (
    datetime,
)
from db_model.groups.enums import (
    GroupTier,
)
from db_model.groups.types import (
    Group,
)
from db_model.organizations.types import (
    Organization,
)
from decorators import (
    concurrent_decorators,
    enforce_organization_level_auth_async,
    require_login,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils import (
    datetime as datetime_utils,
)
from typing import (
    Any,
)


@concurrent_decorators(
    enforce_organization_level_auth_async,
    require_login,
)
async def resolve(
    parent: Organization,
    info: GraphQLResolveInfo,
    **kwargs: datetime,
) -> dict[str, Any]:
    loaders: Dataloaders = info.context.loaders
    org_groups: tuple[Group, ...] = await loaders.organization_groups.load(
        parent.id
    )
    date: datetime = kwargs.get("date", datetime_utils.get_now())
    org_authors: tuple[
        OrganizationAuthor, ...
    ] = await billing_domain.get_organization_authors(
        date=date,
        org_id=parent.id,
        loaders=loaders,
    )

    total: int = len(org_authors)

    prices: dict[str, Price] = await billing_domain.get_prices()
    org_squad_authors: int = 0
    for group in org_groups:
        for author in org_authors:
            if (
                group.name in author.groups
                and group.state.tier == GroupTier.SQUAD
            ):
                org_squad_authors += 1
    current_spend: int = int(org_squad_authors * prices["squad"].amount / 100)

    return {
        "current_spend": current_spend,
        "data": org_authors,
        "total": total,
    }
