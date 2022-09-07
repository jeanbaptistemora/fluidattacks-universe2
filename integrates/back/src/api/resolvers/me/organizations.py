# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from dataloaders import (
    Dataloaders,
)
from db_model.organization_access.types import (
    OrganizationAccess,
)
from db_model.organizations.types import (
    Organization,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils import (
    organizations as orgs_utils,
)
from typing import (
    Any,
)


async def resolve(
    parent: dict[str, Any],
    info: GraphQLResolveInfo,
    **_kwargs: None,
) -> tuple[Organization, ...]:
    loaders: Dataloaders = info.context.loaders
    user_email = str(parent["user_email"])
    stakeholder_orgs: tuple[
        OrganizationAccess, ...
    ] = await loaders.stakeholder_organizations_access.load(user_email)
    organization_ids: list[str] = [
        org.organization_id for org in stakeholder_orgs
    ]
    organizations = await loaders.organization.load_many(organization_ids)

    return orgs_utils.filter_active_organizations(organizations)
