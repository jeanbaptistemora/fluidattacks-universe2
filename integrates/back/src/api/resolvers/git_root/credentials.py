# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from dataloaders import (
    Dataloaders,
)
from db_model.credentials.types import (
    Credentials,
    CredentialsRequest,
)
from db_model.groups.types import (
    Group,
)
from db_model.roots.types import (
    GitRoot,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from typing import (
    Optional,
)


async def resolve(
    parent: GitRoot, info: GraphQLResolveInfo
) -> Optional[Credentials]:
    loaders: Dataloaders = info.context.loaders
    group: Group = await loaders.group.load(parent.group_name)
    if parent.state.credential_id:
        request = CredentialsRequest(
            id=parent.state.credential_id,
            organization_id=group.organization_id,
        )
        credential: Credentials = await loaders.credentials.load(request)
        return credential

    return None
