# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from dataloaders import (
    Dataloaders,
)
from db_model.roots.types import (
    GitRoot,
    URLRoot,
)
from decorators import (
    enforce_group_level_auth_async,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from typing import (
    Union,
)


@enforce_group_level_auth_async
async def resolve(
    parent: Union[GitRoot, URLRoot], info: GraphQLResolveInfo
) -> str:
    loaders: Dataloaders = info.context.loaders
    return await loaders.root_secrets.load((parent.id))
