# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

import authz
from dataloaders import (
    Dataloaders,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from typing import (
    Any,
)


async def resolve(
    parent: dict[str, Any], info: GraphQLResolveInfo, **_kwargs: str
) -> str:
    loaders: Dataloaders = info.context.loaders
    user_email = str(parent["user_email"])
    return await authz.get_user_level_role(loaders, user_email)
