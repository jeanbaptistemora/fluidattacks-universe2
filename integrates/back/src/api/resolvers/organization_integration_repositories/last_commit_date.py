# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from db_model.integration_repositories.types import (
    OrganizationIntegrationRepository,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from typing import (
    Optional,
)


async def resolve(
    parent: OrganizationIntegrationRepository,
    _info: GraphQLResolveInfo,
) -> Optional[str]:

    return (
        parent.last_commit_date
        if parent.last_commit_date is not None
        else None
    )
