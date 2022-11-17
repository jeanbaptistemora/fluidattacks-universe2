# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from dataloaders import (
    Dataloaders,
)
from db_model.integration_repositories.types import (
    OrganizationIntegrationRepositoryConnection,
    OrganizationIntegrationRepositoryRequest,
)
from db_model.organizations.types import (
    Organization,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from typing import (
    Optional,
)


async def resolve(
    parent: Organization,
    info: GraphQLResolveInfo,
    after: Optional[str] = None,
    first: Optional[int] = None,
    **_kwargs: None,
) -> tuple[OrganizationIntegrationRepositoryConnection, ...]:
    loaders: Dataloaders = info.context.loaders
    current_repositories: tuple[
        OrganizationIntegrationRepositoryConnection, ...
    ] = await loaders.organization_unreliable_integration_repositories_c.load(
        OrganizationIntegrationRepositoryRequest(
            organization_id=parent.id,
            after=after,
            first=first,
            paginate=True,
        )
    )

    return current_repositories
