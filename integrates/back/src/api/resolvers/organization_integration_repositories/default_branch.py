# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from db_model.integration_repositories.types import (
    OrganizationIntegrationRepository,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


async def resolve(
    parent: OrganizationIntegrationRepository,
    _info: GraphQLResolveInfo,
) -> str:

    return parent.branch if parent.branch is not None else ""
