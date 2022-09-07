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
    Root,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from typing import (
    cast,
)


async def resolve(
    parent: Group,
    info: GraphQLResolveInfo,
    **_kwargs: None,
) -> tuple[Credentials, ...]:
    loaders: Dataloaders = info.context.loaders
    group_roots: tuple[Root, ...] = await loaders.group_roots.load(parent.name)
    group_credential_ids = {
        root.state.credential_id
        for root in group_roots
        if isinstance(root, GitRoot) and root.state.credential_id
    }
    group_credentials = cast(
        tuple[Credentials, ...],
        await loaders.credentials.load_many(
            tuple(
                CredentialsRequest(
                    id=credential_id,
                    organization_id=parent.organization_id,
                )
                for credential_id in group_credential_ids
            )
        ),
    )

    return group_credentials
